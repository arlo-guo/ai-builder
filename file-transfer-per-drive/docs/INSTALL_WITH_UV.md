# Installation mit uv (Ohne Admin-Rechte)

## Was ist uv?

**uv** ist ein moderner, extrem schneller Python-Package-Manager von Astral (den Machern von ruff). Es ist eine moderne Alternative zu pip und kann Pakete **lokal im Benutzer-Bereich** installieren, ohne Windows-Admin-Rechte.

### Vorteile von uv:

- ✅ **Schneller** als pip (bis zu 100x schneller)
- ✅ **Lokale Installation** ohne Admin-Rechte
- ✅ **Automatisches Virtual Environment Management**
- ✅ **Bessere Dependency Resolution**
- ✅ **Moderner und aktiv entwickelt**

---

## Installation von uv

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Oder mit winget (Windows 11):
```powershell
winget install --id=astral-sh.uv -e
```

Oder mit pip (falls Python bereits installiert):
```powershell
pip install uv
```

### Nach der Installation

Starten Sie PowerShell neu oder führen Sie aus:
```powershell
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
```

Prüfen Sie die Installation:
```powershell
uv --version
```

---

## Installation der Dependencies mit uv

### Methode 1: Mit Virtual Environment (Empfohlen)

uv erstellt automatisch ein Virtual Environment:

```powershell
cd C:\DEV\ai-lab\lernbox_01

# Installiere alle Dependencies in einem Virtual Environment
uv pip install -r requirements.txt
```

Oder mit explizitem Virtual Environment:

```powershell
cd C:\DEV\ai-lab\lernbox_01

# Erstelle Virtual Environment
uv venv

# Aktiviere Virtual Environment
.\venv\Scripts\Activate.ps1

# Installiere Dependencies
uv pip install -r requirements.txt
```

### Methode 2: Lokale Installation (User-Scope, ohne Virtual Environment)

Installation direkt in den Benutzer-Bereich (ohne Admin):

```powershell
cd C:\DEV\ai-lab\lernbox_01

# Installiere lokal für den aktuellen Benutzer
uv pip install --user -r requirements.txt
```

Oder einzeln:

```powershell
uv pip install --user google-api-python-client
uv pip install --user google-auth-httplib2
uv pip install --user google-auth-oauthlib
uv pip install --user watchdog
uv pip install --user paramiko
uv pip install --user scp
```

### Methode 3: Mit uv Projekt-Management (Modernste Methode)

uv kann auch Projekte direkt verwalten:

```powershell
cd C:\DEV\ai-lab\lernbox_01

# Initialisiere uv Projekt (erstellt pyproject.toml)
uv init --no-readme

# Installiere Dependencies aus requirements.txt
uv pip install -r requirements.txt
```

---

## Verwendung nach Installation

### Mit Virtual Environment:

```powershell
# Aktiviere Virtual Environment
.\venv\Scripts\Activate.ps1

# Starte Skript
python win1_upload_monitor.py
```

### Mit lokaler Installation (--user):

```powershell
# Direkt starten (Pakete sind im User-Bereich)
python win1_upload_monitor.py
```

---

## uv vs pip Vergleich

| Feature | pip | uv |
|---------|-----|-----|
| Geschwindigkeit | Standard | **100x schneller** |
| Lokale Installation | `pip install --user` | `uv pip install --user` |
| Virtual Environment | Manuell | **Automatisch** |
| Dependency Resolution | Gut | **Besser** |
| Admin-Rechte nötig? | Manchmal | **Nie** |

---

## Komplette Installations-Anleitung

### Schritt 1: uv installieren

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Schritt 2: Projektordner öffnen

```powershell
cd C:\DEV\ai-lab\lernbox_01
```

### Schritt 3: Dependencies installieren

**Option A: Mit Virtual Environment (Empfohlen)**
```powershell
uv venv
.\venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

**Option B: Lokal ohne Virtual Environment**
```powershell
uv pip install --user -r requirements.txt
```

### Schritt 4: Installation prüfen

```powershell
uv pip list
```

Oder mit Python:
```powershell
python -c "import watchdog; print('✅ watchdog OK')"
python -c "import paramiko; print('✅ paramiko OK')"
```

### Schritt 5: Skript starten

```powershell
python win1_upload_monitor.py
```

---

## uv Projekt-Struktur (Optional)

Falls Sie uv für Projekt-Management verwenden möchten:

### pyproject.toml erstellen

uv kann automatisch eine `pyproject.toml` erstellen:

```powershell
uv init --no-readme
```

Dann können Sie Dependencies hinzufügen:

```powershell
uv add google-api-python-client
uv add watchdog
uv add paramiko
uv add scp
```

Dies erstellt automatisch `pyproject.toml` und `uv.lock`.

### Mit pyproject.toml installieren

```powershell
uv sync
```

---

## Troubleshooting

### Problem: "uv is not recognized"

**Lösung**: 
- Prüfen Sie, ob uv installiert ist: `uv --version`
- Fügen Sie uv zum PATH hinzu oder starten Sie PowerShell neu
- Installieren Sie uv erneut

### Problem: "Permission denied"

**Lösung**: 
- Verwenden Sie `--user` Flag: `uv pip install --user -r requirements.txt`
- Oder verwenden Sie Virtual Environment: `uv venv`

### Problem: Pakete werden nicht gefunden

**Lösung**:
- Prüfen Sie, ob Virtual Environment aktiviert ist (falls verwendet)
- Prüfen Sie Installation: `uv pip list`
- Installieren Sie erneut: `uv pip install --user -r requirements.txt`

### Problem: Konflikt mit pip-installierten Paketen

**Lösung**:
- Verwenden Sie Virtual Environment für saubere Trennung
- Oder deinstallieren Sie pip-Versionen: `pip uninstall <paket>`

---

## Migration von pip zu uv

Falls Sie bereits mit pip installiert haben:

### Option 1: Beide parallel verwenden
- uv und pip können parallel existieren
- Verwenden Sie einfach `uv pip` statt `pip`

### Option 2: Komplett zu uv wechseln
```powershell
# Deinstalliere pip-Versionen (optional)
pip uninstall -r requirements.txt

# Installiere mit uv
uv pip install --user -r requirements.txt
```

---

## Best Practices mit uv

1. **Verwenden Sie Virtual Environment** für Projekt-Isolation:
   ```powershell
   uv venv
   .\venv\Scripts\Activate.ps1
   uv pip install -r requirements.txt
   ```

2. **Für lokale Installation ohne Admin**:
   ```powershell
   uv pip install --user -r requirements.txt
   ```

3. **Prüfen Sie Installation regelmäßig**:
   ```powershell
   uv pip list
   ```

4. **Upgrade Pakete**:
   ```powershell
   uv pip install --upgrade -r requirements.txt
   ```

---

## Zusammenfassung

### Schnellstart mit uv:

```powershell
# 1. uv installieren
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Zum Projektordner
cd C:\DEV\ai-lab\lernbox_01

# 3. Dependencies installieren (lokal, ohne Admin)
uv pip install --user -r requirements.txt

# 4. Skript starten
python win1_upload_monitor.py
```

### Mit Virtual Environment:

```powershell
cd C:\DEV\ai-lab\lernbox_01
uv venv
.\venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
python win1_upload_monitor.py
```

---

## Weitere Ressourcen

- **uv Dokumentation**: https://docs.astral.sh/uv/
- **uv GitHub**: https://github.com/astral-sh/uv
- **Installation Guide**: https://docs.astral.sh/uv/getting-started/installation/

---

## Vorteile für Ihr Projekt

✅ **Keine Admin-Rechte nötig** - Installation im User-Bereich  
✅ **Schneller** - Installation dauert Sekunden statt Minuten  
✅ **Modern** - Aktive Entwicklung, bessere Fehlerbehandlung  
✅ **Kompatibel** - Funktioniert mit bestehenden requirements.txt  

