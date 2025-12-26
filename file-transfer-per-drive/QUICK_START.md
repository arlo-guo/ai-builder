# Quick Start - File Transfer Tool

## Workflow
```
win1 → Google Drive → win2 → target-host (via Jumpserver)
```

## Setup (einmalig)

### 1. Dependencies installieren

**Option A: Mit pip**
```powershell
pip install -r requirements.txt
```

**Option B: Mit uv (ohne Admin-Rechte)**
```powershell
uv pip install --user -r requirements.txt
```

Siehe [docs/INSTALL_DEPENDENCIES.md](docs/INSTALL_DEPENDENCIES.md) oder [docs/INSTALL_WITH_UV.md](docs/INSTALL_WITH_UV.md) für Details.

### 2. Google Drive API Setup

1. Gehen Sie zu [Google Cloud Console](https://console.cloud.google.com/)
2. Erstellen Sie ein neues Projekt oder wählen Sie ein bestehendes
3. Navigieren Sie zu "APIs & Services" > "Library"
4. Suchen Sie nach "Google Drive API" und aktivieren Sie sie
5. Navigieren Sie zu "APIs & Services" > "Credentials"
6. Erstellen Sie OAuth 2.0 Credentials:
   - Application type: "Desktop app"
   - Name: z.B. "File Transfer Tool"
7. Laden Sie `credentials.json` herunter und speichern Sie es im Projektordner
8. Erstellen Sie einen Ordner in Google Drive
9. Kopieren Sie die **Folder ID** aus der URL (nach `/folders/`)

**Detaillierte Anleitung**: Siehe [docs/GOOGLE_CREDENTIALS_SETUP.md](docs/GOOGLE_CREDENTIALS_SETUP.md)

### 3. SSH/SCP Zugriff einrichten

**Option A: Mit Pageant (SSH-Agent) - Empfohlen für Windows**

1. Installieren Sie PuTTY (enthält Pageant)
2. Starten Sie Pageant
3. Laden Sie Ihre SSH-Keys in Pageant
4. In `config.json`: Setzen Sie `"use_ssh_agent": true`

**Option B: Mit SSH-Key-Dateien**

1. Generieren Sie SSH-Keys (falls noch nicht vorhanden):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```
2. Kopieren Sie den Key zu Jumpserver und target-host

**Detaillierte Anleitung**: Siehe [docs/PAGEANT_SETUP.md](docs/PAGEANT_SETUP.md)

### 4. config.json anpassen

Bearbeiten Sie `config.json`:

- **win1**:
  - `watch_folder`: Ordner auf win1, der überwacht wird
  - `google_drive_folder_id`: ID des Google Drive Ordners (aus Schritt 2.9)
  - `delete_after_upload` / `move_after_upload`: Post-Upload-Aktion

- **win2**:
  - `download_folder`: Ordner auf win2 für Downloads
  - `google_drive_folder_id`: **Gleiche ID wie win1!**
  - `check_interval_seconds`: Prüfintervall (Standard: 30 Sekunden)
  - `delete_after_transfer`: Datei nach Transfer löschen

- **target_host**:
  - `jumpserver`: SSH-Verbindungsdetails (host, port, username, use_ssh_agent)
  - `target`: SSH-Verbindungsdetails für target-host
  - `target_folder`: Zielordner auf target-host

### 5. Erste Authentifizierung

**Auf win1:**
```powershell
python win1_upload_monitor.py
```
- Browser öffnet sich automatisch
- Melden Sie sich mit Ihrem Google-Konto an
- Erlauben Sie den Zugriff auf Google Drive
- `token.json` wird automatisch erstellt

**Auf win2:**
```powershell
python win2_download_and_transfer.py
```
- Browser öffnet sich automatisch
- Melden Sie sich mit dem **gleichen** Google-Konto an
- Erlauben Sie den Zugriff auf Google Drive
- `token.json` wird automatisch erstellt

## Verwendung

### win1:
```powershell
python win1_upload_monitor.py
```
- Überwacht den konfigurierten Ordner (z.B. `C:\SYN\Upload`)
- Lädt neue Dateien automatisch zu Google Drive hoch
- Logs: `win1_upload.log`

### win2:
```powershell
python win2_download_and_transfer.py
```
- Prüft Google Drive regelmäßig (Standard: alle 30 Sekunden)
- Lädt neue Dateien herunter nach konfiguriertem Download-Ordner
- Überträgt Dateien per SCP über Jumpserver zu target-host
- Logs: `win2_transfer.log`

**Start-Methoden**: Siehe [docs/02_HOW_TO_START.md](docs/02_HOW_TO_START.md) für Task Scheduler, Services, etc.

## Wichtige Dateien

- `config.json` - Zentrale Konfiguration
- `credentials.json` - Google API Credentials (von Cloud Console, **nicht committen!**)
- `token.json` - Auto-generiert beim ersten Start (nicht committen!)
- `requirements.txt` - Python Dependencies
- `.gitignore` - Schützt sensible Dateien

## Wichtige Konfigurationen

### Google Drive Folder ID finden:
1. Ordner in Google Drive öffnen
2. URL: `https://drive.google.com/drive/folders/FOLDER_ID_HIER`
3. `FOLDER_ID_HIER` kopieren → in `config.json` eintragen

**Wichtig**: Verwenden Sie für win1 und win2 die **gleiche** Folder ID!

### Pageant (SSH-Agent):
- PuTTY installieren → Pageant starten → Keys laden
- `use_ssh_agent: true` in config.json
- Falls Pageant nicht läuft: Fallback auf `key_file`

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` oder `uv pip install --user -r requirements.txt` |
| `Credentials-Datei nicht gefunden` | `credentials.json` im Projektordner? |
| `Google Drive Authentifizierung schlägt fehl` | Prüfen Sie ob Google Drive API aktiviert ist, OAuth consent screen konfiguriert |
| `SSH-Fehler` | Pageant läuft? Key-Pfad in config.json korrekt? SSH-Verbindung manuell testen |
| `Dateien nicht erkannt` | Ordner-Pfade in config.json prüfen, Dateiberechtigungen prüfen |
| `uv nicht erkannt` | `$env:Path = "C:\Users\chuan\.local\bin;$env:Path"` (oder PowerShell neu starten) |
| `Token abgelaufen` | Löschen Sie `token.json` und starten Sie das Skript erneut |

## Test

### Test auf win1:
1. Legen Sie eine Testdatei in den überwachten Ordner
2. Prüfen Sie die Logs (`win1_upload.log`)
3. Prüfen Sie Google Drive - die Datei sollte dort erscheinen

### Test auf win2:
1. Starten Sie `win2_download_and_transfer.py`
2. Das Skript sollte die neue Datei erkennen
3. Datei wird heruntergeladen und zu target-host übertragen
4. Prüfen Sie die Logs (`win2_transfer.log`)

## Detaillierte Dokumentation

Für detaillierte Schritt-für-Schritt Anleitungen mit Screenshots-Beschreibungen siehe:
- [docs/01_SETUP.md](docs/01_SETUP.md) - Vollständige Setup-Anleitung
- [docs/GOOGLE_CREDENTIALS_SETUP.md](docs/GOOGLE_CREDENTIALS_SETUP.md) - Google API Setup Details
- [docs/GOOGLE_DRIVE_SETUP.md](docs/GOOGLE_DRIVE_SETUP.md) - Folder ID finden
- [docs/PAGEANT_SETUP.md](docs/PAGEANT_SETUP.md) - SSH-Agent Setup Details
- [docs/00_ARCHITECTURE.md](docs/00_ARCHITECTURE.md) - Technische Architektur
