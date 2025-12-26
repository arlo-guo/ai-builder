#!/usr/bin/env python3
"""
win1_upload_monitor.py
Überwacht einen lokalen Ordner und lädt neue Dateien automatisch zu Google Drive hoch.
"""

import os
import json
import time
import logging
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('win1_upload.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GoogleDriveUploader:
    """Klasse für Google Drive Upload-Operationen."""
    
    def __init__(self, config):
        self.config = config
        self.service = None
        self.credentials = None
        self._authenticate()
    
    def _authenticate(self):
        """Authentifiziert sich bei Google Drive API."""
        creds = None
        token_file = self.config['google_drive']['token_file']
        credentials_file = self.config['google_drive']['credentials_file']
        scopes = self.config['google_drive']['scopes']
        
        # Prüfe ob Token bereits existiert
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Wenn keine gültigen Credentials vorhanden, OAuth Flow starten
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_file):
                    logger.error(f"Credentials-Datei nicht gefunden: {credentials_file}")
                    raise FileNotFoundError(f"Credentials-Datei nicht gefunden: {credentials_file}")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, scopes)
                creds = flow.run_local_server(port=0)
            
            # Token speichern
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.credentials = creds
        self.service = build('drive', 'v3', credentials=creds)
        logger.info("Google Drive Authentifizierung erfolgreich")
    
    def upload_file(self, file_path, folder_id=None):
        """
        Lädt eine Datei zu Google Drive hoch.
        
        Args:
            file_path: Pfad zur lokalen Datei
            folder_id: ID des Zielordners in Google Drive
        
        Returns:
            ID der hochgeladenen Datei oder None bei Fehler
        """
        try:
            file_name = os.path.basename(file_path)
            logger.info(f"Starte Upload von {file_name} zu Google Drive...")
            
            file_metadata = {
                'name': file_name
            }
            
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(file_path, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file.get('id')
            logger.info(f"Upload erfolgreich! Datei-ID: {file_id}, Name: {file_name}")
            return file_id
        
        except Exception as e:
            logger.error(f"Fehler beim Upload von {file_path}: {str(e)}")
            return None


class FileUploadHandler(FileSystemEventHandler):
    """Handler für Dateisystem-Ereignisse."""
    
    def __init__(self, uploader, config):
        self.uploader = uploader
        self.config = config
        self.watch_folder = config['win1']['watch_folder']
        self.processed_files = set()
    
    def on_created(self, event):
        """Wird aufgerufen, wenn eine neue Datei erstellt wird."""
        if event.is_directory:
            return
        
        file_path = event.src_path
        self._handle_file(file_path)
    
    def on_moved(self, event):
        """Wird aufgerufen, wenn eine Datei verschoben wird."""
        if event.is_directory:
            return
        
        file_path = event.dest_path
        self._handle_file(file_path)
    
    def _handle_file(self, file_path):
        """Verarbeitet eine neue Datei."""
        # Warte kurz, damit Datei vollständig geschrieben ist
        time.sleep(2)
        
        if not os.path.exists(file_path):
            return
        
        # Prüfe ob Datei bereits verarbeitet wurde
        if file_path in self.processed_files:
            return
        
        # Prüfe ob Datei vollständig ist (nicht mehr geschrieben wird)
        if not self._is_file_ready(file_path):
            logger.warning(f"Datei {file_path} ist noch nicht bereit, überspringe...")
            return
        
        logger.info(f"Neue Datei erkannt: {file_path}")
        
        # Upload zu Google Drive
        folder_id = self.config['win1']['google_drive_folder_id']
        file_id = self.uploader.upload_file(file_path, folder_id)
        
        if file_id:
            self.processed_files.add(file_path)
            self._post_upload_action(file_path)
        else:
            logger.error(f"Upload fehlgeschlagen für {file_path}")
    
    def _is_file_ready(self, file_path, max_wait=10):
        """Prüft ob Datei vollständig geschrieben ist."""
        initial_size = os.path.getsize(file_path)
        time.sleep(1)
        final_size = os.path.getsize(file_path)
        return initial_size == final_size
    
    def _post_upload_action(self, file_path):
        """Führt Aktion nach erfolgreichem Upload aus."""
        config_win1 = self.config['win1']
        
        if config_win1.get('delete_after_upload', False):
            try:
                os.remove(file_path)
                logger.info(f"Datei gelöscht: {file_path}")
            except Exception as e:
                logger.error(f"Fehler beim Löschen: {e}")
        
        elif config_win1.get('move_after_upload', False):
            move_to = config_win1.get('move_to_folder')
            if move_to:
                try:
                    os.makedirs(move_to, exist_ok=True)
                    dest_path = os.path.join(move_to, os.path.basename(file_path))
                    shutil.move(file_path, dest_path)
                    logger.info(f"Datei verschoben nach: {dest_path}")
                except Exception as e:
                    logger.error(f"Fehler beim Verschieben: {e}")


def main():
    """Hauptfunktion."""
    # Konfiguration laden
    config_path = 'config.json'
    if not os.path.exists(config_path):
        logger.error(f"Konfigurationsdatei nicht gefunden: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Überwachungsordner prüfen
    watch_folder = config['win1']['watch_folder']
    if not os.path.exists(watch_folder):
        os.makedirs(watch_folder, exist_ok=True)
        logger.info(f"Überwachungsordner erstellt: {watch_folder}")
    
    # Google Drive Uploader initialisieren
    try:
        uploader = GoogleDriveUploader(config)
    except Exception as e:
        logger.error(f"Fehler bei Google Drive Initialisierung: {e}")
        return
    
    # File System Observer einrichten
    event_handler = FileUploadHandler(uploader, config)
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()
    
    logger.info(f"Überwache Ordner: {watch_folder}")
    logger.info("Drücken Sie Ctrl+C zum Beenden...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Beende Überwachung...")
        observer.stop()
    
    observer.join()
    logger.info("Programm beendet.")


if __name__ == '__main__':
    main()

