# Google Drive Setup - Detaillierte Anleitung

## Was ist die `google_drive_folder_id`?

Die `google_drive_folder_id` ist eine eindeutige Identifikationsnummer, die Google Drive jedem Ordner zuweist. Sie wird in der URL des Ordners angezeigt, wenn Sie den Ordner in Google Drive öffnen.

## So finden Sie die Google Drive Folder ID

### Methode 1: Aus der URL (Einfachste Methode)

1. **Öffnen Sie Google Drive** in Ihrem Browser: https://drive.google.com

2. **Erstellen Sie einen neuen Ordner** (falls noch nicht vorhanden):
   - Klicken Sie auf "Neu" → "Ordner"
   - Geben Sie einen Namen ein, z.B. "FileTransfer"
   - Klicken Sie auf "Erstellen"

3. **Öffnen Sie den Ordner** durch Doppelklick

4. **Schauen Sie in die Adressleiste** Ihres Browsers:
   ```
   https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
                                                      ↑
                                    Das ist die Folder ID!
   ```

5. **Kopieren Sie die Folder ID** (der lange String nach `/folders/`)

   **Beispiel:**
   - URL: `https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p`
   - Folder ID: `1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p`

### Methode 2: Über Rechtsklick → Link teilen

1. **Rechtsklick** auf den Ordner in Google Drive
2. Klicken Sie auf **"Link teilen"** oder **"Freigeben"**
3. Klicken Sie auf **"Link kopieren"**
4. Der Link enthält die Folder ID:
   ```
   https://drive.google.com/drive/folders/FOLDER_ID_HIER?usp=sharing
   ```

### Methode 3: Über die Ordner-Eigenschaften

1. **Rechtsklick** auf den Ordner
2. Wählen Sie **"Details"** oder **"Eigenschaften"**
3. Die Folder ID kann in den Metadaten angezeigt werden

## Wichtige Hinweise

### ✅ Gleiche Folder ID für win1 und win2

**WICHTIG**: Beide Computer (win1 und win2) müssen die **gleiche** `google_drive_folder_id` verwenden!

- win1 lädt Dateien in diesen Ordner hoch
- win2 überwacht diesen Ordner auf neue Dateien

**Beispiel in config.json:**
```json
{
  "win1": {
    "google_drive_folder_id": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"
  },
  "win2": {
    "google_drive_folder_id": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"
  }
}
```

### ✅ Ordner-Berechtigungen

Stellen Sie sicher, dass:
- Der Ordner für das Google-Konto zugänglich ist, das Sie für die Authentifizierung verwenden
- Beide Computer (win1 und win2) mit dem **gleichen Google-Konto** authentifiziert werden (empfohlen)

## Benötigen Sie Username oder andere Informationen?

### ❌ Username wird NICHT benötigt

Die Google Drive API verwendet **OAuth 2.0** zur Authentifizierung. Sie müssen keinen Username in der Konfiguration angeben.

### ✅ Was Sie benötigen:

1. **`credentials.json`** (einmalig)
   - Wird von Google Cloud Console heruntergeladen
   - Enthält OAuth 2.0 Client Credentials
   - Siehe `GOOGLE_CREDENTIALS_SETUP.md`

2. **`google_drive_folder_id`** (in config.json)
   - Die ID des Ordners, wie oben beschrieben

3. **Token** (wird automatisch erstellt)
   - Beim ersten Start der Skripte wird ein Browser-Fenster geöffnet
   - Sie melden sich mit Ihrem Google-Konto an
   - Das Token wird automatisch in `token.json` gespeichert
   - **Sie müssen das Token nicht manuell konfigurieren!**

## Vollständiger Setup-Prozess

### Schritt 1: Google Cloud Console Setup

1. Gehen Sie zu [Google Cloud Console](https://console.cloud.google.com/)
2. Erstellen Sie ein Projekt
3. Aktivieren Sie die Google Drive API
4. Erstellen Sie OAuth 2.0 Credentials (Desktop App)
5. Laden Sie `credentials.json` herunter

### Schritt 2: Google Drive Ordner erstellen

1. Erstellen Sie einen Ordner in Google Drive
2. Notieren Sie sich die Folder ID aus der URL

### Schritt 3: config.json konfigurieren

```json
{
  "win1": {
    "google_drive_folder_id": "IHRE_FOLDER_ID_HIER"
  },
  "win2": {
    "google_drive_folder_id": "IHRE_FOLDER_ID_HIER"
  },
  "google_drive": {
    "credentials_file": "credentials.json",
    "token_file": "token.json",
    "scopes": ["https://www.googleapis.com/auth/drive.file"]
  }
}
```

### Schritt 4: Erste Authentifizierung

**Auf win1:**
```bash
python win1_upload_monitor.py
```
- Browser öffnet sich automatisch
- Melden Sie sich mit Ihrem Google-Konto an
- Erlauben Sie den Zugriff
- Token wird in `token.json` gespeichert

**Auf win2:**
```bash
python win2_download_and_transfer.py
```
- Browser öffnet sich automatisch
- Melden Sie sich mit dem **gleichen** Google-Konto an
- Erlauben Sie den Zugriff
- Token wird in `token.json` gespeichert

## Beispiel-Konfiguration

```json
{
  "win1": {
    "watch_folder": "C:\\SYN\\Upload",
    "google_drive_folder_id": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p",
    "delete_after_upload": false,
    "move_after_upload": true,
    "move_to_folder": "C:\\SYN\\Upload\\transfered"
  },
  "win2": {
    "download_folder": "C:\\SYN\\Download",
    "google_drive_folder_id": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p",
    "check_interval_seconds": 30,
    "delete_after_transfer": true
  },
  "google_drive": {
    "credentials_file": "credentials.json",
    "token_file": "token.json",
    "scopes": ["https://www.googleapis.com/auth/drive.file"]
  }
}
```

## Häufige Fragen

### Q: Muss ich die Folder ID jedes Mal neu eingeben?
**A:** Nein, einmal konfiguriert bleibt sie bestehen.

### Q: Kann ich mehrere Ordner verwenden?
**A:** Aktuell unterstützt das Skript nur einen Ordner. Für mehrere Ordner müsste das Skript erweitert werden.

### Q: Was passiert, wenn ich die falsche Folder ID eingebe?
**A:** Die Skripte werden einen Fehler melden, dass der Ordner nicht gefunden wurde.

### Q: Muss ich den Ordner freigeben?
**A:** Nein, solange beide Computer mit dem gleichen Google-Konto authentifiziert sind, haben sie Zugriff auf den Ordner.

### Q: Was ist, wenn ich verschiedene Google-Konten verwenden möchte?
**A:** Sie müssen den Ordner für das andere Konto freigeben:
1. Rechtsklick auf Ordner → "Link teilen"
2. Geben Sie die E-Mail-Adresse des anderen Kontos ein
3. Wählen Sie Berechtigung "Bearbeiter" oder "Leser"

## Troubleshooting

### Fehler: "Folder not found"
- Prüfen Sie, ob die Folder ID korrekt ist
- Prüfen Sie, ob der Ordner für Ihr Google-Konto zugänglich ist

### Fehler: "Permission denied"
- Prüfen Sie, ob Sie den Ordner öffnen können in Google Drive
- Prüfen Sie, ob das richtige Google-Konto verwendet wird

### Token abgelaufen
- Löschen Sie `token.json`
- Starten Sie das Skript erneut
- Authentifizieren Sie sich erneut

