# Dependencies Installation - Schritt für Schritt

## Übersicht

Dieses Projekt benötigt mehrere Python-Pakete. Sie werden mit **pip** (Python Package Installer) installiert.

---

## Installations-Tool: pip

**pip** ist der Standard-Package-Manager für Python und wird normalerweise automatisch mit Python installiert.

### Prüfen ob pip installiert ist:

```powershell
pip --version
```

Falls pip nicht installiert ist, installieren Sie es:
```powershell
python -m ensurepip --upgrade
```

---

## Schnell-Installation (Empfohlen)

### Einfachste Methode - Alle Dependencies auf einmal:

```powershell
cd C:\DEV\ai-lab\lernbox_01
pip install -r requirements.txt
```

Das installiert alle benötigten Pakete automatisch!

---

## Detaillierte Installations-Anleitung

### Schritt 1: Terminal öffnen

1. Öffnen Sie **PowerShell** oder **Command Prompt**
2. Navigieren Sie zum Projektordner:
   ```powershell
   cd C:\DEV\ai-lab\lernbox_01
   ```

### Schritt 2: Dependencies installieren

#### Option A: Alle auf einmal (Empfohlen)

```powershell
pip install -r requirements.txt
```

#### Option B: Einzeln installieren

Falls Sie Probleme haben, können Sie auch einzeln installieren:

```powershell
# Google Drive API
pip install google-api-python-client
pip install google-auth-httplib2
pip install google-auth-oauthlib

# File System Monitoring
pip install watchdog

# SSH/SCP Transfer
pip install paramiko
pip install scp
```

### Schritt 3: Installation prüfen

Prüfen Sie, ob alle Pakete installiert sind:

```powershell
pip list
```

Sie sollten folgende Pakete sehen:
- `google-api-python-client`
- `google-auth-httplib2`
- `google-auth-oauthlib`
- `watchdog`
- `paramiko`
- `scp`

---

## Liste aller Dependencies

### Für win1_upload_monitor.py:

| Paket | Version | Zweck |
|-------|---------|-------|
| `google-api-python-client` | >=2.100.0 | Google Drive API Client |
| `google-auth-httplib2` | >=0.1.1 | HTTP-Transport für Google Auth |
| `google-auth-oauthlib` | >=1.1.0 | OAuth 2.0 Flow |
| `watchdog` | >=3.0.0 | Dateisystem-Überwachung |

### Für win2_download_and_transfer.py:

| Paket | Version | Zweck |
|-------|---------|-------|
| `google-api-python-client` | >=2.100.0 | Google Drive API Client |
| `google-auth-httplib2` | >=0.1.1 | HTTP-Transport für Google Auth |
| `google-auth-oauthlib` | >=1.1.0 | OAuth 2.0 Flow |
| `paramiko` | >=3.3.1 | SSH-Client für SCP |
| `scp` | >=0.14.5 | SCP-Protokoll |

### Standard-Bibliotheken (müssen NICHT installiert werden):

- `os` - Betriebssystem-Interfaces
- `json` - JSON-Verarbeitung
- `time` - Zeit-Funktionen
- `logging` - Logging-System
- `shutil` - Datei-Operationen
- `pathlib` - Pfad-Verarbeitung (Python 3.4+)
- `io` - Input/Output
- `pickle` - Objekt-Serialisierung

---

## Installation mit Virtual Environment (Empfohlen für fortgeschrittene Nutzer)

Ein Virtual Environment isoliert die Dependencies für dieses Projekt.

### Schritt 1: Virtual Environment erstellen

```powershell
cd C:\DEV\ai-lab\lernbox_01
python -m venv venv
```

### Schritt 2: Virtual Environment aktivieren

```powershell
.\venv\Scripts\Activate.ps1
```

Falls PowerShell-Skripte blockiert sind:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

Oder mit CMD:
```cmd
venv\Scripts\activate.bat
```

### Schritt 3: Dependencies installieren

```powershell
pip install -r requirements.txt
```

### Schritt 4: Virtual Environment deaktivieren (später)

```powershell
deactivate
```

**Hinweis**: Bei Verwendung eines Virtual Environment müssen Sie es jedes Mal aktivieren, bevor Sie die Skripte starten!

---

## Troubleshooting

### Problem: "pip is not recognized"

**Lösung 1**: Python zum PATH hinzufügen
- Öffnen Sie "Umgebungsvariablen" in Windows
- Fügen Sie Python-Installationspfad zum PATH hinzu

**Lösung 2**: Verwenden Sie `python -m pip`:
```powershell
python -m pip install -r requirements.txt
```

### Problem: "Permission denied" oder "Access denied"

**Lösung**: Installieren Sie mit Administrator-Rechten:
1. Rechtsklick auf PowerShell → "Run as Administrator"
2. Dann `pip install -r requirements.txt` ausführen

Oder installieren Sie für den aktuellen Benutzer:
```powershell
pip install --user -r requirements.txt
```

### Problem: "ModuleNotFoundError" nach Installation

**Lösung 1**: Prüfen Sie, ob Sie das richtige Python verwenden:
```powershell
python --version
which python
```

**Lösung 2**: Installieren Sie für das richtige Python:
```powershell
python -m pip install -r requirements.txt
```

**Lösung 3**: Prüfen Sie, ob Pakete installiert sind:
```powershell
pip list | findstr watchdog
pip list | findstr paramiko
```

### Problem: "Failed to build wheel"

**Lösung**: Installieren Sie Build-Tools:
```powershell
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Problem: "SSL Certificate" Fehler

**Lösung**: Temporär SSL-Verifizierung deaktivieren (nur wenn nötig):
```powershell
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Problem: Konflikt mit anderen Python-Projekten

**Lösung**: Verwenden Sie ein Virtual Environment (siehe oben)

---

## Installation prüfen

### Test 1: Import-Test

Erstellen Sie eine Test-Datei `test_imports.py`:

```python
try:
    from watchdog.observers import Observer
    print("✅ watchdog OK")
except ImportError as e:
    print(f"❌ watchdog FEHLER: {e}")

try:
    from google.oauth2.credentials import Credentials
    print("✅ google-auth OK")
except ImportError as e:
    print(f"❌ google-auth FEHLER: {e}")

try:
    from googleapiclient.discovery import build
    print("✅ google-api-python-client OK")
except ImportError as e:
    print(f"❌ google-api-python-client FEHLER: {e}")

try:
    import paramiko
    print("✅ paramiko OK")
except ImportError as e:
    print(f"❌ paramiko FEHLER: {e}")

try:
    from scp import SCPClient
    print("✅ scp OK")
except ImportError as e:
    print(f"❌ scp FEHLER: {e}")

print("\n✅ Alle Dependencies installiert!" if True else "")
```

Führen Sie aus:
```powershell
python test_imports.py
```

### Test 2: Skript starten

```powershell
python win1_upload_monitor.py
```

Falls keine ModuleNotFoundError erscheint, sind alle Dependencies installiert!

---

## Upgrade vorhandener Pakete

Falls Pakete bereits installiert sind, aber veraltet:

```powershell
pip install --upgrade -r requirements.txt
```

Oder einzeln:
```powershell
pip install --upgrade google-api-python-client
pip install --upgrade watchdog
pip install --upgrade paramiko
```

---

## Deinstallation (falls nötig)

Falls Sie Pakete entfernen möchten:

```powershell
pip uninstall -r requirements.txt
```

Oder einzeln:
```powershell
pip uninstall watchdog
pip uninstall paramiko
# etc.
```

---

## Zusammenfassung

### Schnellstart:

```powershell
cd C:\DEV\ai-lab\lernbox_01
pip install -r requirements.txt
```

### Benötigte Pakete:

- ✅ `google-api-python-client` - Google Drive API
- ✅ `google-auth-httplib2` - HTTP Transport
- ✅ `google-auth-oauthlib` - OAuth 2.0
- ✅ `watchdog` - Dateisystem-Überwachung
- ✅ `paramiko` - SSH-Client
- ✅ `scp` - SCP-Protokoll

### Installations-Tool:

**pip** (Python Package Installer) - wird mit Python mitgeliefert

---

## Nächste Schritte

Nach erfolgreicher Installation:

1. ✅ Prüfen Sie `credentials.json` ist vorhanden
2. ✅ Prüfen Sie `config.json` ist korrekt konfiguriert
3. ✅ Starten Sie das Skript: `python win1_upload_monitor.py`

