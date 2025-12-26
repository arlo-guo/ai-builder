# Architektur-Übersicht

## Workflow-Diagramm

```
┌─────────────┐
│    win1     │
│  (Windows)  │
│             │
│  Watchdog   │───┐
│  Monitor    │   │
└─────────────┘   │
                  │ (1) Datei erkannt
                  │
                  ▼
         ┌─────────────────┐
         │  Google Drive   │
         │  (Cloud)        │
         │                 │
         │  Shared Folder  │
         └─────────────────┘
                  │
                  │ (2) Neue Datei
                  │
                  ▼
┌─────────────┐   │
│    win2     │   │
│  (Windows)  │◄──┘
│             │
│  Monitor    │───┐
│  Download   │   │
└─────────────┘   │
                  │ (3) SCP Transfer
                  │
                  ▼
         ┌─────────────────┐
         │  Jumpserver     │
         │  (SSH Gateway)  │
         └─────────────────┘
                  │
                  │ (4) SSH Tunnel
                  │
                  ▼
         ┌─────────────────┐
         │  target-host    │
         │  (Linux)        │
         │                 │
         │  /target/folder │
         └─────────────────┘
```

## Komponenten

### 1. win1_upload_monitor.py

**Aufgabe**: Überwacht lokalen Ordner und lädt Dateien zu Google Drive hoch

**Technologien**:
- `watchdog`: Dateisystem-Überwachung
- `google-api-python-client`: Google Drive API
- `google-auth-oauthlib`: OAuth 2.0 Authentifizierung

**Funktionsweise**:
1. Überwacht konfigurierten Ordner mit `watchdog.Observer`
2. Erkennt neue Dateien via `FileSystemEventHandler`
3. Prüft ob Datei vollständig geschrieben ist
4. Lädt Datei zu Google Drive hoch
5. Führt Post-Upload-Aktion aus (löschen/verschieben)

**Ausgabe**: Datei in Google Drive

### 2. win2_download_and_transfer.py

**Aufgabe**: Überwacht Google Drive, lädt Dateien herunter und überträgt sie zu target-host

**Technologien**:
- `google-api-python-client`: Google Drive API
- `paramiko`: SSH-Verbindungen
- `scp`: SCP-Transfer

**Funktionsweise**:
1. Prüft regelmäßig Google Drive auf neue Dateien
2. Lädt neue Dateien herunter
3. Erstellt SSH-Verbindung zu Jumpserver
4. Erstellt SSH-Tunnel zu target-host über Jumpserver
5. Überträgt Datei per SCP zu target-host
6. Markiert Datei als verarbeitet
7. Löscht lokale Datei (optional)

**Ausgabe**: Datei auf target-host

### 3. config.json

**Aufgabe**: Zentrale Konfiguration aller Parameter

**Sektionen**:
- `win1`: Upload-Konfiguration
- `win2`: Download und Transfer-Konfiguration
- `target_host`: SSH-Verbindungsdetails
- `google_drive`: API-Credentials
- `logging`: Logging-Konfiguration

## Datenfluss

### Phase 1: Upload (win1 → Google Drive)

```
Datei speichern in watch_folder
    ↓
watchdog erkennt Datei
    ↓
Prüfe ob Datei vollständig
    ↓
Google Drive API Upload
    ↓
Datei in Google Drive
```

### Phase 2: Download (Google Drive → win2)

```
Periodische Prüfung (alle X Sekunden)
    ↓
Google Drive API: Liste Dateien
    ↓
Filtere neue Dateien (nicht in processed_files.txt)
    ↓
Download jeder neuen Datei
    ↓
Datei lokal speichern
```

### Phase 3: Transfer (win2 → target-host)

```
SSH-Verbindung zu Jumpserver
    ↓
SSH-Tunnel zu target-host erstellen
    ↓
SCP Transfer über Tunnel
    ↓
Datei auf target-host speichern
    ↓
Als verarbeitet markieren
```

## Sicherheitsaspekte

### Authentifizierung

1. **Google Drive**:
   - OAuth 2.0 Flow
   - Token werden lokal gespeichert
   - Automatische Token-Erneuerung

2. **SSH/SCP**:
   - SSH-Key-basierte Authentifizierung (empfohlen)
   - Alternative: Passwort-Authentifizierung
   - SSH-Tunnel über Jumpserver
   - Unterstützung für Pageant (SSH-Agent)

### Datenschutz

- Credentials werden nicht in Git committet (`.gitignore`)
- Token werden lokal gespeichert
- SSH-Keys sollten sicher aufbewahrt werden

## Fehlerbehandlung

### Retry-Mechanismus
- Bei fehlgeschlagenen Uploads: Logging, keine automatische Wiederholung
- Bei fehlgeschlagenen Downloads: Datei bleibt in Google Drive, wird beim nächsten Check erneut versucht
- Bei fehlgeschlagenen Transfers: Datei bleibt lokal, wird beim nächsten Check erneut versucht

### Logging
- Alle Operationen werden geloggt
- Logs in separaten Dateien (`win1_upload.log`, `win2_transfer.log`)
- Log-Level konfigurierbar

## Erweiterungsmöglichkeiten

1. **Verschlüsselung**: Dateien vor Upload verschlüsseln
2. **Komprimierung**: Große Dateien komprimieren
3. **Benachrichtigungen**: E-Mail bei Erfolg/Fehler
4. **Web-Interface**: Status-Monitoring über Web-UI
5. **Multi-File Support**: Batch-Transfers optimieren
6. **Resume-Funktion**: Unterbrochene Transfers fortsetzen

## Performance-Überlegungen

- **Upload**: Abhängig von Internet-Geschwindigkeit auf win1
- **Download**: Abhängig von Internet-Geschwindigkeit auf win2
- **Transfer**: Abhängig von Netzwerk-Geschwindigkeit zwischen win2 und target-host
- **Check-Intervall**: Konfigurierbar, Standard 30 Sekunden

## Skalierbarkeit

- Aktuell: Einzelne Dateien sequenziell
- Erweiterbar: Parallele Verarbeitung mehrerer Dateien
- Erweiterbar: Queue-System für große Dateimengen

