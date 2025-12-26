# Datei-Transfer-Tool: win1 → Google Drive → win2 → target-host

## Übersicht

Dieses Tool ermöglicht den Transfer von Dateien von einem Windows-Computer (win1) zu einem Linux-Server (target-host), der nicht direkt über das Internet erreichbar ist. Der Transfer erfolgt über einen mehrstufigen Prozess:

```
win1 (Windows) 
  ↓ (automatischer Upload)
Google Drive (vordefinierter Ordner)
  ↓ (automatischer Download)
win2 (Windows Notebook)
  ↓ (SCP über Jumpserver)
target-host (Linux Server)
```

## Architektur

### Komponenten

1. **win1_upload_monitor.py** (auf win1)
   - Überwacht einen lokalen Ordner mit `watchdog`
   - Lädt neue Dateien automatisch zu Google Drive hoch
   - Verwendet Google Drive API v3

2. **win2_download_and_transfer.py** (auf win2)
   - Überwacht Google Drive auf neue Dateien
   - Lädt neue Dateien herunter
   - Überträgt Dateien per SCP über Jumpserver zu target-host
   - Verwendet `paramiko` für SSH/SCP

3. **config.json**
   - Zentrale Konfigurationsdatei für alle Parameter

## Voraussetzungen

- **win1**: Python 3.8+, Google Drive API Credentials, Internetverbindung
- **win2**: Python 3.8+, Google Drive API Credentials, SSH/SCP Zugriff auf Jumpserver, Internetverbindung
- **target-host**: SSH-Zugriff über Jumpserver, Schreibberechtigung im Zielordner

## Schnellstart

```powershell
# 1. Dependencies installieren
pip install -r requirements.txt
# oder: uv pip install --user -r requirements.txt

# 2. config.json anpassen (Google Drive Folder ID, SSH-Details)

# 3. Erste Authentifizierung
python win1_upload_monitor.py  # Browser öffnet sich → Anmelden
python win2_download_and_transfer.py  # Browser öffnet sich → Anmelden
```

**Detaillierte Anleitung**: Siehe [QUICK_START.md](QUICK_START.md)

## Workflow

1. **Upload-Phase (win1)**: Datei in überwachten Ordner → automatischer Upload zu Google Drive
2. **Download-Phase (win2)**: Google Drive wird regelmäßig geprüft → neue Dateien werden heruntergeladen
3. **Transfer-Phase (win2)**: Heruntergeladene Dateien werden per SCP über Jumpserver zu target-host übertragen

## Dokumentation

- **[QUICK_START.md](QUICK_START.md)** - Kompakte Setup-Anleitung und Verwendung
- **[docs/01_SETUP.md](docs/01_SETUP.md)** - Detaillierte Schritt-für-Schritt Setup-Anleitung
- **[docs/GOOGLE_CREDENTIALS_SETUP.md](docs/GOOGLE_CREDENTIALS_SETUP.md)** - Google Drive API Credentials Setup
- **[docs/GOOGLE_DRIVE_SETUP.md](docs/GOOGLE_DRIVE_SETUP.md)** - Google Drive Folder ID finden
- **[docs/PAGEANT_SETUP.md](docs/PAGEANT_SETUP.md)** - SSH-Agent (Pageant) Setup
- **[docs/02_HOW_TO_START.md](docs/02_HOW_TO_START.md)** - Start-Methoden (Task Scheduler, etc.)
- **[docs/INSTALL_DEPENDENCIES.md](docs/INSTALL_DEPENDENCIES.md)** - Dependencies Installation mit pip
- **[docs/INSTALL_WITH_UV.md](docs/INSTALL_WITH_UV.md)** - Dependencies Installation mit uv (ohne Admin)
- **[docs/00_ARCHITECTURE.md](docs/00_ARCHITECTURE.md)** - Technische Architektur

## Sicherheit

- Google Drive API verwendet OAuth 2.0
- SSH-Verbindungen verwenden SSH-Keys (empfohlen) oder Pageant
- Credentials sollten sicher gespeichert werden (nicht in Git committen)

## Erweiterungen

- E-Mail-Benachrichtigungen bei Erfolg/Fehler
- Verschlüsselung der Dateien vor Upload
- Komprimierung großer Dateien
- Web-Interface für Status-Monitoring
