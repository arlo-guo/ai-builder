# Wie starte ich die Skripte?

## win1_upload_monitor.py starten

### Voraussetzungen

Bevor Sie das Skript starten, stellen Sie sicher:

1. ✅ Python ist installiert (3.8 oder höher)
2. ✅ Dependencies sind installiert: `pip install -r requirements.txt` oder `uv pip install --user -r requirements.txt`
3. ✅ `credentials.json` ist im Projektordner vorhanden
4. ✅ `config.json` ist korrekt konfiguriert
5. ✅ Der Überwachungsordner existiert (wird automatisch erstellt, falls nicht vorhanden)

---

## Methode 1: Manueller Start (Kommandozeile)

### Windows PowerShell oder Command Prompt

1. **Öffnen Sie PowerShell oder CMD**

2. **Navigieren Sie zum Projektordner**:
   ```powershell
   cd C:\DEV\ai-lab\lernbox_01
   ```

3. **Starten Sie das Skript**:
   ```powershell
   python win1_upload_monitor.py
   ```

   Oder falls `python` nicht funktioniert:
   ```powershell
   python3 win1_upload_monitor.py
   ```
   
   Oder mit vollem Pfad:
   ```powershell
   C:\Python39\python.exe win1_upload_monitor.py
   ```

### Was passiert beim Start?

1. **Konfiguration wird geladen** (`config.json`)
2. **Google Drive Authentifizierung**:
   - Beim **ersten Start**: Browser öffnet sich → Sie melden sich an → `token.json` wird erstellt
   - Bei **weiteren Starts**: Token wird automatisch verwendet
3. **Ordner-Überwachung startet**:
   - Das Skript überwacht den konfigurierten Ordner (z.B. `C:\SYN\Upload`)
   - Neue Dateien werden automatisch erkannt und hochgeladen
4. **Skript läuft kontinuierlich**:
   - Sie sehen Logs in der Konsole
   - Logs werden auch in `win1_upload.log` gespeichert
   - Drücken Sie **Ctrl+C** zum Beenden

### Beispiel-Output:

```
2024-01-15 10:30:15 - __main__ - INFO - Google Drive Authentifizierung erfolgreich
2024-01-15 10:30:15 - __main__ - INFO - Überwache Ordner: C:\SYN\Upload
2024-01-15 10:30:15 - __main__ - INFO - Drücken Sie Ctrl+C zum Beenden...
```

---

## Methode 2: Automatischer Start (Windows Task Scheduler)

### Schritt-für-Schritt Anleitung

#### Schritt 1: Task Scheduler öffnen

1. Drücken Sie **Windows + R**
2. Geben Sie ein: `taskschd.msc`
3. Drücken Sie **Enter**

#### Schritt 2: Neue Aufgabe erstellen

1. Klicken Sie rechts auf **"Create Basic Task..."** oder **"Create Task..."**

2. **General Tab**:
   - **Name**: `File Transfer Upload Monitor`
   - **Description**: `Überwacht Ordner und lädt Dateien zu Google Drive hoch`
   - ✅ **Run whether user is logged on or not** (optional)
   - ✅ **Run with highest privileges** (optional, falls nötig)

3. **Triggers Tab** (Trigger hinzufügen):
   - Klicken Sie auf **"New..."**
   - **Begin the task**: Wählen Sie eine Option:
     - ✅ **At startup** - Startet beim Windows-Start
     - ✅ **At log on** - Startet bei Anmeldung (empfohlen)
     - ✅ **On a schedule** - Zu bestimmten Zeiten
   - Klicken Sie auf **OK**

4. **Actions Tab** (Aktion hinzufügen):
   - Klicken Sie auf **"New..."**
   - **Action**: `Start a program`
   - **Program/script**: 
     ```
     python
     ```
     Oder vollständiger Pfad:
     ```
     C:\Python39\python.exe
     ```
   - **Add arguments (optional)**:
     ```
     C:\DEV\ai-lab\lernbox_01\win1_upload_monitor.py
     ```
   - **Start in (optional)**:
     ```
     C:\DEV\ai-lab\lernbox_01
     ```
   - Klicken Sie auf **OK**

5. **Conditions Tab** (optional):
   - ✅ **Start the task only if the computer is on AC power** (deaktivieren, falls auf Laptop)
   - ✅ **Wake the computer to run this task** (optional)

6. **Settings Tab** (optional):
   - ✅ **Allow task to be run on demand**
   - ✅ **Run task as soon as possible after a scheduled start is missed**
   - ✅ **If the task fails, restart every**: `1 minute` (max 3 attempts)

7. Klicken Sie auf **OK**

8. **Passwort eingeben** (falls "Run whether user is logged on or not" aktiviert)

#### Schritt 3: Task testen

1. Rechtsklick auf die erstellte Task
2. Wählen Sie **"Run"**
3. Prüfen Sie, ob das Skript startet

#### Schritt 4: Task-Status prüfen

- **Task Scheduler Library** → Ihre Task → **"Last Run Result"** sollte "The operation completed successfully" zeigen
- Prüfen Sie die Log-Datei: `C:\DEV\ai-lab\lernbox_01\win1_upload.log`

---

## Methode 3: Als Windows Service (Erweitert)

Für fortgeschrittene Nutzer: Das Skript kann als Windows Service laufen. Dafür benötigen Sie zusätzliche Tools wie `NSSM` (Non-Sucking Service Manager) oder `pywin32`.

### Mit NSSM (Empfohlen)

1. **NSSM herunterladen**: https://nssm.cc/download
2. **Service installieren**:
   ```powershell
   nssm install FileTransferUploadMonitor
   ```
3. **Konfiguration**:
   - **Path**: `C:\Python39\python.exe`
   - **Startup directory**: `C:\DEV\ai-lab\lernbox_01`
   - **Arguments**: `win1_upload_monitor.py`
4. **Service starten**:
   ```powershell
   nssm start FileTransferUploadMonitor
   ```

---

## Methode 4: Batch-Datei erstellen (Einfach)

Erstellen Sie eine `.bat` Datei für einfachen Start:

### win1_start.bat

```batch
@echo off
cd /d C:\DEV\ai-lab\lernbox_01
python win1_upload_monitor.py
pause
```

**Verwendung**:
- Doppelklick auf `win1_start.bat`
- Oder: Rechtsklick → "Send to" → "Desktop (create shortcut)"

---

## Verhalten beim Start

### Beim ersten Start:

1. ✅ Konfiguration wird geladen
2. ✅ Browser öffnet sich automatisch für Google-Authentifizierung
3. ✅ Sie melden sich mit Google-Konto an
4. ✅ `token.json` wird erstellt
5. ✅ Ordner-Überwachung startet

### Bei weiteren Starts:

1. ✅ Konfiguration wird geladen
2. ✅ `token.json` wird automatisch verwendet (kein Browser nötig)
3. ✅ Ordner-Überwachung startet sofort

---

## Skript beenden

### Manuell gestartet:
- Drücken Sie **Ctrl+C** in der Konsole
- Oder schließen Sie das Konsolen-Fenster

### Automatisch gestartet (Task Scheduler):
- Öffnen Sie **Task Scheduler**
- Rechtsklick auf die Task → **"End"**

### Als Service:
```powershell
nssm stop FileTransferUploadMonitor
```

---

## Prüfen ob Skript läuft

### Methode 1: Task Manager
1. Öffnen Sie **Task Manager** (Ctrl+Shift+Esc)
2. Prüfen Sie, ob `python.exe` läuft
3. Prüfen Sie die Kommandozeile: sollte `win1_upload_monitor.py` enthalten

### Methode 2: Log-Datei prüfen
```powershell
Get-Content C:\DEV\ai-lab\lernbox_01\win1_upload.log -Tail 20
```

### Methode 3: Test-Datei erstellen
1. Legen Sie eine Testdatei in den Überwachungsordner
2. Prüfen Sie, ob sie zu Google Drive hochgeladen wird

---

## Troubleshooting

### Problem: "python is not recognized"
**Lösung**:
- Prüfen Sie, ob Python installiert ist: `python --version`
- Fügen Sie Python zum PATH hinzu
- Oder verwenden Sie den vollständigen Pfad: `C:\Python39\python.exe`

### Problem: "Module not found"
**Lösung**:
```powershell
pip install -r requirements.txt
```

### Problem: "Credentials-Datei nicht gefunden"
**Lösung**:
- Stellen Sie sicher, dass `credentials.json` im Projektordner liegt
- Prüfen Sie den Pfad in `config.json`

### Problem: Task startet nicht automatisch
**Lösung**:
- Prüfen Sie Task Scheduler → Ihre Task → "Last Run Result"
- Prüfen Sie, ob der Trigger korrekt konfiguriert ist
- Prüfen Sie, ob Python-Pfad korrekt ist

### Problem: Browser öffnet sich nicht (bei automatischem Start)
**Lösung**:
- Bei Task Scheduler: Aktivieren Sie "Run only when user is logged on"
- Oder: Authentifizieren Sie sich manuell einmal, dann wird `token.json` gespeichert

---

## Empfehlung

**Für normale Nutzung**: 
- ✅ **Task Scheduler** mit Trigger "At log on"
- ✅ Skript startet automatisch bei Windows-Anmeldung
- ✅ Läuft im Hintergrund

**Für Tests/Entwicklung**:
- ✅ **Manueller Start** über Kommandozeile
- ✅ Sie sehen die Logs direkt

---

## Zusammenfassung

| Methode | Vorteil | Nachteil |
|---------|---------|----------|
| **Manuell** | Einfach, sieht Logs direkt | Muss jedes Mal manuell starten |
| **Task Scheduler** | Startet automatisch | Etwas komplexer zu konfigurieren |
| **Service** | Läuft immer, auch ohne Login | Komplexeste Konfiguration |
| **Batch-Datei** | Einfacher Doppelklick-Start | Muss manuell gestartet werden |

**Empfohlen**: Task Scheduler mit "At log on" Trigger

