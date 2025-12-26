# Pageant (SSH-Agent) Setup

## Was ist Pageant?

Pageant ist ein SSH-Agent für Windows, der Teil von PuTTY ist. Er ermöglicht es, SSH-Keys einmal zu laden und dann automatisch für alle SSH-Verbindungen zu verwenden, ohne dass Sie den Key-Pfad jedes Mal angeben müssen.

## Vorteile der Verwendung von Pageant

- ✅ Keys müssen nicht in der Konfiguration gespeichert werden
- ✅ Keys sind sicher im Speicher (nicht auf der Festplatte während der Verwendung)
- ✅ Einmal geladen, funktioniert für alle SSH-Verbindungen
- ✅ Unterstützt mehrere Keys gleichzeitig

## Installation und Setup

### Schritt 1: Pageant installieren

Pageant ist Teil von PuTTY. Falls Sie PuTTY noch nicht haben:

1. Laden Sie PuTTY herunter: https://www.chiark.greenend.org.uk/~sgtatham/putty/
2. Installieren Sie PuTTY (Pageant ist enthalten)

### Schritt 2: SSH-Keys zu Pageant hinzufügen

#### Methode 1: Über Pageant GUI

1. **Starten Sie Pageant**:
   - Suchen Sie nach "Pageant" im Startmenü
   - Oder führen Sie `pageant.exe` aus

2. **Pageant erscheint im System-Tray** (rechts unten in der Taskleiste)
   - Klicken Sie mit der rechten Maustaste auf das Pageant-Icon
   - Wählen Sie "Add Key"

3. **Wählen Sie Ihre SSH-Key-Datei**:
   - Navigieren Sie zu Ihrer Key-Datei (z.B. `id_rsa` oder `id_rsa.ppk`)
   - Falls Sie einen OpenSSH-Key haben (id_rsa), müssen Sie ihn möglicherweise zuerst mit PuTTYgen in .ppk Format konvertieren

4. **Geben Sie das Passphrase ein** (falls vorhanden)

5. **Key ist jetzt geladen** und wird automatisch verwendet

#### Methode 2: Über Kommandozeile

```powershell
# Starte Pageant und lade Key
pageant.exe C:\Users\YourUser\.ssh\id_rsa.ppk
```

#### Methode 3: Automatischer Start beim Windows-Login

1. Erstellen Sie eine Verknüpfung zu Pageant
2. Fügen Sie den Key-Pfad als Parameter hinzu:
   ```
   "C:\Program Files\PuTTY\pageant.exe" "C:\Users\YourUser\.ssh\id_rsa.ppk"
   ```
3. Legen Sie die Verknüpfung in den Autostart-Ordner:
   - Windows + R
   - `shell:startup`
   - Verknüpfung dort ablegen

## Konfiguration in config.json

Die Skripte unterstützen jetzt Pageant automatisch. In der `config.json` können Sie konfigurieren:

```json
{
  "target_host": {
    "jumpserver": {
      "host": "jumpserver.example.com",
      "port": 22,
      "username": "jumpuser",
      "use_ssh_agent": true,    // ← Aktiviert Pageant-Unterstützung
      "key_file": "C:\\Users\\YourUser\\.ssh\\id_rsa",  // Fallback, falls Pageant nicht verfügbar
      "password": null
    },
    "target": {
      "host": "target-host.example.com",
      "port": 22,
      "username": "targetuser",
      "use_ssh_agent": true,    // ← Aktiviert Pageant-Unterstützung
      "key_file": "C:\\Users\\YourUser\\.ssh\\id_rsa",  // Fallback
      "password": null,
      "target_folder": "/home/targetuser/transfer"
    }
  }
}
```

### Konfigurationsoptionen

- **`use_ssh_agent: true`** (empfohlen)
  - Das Skript versucht zuerst, Pageant zu verwenden
  - Falls Pageant nicht verfügbar ist, wird auf `key_file` zurückgegriffen
  - Falls auch `key_file` nicht verfügbar ist, wird `password` verwendet

- **`use_ssh_agent: false`**
  - Pageant wird nicht verwendet
  - Es wird direkt `key_file` oder `password` verwendet

## Funktionsweise

Das Skript verwendet folgende Priorität:

1. **SSH-Agent (Pageant)** - wenn `use_ssh_agent: true` und Pageant läuft
2. **Key-Datei** - wenn `key_file` angegeben und Datei existiert
3. **Passwort** - wenn `password` angegeben

## Konvertierung von OpenSSH zu PuTTY Format

Falls Sie einen OpenSSH-Key haben (`id_rsa`) und Pageant verwenden möchten:

1. **Starten Sie PuTTYgen**:
   - Suchen Sie nach "PuTTYgen" im Startmenü

2. **Laden Sie Ihren OpenSSH-Key**:
   - Klicken Sie auf "Load"
   - Wählen Sie Ihre `id_rsa` Datei
   - Geben Sie das Passphrase ein (falls vorhanden)

3. **Speichern Sie als PuTTY-Key**:
   - Klicken Sie auf "Save private key"
   - Speichern Sie als `id_rsa.ppk`

4. **Laden Sie den .ppk Key in Pageant**

## Troubleshooting

### Problem: "SSH-Agent nicht verfügbar"

**Lösung**: 
- Stellen Sie sicher, dass Pageant läuft (Icon im System-Tray)
- Prüfen Sie, ob Keys in Pageant geladen sind (Rechtsklick auf Icon → "View Keys")

### Problem: "Keine Authentifizierungsmethode verfügbar"

**Lösung**:
- Stellen Sie sicher, dass entweder:
  - Pageant läuft und Keys geladen sind, ODER
  - `key_file` korrekt konfiguriert ist, ODER
  - `password` konfiguriert ist

### Problem: "Permission denied"

**Lösung**:
- Prüfen Sie, ob der richtige Key in Pageant geladen ist
- Prüfen Sie, ob der Key auf dem Server installiert ist
- Testen Sie die Verbindung manuell mit PuTTY

### Problem: Key wird nicht erkannt

**Lösung**:
- Stellen Sie sicher, dass der Key im richtigen Format ist (.ppk für Pageant)
- Konvertieren Sie OpenSSH-Keys zu PuTTY-Format mit PuTTYgen
- Laden Sie den Key erneut in Pageant

## Test der Verbindung

### Test mit PuTTY

1. Starten Sie PuTTY
2. Geben Sie Hostname und Port ein
3. Klicken Sie auf "Open"
4. Wenn Pageant läuft, sollte die Authentifizierung automatisch funktionieren

### Test mit dem Skript

```bash
python win2_download_and_transfer.py
```

Das Skript sollte automatisch Pageant verwenden, wenn es läuft. Prüfen Sie die Logs:
- `"Verwende SSH-Agent (Pageant) für ..."` = Pageant wird verwendet ✅
- `"Verwende Key-Datei für ..."` = Fallback auf Key-Datei
- `"Verwende Passwort-Authentifizierung für ..."` = Fallback auf Passwort

## Sicherheitshinweise

- ✅ Pageant speichert Keys im Speicher (RAM), nicht auf der Festplatte
- ✅ Keys werden beim Beenden von Pageant entfernt
- ⚠️ Wenn jemand Zugriff auf Ihren Computer hat, während Pageant läuft, kann er Ihre Keys verwenden
- ⚠️ Verwenden Sie Passphrases für Ihre Keys
- ⚠️ Sperren Sie Ihren Computer, wenn Sie es verlassen

## Zusammenfassung

Mit Pageant müssen Sie:
- ✅ Keys nur einmal laden (beim Start von Pageant)
- ✅ Keine Key-Pfade in der Konfiguration speichern (optional)
- ✅ Keys sicher im Speicher verwenden

Die Skripte funktionieren automatisch mit Pageant, wenn:
- ✅ `use_ssh_agent: true` in config.json
- ✅ Pageant läuft
- ✅ Keys in Pageant geladen sind

