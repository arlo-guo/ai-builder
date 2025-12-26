# Setup-Anleitung - Detailliert

> **Hinweis**: Für eine kompakte Anleitung siehe [QUICK_START.md](../QUICK_START.md). Diese Anleitung enthält detaillierte Schritt-für-Schritt Beschreibungen mit Screenshots-Hinweisen.

## Schritt 1: Python-Umgebung einrichten

### Python installieren

1. Laden Sie Python 3.8 oder höher von [python.org](https://www.python.org/downloads/) herunter
2. Bei Installation **"Add Python to PATH"** aktivieren
3. Installation abschließen

### Dependencies installieren

**Option A: Mit pip**
```bash
pip install -r requirements.txt
```

**Option B: Mit uv (ohne Admin-Rechte)**
```bash
uv pip install --user -r requirements.txt
```

Siehe [INSTALL_DEPENDENCIES.md](INSTALL_DEPENDENCIES.md) oder [INSTALL_WITH_UV.md](INSTALL_WITH_UV.md) für Details und Troubleshooting.

## Schritt 2: Google Drive API einrichten

### 2.1 Google Cloud Console Projekt erstellen

1. Gehen Sie zu [Google Cloud Console](https://console.cloud.google.com/)
2. Klicken Sie oben auf das **Projekt-Dropdown** (neben "Google Cloud")
3. Klicken Sie auf **"New Project"** (oder wählen Sie ein bestehendes Projekt)
4. Geben Sie einen Projektnamen ein, z.B. "File Transfer Tool"
5. Klicken Sie auf **"Create"**
6. Warten Sie, bis das Projekt erstellt ist (kann einige Sekunden dauern)
7. Notieren Sie sich die Projekt-ID

### 2.2 Google Drive API aktivieren

1. Im Google Cloud Console Dashboard:
   - Klicken Sie auf das **☰ Menü** (oben links)
   - Navigieren Sie zu **"APIs & Services"** > **"Library"**
2. Suchen Sie nach **"Google Drive API"**:
   - Geben Sie "Google Drive API" in die Suchleiste ein
   - Klicken Sie auf **"Google Drive API"** in den Suchergebnissen
3. Aktivieren Sie die API:
   - Klicken Sie auf den Button **"Enable"** (oben)
   - Warten Sie, bis die API aktiviert ist

### 2.3 OAuth Consent Screen konfigurieren (einmalig)

**WICHTIG**: Dies muss vor dem Erstellen der Credentials gemacht werden!

1. Navigieren Sie zu **"APIs & Services"** > **"OAuth consent screen"**
2. Wählen Sie **"External"** (für persönliche/Test-Nutzung)
   - Klicken Sie auf **"Create"**
3. Füllen Sie die erforderlichen Felder aus:
   - **App name**: z.B. "File Transfer Tool"
   - **User support email**: Ihre E-Mail-Adresse
   - **Developer contact information**: Ihre E-Mail-Adresse
   - Klicken Sie auf **"Save and Continue"**
4. **Scopes** (kann übersprungen werden):
   - Klicken Sie auf **"Save and Continue"**
5. **Test users** (wichtig für Testphase):
   - Klicken Sie auf **"Add Users"**
   - Geben Sie Ihre E-Mail-Adresse ein
   - Klicken Sie auf **"Add"**
   - Klicken Sie auf **"Save and Continue"**
6. **Summary**:
   - Klicken Sie auf **"Back to Dashboard"**

### 2.4 OAuth 2.0 Credentials erstellen

1. Navigieren Sie zu **"APIs & Services"** > **"Credentials"**
2. Klicken Sie auf **"+ CREATE CREDENTIALS"** (oben)
   - Wählen Sie **"OAuth client ID"**
3. Falls Sie aufgefordert werden, den Consent Screen zu konfigurieren:
   - Folgen Sie den Anweisungen von Schritt 2.3
4. **Application type auswählen**:
   - Wählen Sie **"Desktop app"**
   - Geben Sie einen **Name** ein, z.B. "File Transfer Tool"
   - Klicken Sie auf **"Create"**
5. **Credentials herunterladen**:
   - Ein Popup-Fenster erscheint mit **Client ID** und **Client Secret**
   - Klicken Sie auf **"DOWNLOAD JSON"** (rechts unten)
   - Die Datei wird als `client_secret_XXXXX.json` heruntergeladen
6. **Datei umbenennen**:
   - Benennen Sie die heruntergeladene Datei um zu: **`credentials.json`**
   - Verschieben Sie die Datei in Ihren Projektordner (wo `config.json` liegt)

### 2.5 Google Drive Ordner erstellen und ID ermitteln

1. Erstellen Sie einen Ordner in Google Drive
2. Öffnen Sie den Ordner (Doppelklick)
3. Die Ordner-ID finden Sie in der URL:
   ```
   https://drive.google.com/drive/folders/FOLDER_ID_HIER
   ```
4. Kopieren Sie die `FOLDER_ID_HIER` und tragen Sie sie in `config.json` ein

**Wichtig**: Verwenden Sie für win1 und win2 den **gleichen** Google Drive Ordner!

**Detaillierte Anleitung**: Siehe [GOOGLE_CREDENTIALS_SETUP.md](GOOGLE_CREDENTIALS_SETUP.md) und [GOOGLE_DRIVE_SETUP.md](GOOGLE_DRIVE_SETUP.md)

## Schritt 3: SSH/SCP Zugriff einrichten

### Option A: Mit Pageant (SSH-Agent) - Empfohlen für Windows

**Sie verwenden Pageant?** Siehe detaillierte Anleitung in [PAGEANT_SETUP.md](PAGEANT_SETUP.md)

Kurzanleitung:
1. Installieren Sie PuTTY (enthält Pageant)
2. Starten Sie Pageant
3. Laden Sie Ihre SSH-Keys in Pageant
4. In `config.json`: Setzen Sie `"use_ssh_agent": true`

Das Skript verwendet automatisch Pageant, wenn es läuft!

### Option B: Mit SSH-Key-Dateien

#### 3.1 SSH-Key generieren (falls noch nicht vorhanden)

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

#### 3.2 SSH-Key zu Jumpserver kopieren

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub jumpuser@jumpserver.example.com
```

#### 3.3 SSH-Key zu target-host kopieren (über Jumpserver)

```bash
ssh -t jumpuser@jumpserver.example.com "ssh-copy-id -i ~/.ssh/id_rsa.pub targetuser@target-host.example.com"
```

#### 3.4 Test der Verbindung

```bash
# Test Jumpserver
ssh jumpuser@jumpserver.example.com

# Test target-host über Jumpserver
ssh -J jumpuser@jumpserver.example.com targetuser@target-host.example.com
```

## Schritt 4: Konfiguration anpassen

Bearbeiten Sie `config.json`:

1. **win1 Konfiguration**:
   - `watch_folder`: Ordner auf win1, der überwacht wird (z.B. `C:\SYN\Upload`)
   - `google_drive_folder_id`: ID des Google Drive Ordners (aus Schritt 2.5)
   - `delete_after_upload`: `true` = Datei nach Upload löschen
   - `move_after_upload`: `true` = Datei nach Upload verschieben
   - `move_to_folder`: Zielordner für verschobene Dateien

2. **win2 Konfiguration**:
   - `download_folder`: Ordner auf win2 für Downloads (z.B. `C:\SYN\Download`)
   - `google_drive_folder_id`: ID des Google Drive Ordners (gleiche wie win1!)
   - `check_interval_seconds`: Wie oft Google Drive geprüft wird (Standard: 30)
   - `delete_after_transfer`: `true` = Datei nach Transfer löschen

3. **target_host Konfiguration**:
   - `jumpserver`: SSH-Verbindungsdetails für Jumpserver
     - `host`: Hostname oder IP
     - `port`: SSH-Port (Standard: 22)
     - `username`: Benutzername
     - `use_ssh_agent`: `true` wenn Pageant verwendet wird
     - `key_file`: Pfad zur SSH-Key-Datei (Fallback)
     - `password`: Passwort (nur wenn kein Key/Pageant)
   - `target`: SSH-Verbindungsdetails für target-host
     - `host`: Hostname oder IP
     - `port`: SSH-Port
     - `username`: Benutzername
     - `use_ssh_agent`: `true` wenn Pageant verwendet wird
     - `key_file`: Pfad zur SSH-Key-Datei (Fallback)
     - `target_folder`: Zielordner auf target-host (z.B. `/home/user/transfer`)

4. **google_drive Konfiguration**:
   - `credentials_file`: Pfad zu `credentials.json` (Standard: `credentials.json`)
   - `token_file`: Pfad wo Token gespeichert wird (Standard: `token.json`)
   - `scopes`: API-Berechtigungen (Standard: `["https://www.googleapis.com/auth/drive.file"]`)

## Schritt 5: Erste Authentifizierung

### Auf win1:
```bash
python win1_upload_monitor.py
```
- Beim ersten Start öffnet sich ein Browser-Fenster
- Sie werden zu Google weitergeleitet
- Melden Sie sich mit Ihrem Google-Konto an
- Sie sehen eine Warnung: "Google hasn't verified this app"
  - Klicken Sie auf **"Advanced"** → **"Go to File Transfer Tool (unsafe)"**
  - Klicken Sie auf **"Allow"** um den Zugriff zu erlauben
- Token wird automatisch in `token.json` gespeichert

### Auf win2:
```bash
python win2_download_and_transfer.py
```
- Beim ersten Start öffnet sich ein Browser-Fenster
- Melden Sie sich mit dem **gleichen** Google-Konto an
- Erlauben Sie den Zugriff auf Google Drive
- Token wird automatisch in `token.json` gespeichert

## Schritt 6: Test

### Test auf win1:
1. Legen Sie eine Testdatei in den überwachten Ordner (aus `config.json`)
2. Prüfen Sie die Logs (`win1_upload.log`)
3. Prüfen Sie Google Drive - die Datei sollte dort erscheinen

### Test auf win2:
1. Starten Sie `win2_download_and_transfer.py`
2. Das Skript sollte die neue Datei erkennen (beim nächsten Check-Intervall)
3. Datei wird heruntergeladen und zu target-host übertragen
4. Prüfen Sie die Logs (`win2_transfer.log`)
5. Prüfen Sie, ob die Datei auf target-host angekommen ist

## Fehlerbehebung

### Google Drive Authentifizierung schlägt fehl
- Prüfen Sie ob `credentials.json` vorhanden ist
- Prüfen Sie ob Google Drive API aktiviert ist
- Prüfen Sie OAuth consent screen Konfiguration
- Prüfen Sie ob Sie als Test-User hinzugefügt wurden

### SSH-Verbindung schlägt fehl
- Prüfen Sie SSH-Key-Pfade in `config.json`
- Testen Sie SSH-Verbindung manuell
- Prüfen Sie Firewall-Einstellungen
- Prüfen Sie ob Pageant läuft (falls `use_ssh_agent: true`)

### Dateien werden nicht erkannt
- Prüfen Sie ob Ordner-Pfade korrekt sind
- Prüfen Sie Dateiberechtigungen
- Prüfen Sie Logs auf Fehlermeldungen
- Prüfen Sie ob Dateien vollständig geschrieben sind (warten Sie 2-3 Sekunden)

## Automatischer Start (Optional)

### Windows Task Scheduler (win1)
1. Öffnen Sie Task Scheduler (`taskschd.msc`)
2. Klicken Sie rechts auf **"Create Basic Task..."** oder **"Create Task..."**
3. **General Tab**:
   - **Name**: `File Transfer Upload Monitor`
   - **Description**: `Überwacht Ordner und lädt Dateien zu Google Drive hoch`
4. **Triggers Tab**:
   - Klicken Sie auf **"New..."**
   - **Begin the task**: Wählen Sie **"At log on"** (bei Anmeldung)
5. **Actions Tab**:
   - Klicken Sie auf **"New..."**
   - **Action**: `Start a program`
   - **Program/script**: `python`
   - **Add arguments**: `C:\Pfad\zum\win1_upload_monitor.py`
   - **Start in**: `C:\Pfad\zum\Projekt`
6. Klicken Sie auf **OK**

### Windows Task Scheduler (win2)
1. Öffnen Sie Task Scheduler
2. Erstellen Sie eine neue Aufgabe (wie oben)
3. **Name**: `File Transfer Download and Transfer`
4. **Arguments**: `C:\Pfad\zum\win2_download_and_transfer.py`

Siehe [02_HOW_TO_START.md](02_HOW_TO_START.md) für detaillierte Anleitung mit Screenshots-Beschreibungen.
