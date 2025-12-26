# Google Drive Credentials Setup - Schritt für Schritt

## Übersicht

Sie benötigen **zwei Dateien** für die Google Drive API:

1. **`credentials.json`** - Einmalig von Google Cloud Console herunterladen
2. **`token.json`** - Wird automatisch beim ersten Start erstellt (Sie müssen nichts tun!)

---

## Teil 1: `credentials.json` erstellen

### Schritt 1: Google Cloud Console öffnen

1. Gehen Sie zu: https://console.cloud.google.com/
2. Melden Sie sich mit Ihrem Google-Konto an

### Schritt 2: Neues Projekt erstellen (oder bestehendes verwenden)

1. Klicken Sie oben auf das **Projekt-Dropdown** (neben "Google Cloud")
2. Klicken Sie auf **"New Project"** (oder wählen Sie ein bestehendes Projekt)
3. Geben Sie einen Projektnamen ein, z.B. "File Transfer Tool"
4. Klicken Sie auf **"Create"**
5. Warten Sie, bis das Projekt erstellt ist (kann einige Sekunden dauern)

### Schritt 3: Google Drive API aktivieren

1. Im Google Cloud Console Dashboard:
   - Klicken Sie auf das **☰ Menü** (oben links)
   - Navigieren Sie zu **"APIs & Services"** > **"Library"**
   
2. Suchen Sie nach **"Google Drive API"**:
   - Geben Sie "Google Drive API" in die Suchleiste ein
   - Klicken Sie auf **"Google Drive API"** in den Suchergebnissen
   
3. Aktivieren Sie die API:
   - Klicken Sie auf den Button **"Enable"** (oben)
   - Warten Sie, bis die API aktiviert ist

### Schritt 4: OAuth Consent Screen konfigurieren (einmalig)

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

### Schritt 5: OAuth 2.0 Credentials erstellen

1. Navigieren Sie zu **"APIs & Services"** > **"Credentials"**

2. Klicken Sie auf **"+ CREATE CREDENTIALS"** (oben)
   - Wählen Sie **"OAuth client ID"**

3. Falls Sie aufgefordert werden, den Consent Screen zu konfigurieren:
   - Folgen Sie den Anweisungen von Schritt 4

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

### ✅ Fertig für `credentials.json`!

Die Datei sollte jetzt so aussehen:
```json
{
  "installed": {
    "client_id": "xxxxx.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_secret": "xxxxx",
    "redirect_uris": ["http://localhost"]
  }
}
```

---

## Teil 2: `token.json` erstellen (automatisch!)

**WICHTIG**: Sie müssen `token.json` **NICHT manuell erstellen**! Es wird automatisch beim ersten Start der Skripte erstellt.

### So funktioniert es:

1. **Stellen Sie sicher, dass `credentials.json` im Projektordner liegt**

2. **Starten Sie eines der Skripte**:
   ```bash
   # Auf win1:
   python win1_upload_monitor.py
   
   # Oder auf win2:
   python win2_download_and_transfer.py
   ```

3. **Browser öffnet sich automatisch**:
   - Ein Browser-Fenster öffnet sich
   - Sie werden zu Google weitergeleitet

4. **Melden Sie sich an**:
   - Wählen Sie Ihr Google-Konto
   - Geben Sie Ihr Passwort ein

5. **Berechtigungen erlauben**:
   - Sie sehen eine Warnung: "Google hasn't verified this app"
   - Klicken Sie auf **"Advanced"** → **"Go to File Transfer Tool (unsafe)"**
   - Klicken Sie auf **"Allow"** um den Zugriff zu erlauben

6. **Token wird gespeichert**:
   - Nach erfolgreicher Authentifizierung wird `token.json` automatisch erstellt
   - Die Datei wird im Projektordner gespeichert
   - **Sie müssen nichts weiter tun!**

### ✅ Fertig für `token.json`!

Die Datei wird automatisch erstellt und sieht etwa so aus:
```json
{
  "token": "ya29.xxxxx",
  "refresh_token": "1//xxxxx",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "xxxxx.apps.googleusercontent.com",
  "client_secret": "xxxxx",
  "scopes": ["https://www.googleapis.com/auth/drive.file"]
}
```

---

## Konfiguration in `config.json`

Stellen Sie sicher, dass Ihre `config.json` folgendes enthält:

```json
{
  "google_drive": {
    "credentials_file": "credentials.json",
    "token_file": "token.json",
    "scopes": ["https://www.googleapis.com/auth/drive.file"]
  }
}
```

**Wichtig**: 
- Beide Dateien müssen im **gleichen Ordner** wie `config.json` liegen
- Die Dateinamen müssen genau übereinstimmen

---

## Dateistruktur

Ihr Projektordner sollte so aussehen:

```
lernbox_01/
├── config.json
├── credentials.json          ← Von Google Cloud Console heruntergeladen
├── token.json                ← Automatisch beim ersten Start erstellt
├── win1_upload_monitor.py
├── win2_download_and_transfer.py
└── requirements.txt
```

---

## Häufige Fragen

### Q: Wo finde ich die Google Cloud Console?
**A**: https://console.cloud.google.com/

### Q: Muss ich für Google Cloud Console bezahlen?
**A**: Nein, für die Google Drive API gibt es ein kostenloses Kontingent, das für normale Nutzung ausreicht.

### Q: Kann ich `credentials.json` mehrfach verwenden?
**A**: Ja, Sie können die gleiche `credentials.json` auf win1 und win2 verwenden.

### Q: Muss ich `token.json` auf beide Computer kopieren?
**A**: Nein! Jeder Computer erstellt sein eigenes `token.json` beim ersten Start.

### Q: Was passiert, wenn `token.json` abläuft?
**A**: Das Skript erneuert das Token automatisch. Sie müssen nichts tun!

### Q: Kann ich `token.json` löschen?
**A**: Ja, aber dann müssen Sie sich beim nächsten Start erneut authentifizieren.

### Q: "Google hasn't verified this app" - ist das sicher?
**A**: Ja, das ist normal für selbst erstellte Apps. Klicken Sie auf "Advanced" → "Go to [Ihr App Name] (unsafe)".

### Q: Ich sehe keinen "Download JSON" Button?
**A**: Nach dem Erstellen der OAuth Client ID erscheint ein Popup. Falls nicht, klicken Sie auf das **Download-Icon** (⬇️) neben der Client ID in der Credentials-Liste.

---

## Troubleshooting

### Problem: "Credentials-Datei nicht gefunden"
**Lösung**: 
- Stellen Sie sicher, dass `credentials.json` im Projektordner liegt
- Prüfen Sie den Pfad in `config.json`

### Problem: Browser öffnet sich nicht
**Lösung**:
- Prüfen Sie, ob ein Browser installiert ist
- Prüfen Sie Firewall-Einstellungen
- Versuchen Sie, den Standard-Browser manuell zu öffnen

### Problem: "Access denied" oder "Permission denied"
**Lösung**:
- Stellen Sie sicher, dass Sie sich mit dem richtigen Google-Konto anmelden
- Prüfen Sie, ob Sie als Test-User hinzugefügt wurden (OAuth Consent Screen)

### Problem: Token wird nicht erstellt
**Lösung**:
- Prüfen Sie, ob Sie auf "Allow" geklickt haben
- Prüfen Sie die Logs auf Fehlermeldungen
- Löschen Sie eventuell vorhandene `token.json` und versuchen Sie es erneut

---

## Zusammenfassung

1. **`credentials.json`**: 
   - ✅ Einmalig von Google Cloud Console herunterladen
   - ✅ In Projektordner speichern

2. **`token.json`**: 
   - ✅ Wird automatisch beim ersten Start erstellt
   - ✅ Sie müssen nichts manuell tun!

3. **Beide Dateien** müssen im Projektordner liegen, wo auch `config.json` ist.

