#!/usr/bin/env python3
"""
win2_download_and_transfer.py
Überwacht Google Drive auf neue Dateien, lädt sie herunter und überträgt sie zu target-host.
"""

import os
import json
import time
import logging
import shutil
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import pickle
import paramiko
from paramiko.agent import Agent
from scp import SCPClient

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('win2_transfer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GoogleDriveMonitor:
    """Klasse für Google Drive Monitoring und Download."""
    
    def __init__(self, config):
        self.config = config
        self.service = None
        self.credentials = None
        self.processed_file_ids = set()
        self._authenticate()
        self._load_processed_files()
    
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
    
    def _load_processed_files(self):
        """Lädt Liste bereits verarbeiteter Dateien."""
        processed_file = 'processed_files.txt'
        if os.path.exists(processed_file):
            with open(processed_file, 'r') as f:
                self.processed_file_ids = set(line.strip() for line in f if line.strip())
    
    def _save_processed_file(self, file_id):
        """Speichert verarbeitete Datei-ID."""
        processed_file = 'processed_files.txt'
        with open(processed_file, 'a') as f:
            f.write(f"{file_id}\n")
        self.processed_file_ids.add(file_id)
    
    def check_for_new_files(self, folder_id):
        """
        Prüft Google Drive auf neue Dateien im angegebenen Ordner.
        
        Args:
            folder_id: ID des Google Drive Ordners
        
        Returns:
            Liste von Datei-Informationen (id, name)
        """
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, createdTime, modifiedTime)"
            ).execute()
            
            files = results.get('files', [])
            new_files = [
                f for f in files 
                if f['id'] not in self.processed_file_ids
            ]
            
            return new_files
        
        except Exception as e:
            logger.error(f"Fehler beim Prüfen auf neue Dateien: {e}")
            return []
    
    def download_file(self, file_id, file_name, download_folder):
        """
        Lädt eine Datei von Google Drive herunter.
        
        Args:
            file_id: ID der Datei in Google Drive
            file_name: Name der Datei
            download_folder: Lokaler Download-Ordner
        
        Returns:
            Pfad zur heruntergeladenen Datei oder None bei Fehler
        """
        try:
            os.makedirs(download_folder, exist_ok=True)
            file_path = os.path.join(download_folder, file_name)
            
            logger.info(f"Lade Datei herunter: {file_name} (ID: {file_id})")
            
            request = self.service.files().get_media(fileId=file_id)
            fh = io.FileIO(file_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                if status:
                    logger.info(f"Download Fortschritt: {int(status.progress() * 100)}%")
            
            fh.close()
            logger.info(f"Download erfolgreich: {file_path}")
            return file_path
        
        except Exception as e:
            logger.error(f"Fehler beim Download von {file_name}: {e}")
            return None


class SCPTransfer:
    """Klasse für SCP-Transfer über Jumpserver zu target-host."""
    
    def __init__(self, config):
        self.config = config
        self.jumpserver_config = config['target_host']['jumpserver']
        self.target_config = config['target_host']['target']
    
    def _create_ssh_client(self, host, port, username, key_file=None, password=None, use_ssh_agent=True):
        """
        Erstellt einen SSH-Client.
        
        Args:
            host: Hostname oder IP
            port: SSH-Port
            username: Benutzername
            key_file: Pfad zur SSH-Key-Datei (optional)
            password: Passwort (optional)
            use_ssh_agent: True = versuche zuerst SSH-Agent (Pageant) zu verwenden
        
        Returns:
            SSH-Client
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            # Versuche zuerst SSH-Agent (Pageant) zu verwenden
            if use_ssh_agent:
                try:
                    agent = Agent()
                    agent_keys = agent.get_keys()
                    if agent_keys:
                        logger.info(f"Verwende SSH-Agent (Pageant) für {host}")
                        client.connect(
                            hostname=host,
                            port=port,
                            username=username,
                            pkey=agent_keys[0],  # Verwende ersten verfügbaren Key
                            timeout=30
                        )
                        return client
                    else:
                        logger.debug(f"SSH-Agent verfügbar, aber keine Keys gefunden für {host}")
                except Exception as e:
                    logger.debug(f"SSH-Agent nicht verfügbar oder Fehler: {e}, verwende Key-Datei")
            
            # Fallback: Verwende Key-Datei
            if key_file and os.path.exists(key_file):
                logger.info(f"Verwende Key-Datei für {host}: {key_file}")
                client.connect(
                    hostname=host,
                    port=port,
                    username=username,
                    key_filename=key_file,
                    timeout=30
                )
            # Fallback: Verwende Passwort
            elif password:
                logger.info(f"Verwende Passwort-Authentifizierung für {host}")
                client.connect(
                    hostname=host,
                    port=port,
                    username=username,
                    password=password,
                    timeout=30
                )
            else:
                raise ValueError("Keine Authentifizierungsmethode verfügbar. Bitte SSH-Agent (Pageant), key_file oder password konfigurieren.")
            
            return client
        
        except Exception as e:
            logger.error(f"Fehler beim SSH-Verbindungsaufbau zu {host}: {e}")
            raise
    
    def transfer_file(self, local_file_path):
        """
        Überträgt eine Datei über Jumpserver zu target-host.
        
        Args:
            local_file_path: Pfad zur lokalen Datei
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            file_name = os.path.basename(local_file_path)
            logger.info(f"Starte Transfer von {file_name} zu target-host...")
            
            # Verbindung zu Jumpserver
            use_ssh_agent = self.jumpserver_config.get('use_ssh_agent', True)
            jump_client = self._create_ssh_client(
                host=self.jumpserver_config['host'],
                port=self.jumpserver_config['port'],
                username=self.jumpserver_config['username'],
                key_file=self.jumpserver_config.get('key_file'),
                password=self.jumpserver_config.get('password'),
                use_ssh_agent=use_ssh_agent
            )
            
            # SSH-Tunnel zu target-host über Jumpserver
            target_host = self.target_config['host']
            target_port = self.target_config['port']
            target_username = self.target_config['username']
            
            # Transport über Jumpserver
            jump_transport = jump_client.get_transport()
            dest_addr = (target_host, target_port)
            local_addr = ('localhost', 0)
            channel = jump_transport.open_channel("direct-tcpip", dest_addr, local_addr)
            
            # Verbindung zu target-host
            target_client = paramiko.SSHClient()
            target_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            target_key_file = self.target_config.get('key_file')
            target_password = self.target_config.get('password')
            use_ssh_agent_target = self.target_config.get('use_ssh_agent', True)
            
            # Versuche zuerst SSH-Agent (Pageant)
            connected = False
            if use_ssh_agent_target:
                try:
                    agent = Agent()
                    agent_keys = agent.get_keys()
                    if agent_keys:
                        logger.info(f"Verwende SSH-Agent (Pageant) für target-host {target_host}")
                        target_client.connect(
                            hostname=target_host,
                            port=target_port,
                            username=target_username,
                            pkey=agent_keys[0],
                            sock=channel
                        )
                        connected = True
                except Exception as e:
                    logger.debug(f"SSH-Agent nicht verfügbar für target-host: {e}")
            
            # Fallback: Verwende Key-Datei
            if not connected and target_key_file and os.path.exists(target_key_file):
                logger.info(f"Verwende Key-Datei für target-host: {target_key_file}")
                target_key = paramiko.RSAKey.from_private_key_file(target_key_file)
                target_client.connect(
                    hostname=target_host,
                    port=target_port,
                    username=target_username,
                    pkey=target_key,
                    sock=channel
                )
                connected = True
            # Fallback: Verwende Passwort
            elif not connected and target_password:
                logger.info(f"Verwende Passwort-Authentifizierung für target-host")
                target_client.connect(
                    hostname=target_host,
                    port=target_port,
                    username=target_username,
                    password=target_password,
                    sock=channel
                )
                connected = True
            
            if not connected:
                raise ValueError("Keine Authentifizierungsmethode verfügbar für target-host. Bitte SSH-Agent (Pageant), key_file oder password konfigurieren.")
            
            # SCP Transfer
            target_folder = self.target_config['target_folder']
            
            # Erstelle Zielordner falls nicht vorhanden
            stdin, stdout, stderr = target_client.exec_command(f'mkdir -p {target_folder}')
            stdout.channel.recv_exit_status()
            
            # SCP Transfer durchführen
            with SCPClient(target_client.get_transport()) as scp:
                scp.put(local_file_path, target_folder)
            
            logger.info(f"Transfer erfolgreich: {file_name} → {target_host}:{target_folder}")
            
            # Verbindungen schließen
            target_client.close()
            jump_client.close()
            
            return True
        
        except Exception as e:
            logger.error(f"Fehler beim Transfer von {local_file_path}: {e}")
            return False


def main():
    """Hauptfunktion."""
    # Konfiguration laden
    config_path = 'config.json'
    if not os.path.exists(config_path):
        logger.error(f"Konfigurationsdatei nicht gefunden: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Download-Ordner prüfen
    download_folder = config['win2']['download_folder']
    if not os.path.exists(download_folder):
        os.makedirs(download_folder, exist_ok=True)
        logger.info(f"Download-Ordner erstellt: {download_folder}")
    
    # Google Drive Monitor initialisieren
    try:
        monitor = GoogleDriveMonitor(config)
    except Exception as e:
        logger.error(f"Fehler bei Google Drive Initialisierung: {e}")
        return
    
    # SCP Transfer initialisieren
    try:
        scp_transfer = SCPTransfer(config)
    except Exception as e:
        logger.error(f"Fehler bei SCP Transfer Initialisierung: {e}")
        return
    
    # Hauptschleife
    folder_id = config['win2']['google_drive_folder_id']
    check_interval = config['win2']['check_interval_seconds']
    delete_after_transfer = config['win2'].get('delete_after_transfer', False)
    
    logger.info(f"Überwache Google Drive Ordner (ID: {folder_id})")
    logger.info(f"Prüfintervall: {check_interval} Sekunden")
    logger.info("Drücken Sie Ctrl+C zum Beenden...")
    
    try:
        while True:
            # Prüfe auf neue Dateien
            new_files = monitor.check_for_new_files(folder_id)
            
            if new_files:
                logger.info(f"{len(new_files)} neue Datei(en) gefunden")
                
                for file_info in new_files:
                    file_id = file_info['id']
                    file_name = file_info['name']
                    
                    # Datei herunterladen
                    local_file_path = monitor.download_file(
                        file_id, file_name, download_folder
                    )
                    
                    if local_file_path:
                        # Datei zu target-host übertragen
                        if scp_transfer.transfer_file(local_file_path):
                            # Als verarbeitet markieren
                            monitor._save_processed_file(file_id)
                            
                            # Datei löschen falls konfiguriert
                            if delete_after_transfer:
                                try:
                                    os.remove(local_file_path)
                                    logger.info(f"Lokale Datei gelöscht: {local_file_path}")
                                except Exception as e:
                                    logger.warning(f"Konnte Datei nicht löschen: {e}")
                        else:
                            logger.error(f"Transfer fehlgeschlagen für {file_name}")
                    else:
                        logger.error(f"Download fehlgeschlagen für {file_name}")
            else:
                logger.debug("Keine neuen Dateien gefunden")
            
            # Warte auf nächsten Check
            time.sleep(check_interval)
    
    except KeyboardInterrupt:
        logger.info("Beende Überwachung...")
    
    logger.info("Programm beendet.")


if __name__ == '__main__':
    main()

