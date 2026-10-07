# RoBi mit Blender MCP

Mit Blender MCP steuert Claude dein Blender direkt. Claude führt Python-Code in Blender aus, holt sich Screenshots vom Viewport und prüft seine Arbeit selbst. Copy-Paste von Skripten entfällt.

Projekt: https://github.com/ahujasid/blender-mcp (Open Source, läuft lokal auf deinem Rechner)

## Einrichten (einmalig)

1. **uv installieren** (startet den MCP-Server)
   - Mac: `brew install uv`
   - Windows (PowerShell): `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`, danach den PC neu starten
2. **Blender-Add-on installieren**
   - `addon.py` aus dem Repo herunterladen
   - Blender → Bearbeiten → Einstellungen → Add-ons → ⌄ → „Von Datenträger installieren…“ → `addon.py` wählen → Häkchen bei **„Interface: Blender MCP“** setzen
3. **Claude verbinden**
   - **Claude Desktop:** Einstellungen → Entwickler → Konfiguration bearbeiten → in `claude_desktop_config.json` eintragen:
     ```json
     {"mcpServers": {"blender": {"command": "uvx", "args": ["blender-mcp"]}}}
     ```
     Falls dort schon Einträge stehen: nur `"blender": {...}` in das bestehende `"mcpServers"` einfügen.
     Danach Claude Desktop komplett neu starten.
   - **Claude Code (Terminal):** `claude mcp add blender uvx blender-mcp`
4. **Starten**
   - In Blender im 3D-Viewport **N** drücken → Reiter **BlenderMCP** → **„Connect to Claude“**
   - In Claude erscheint dann ein Hammer- bzw. Tool-Symbol mit den Blender-Werkzeugen

## Wichtig
- Immer nur **ein** Programm gleichzeitig mit Blender MCP verbinden.
- Claude führt beliebigen Python-Code in Blender aus: vorher die .blend-Datei **speichern**, regelmäßig Versionen sichern (Datei → Speichern unter… `robi_v2_01.blend`, `_02` …).
- Der Ordner `blender/` aus diesem Repo muss lokal liegen. Gib Claude den Pfad dazu, z. B. `C:\Users\Kai\Desktop\robi\blender\` oder `~/Desktop/robi/blender/`.
- Dieser Cloud-Chat hier kann nicht auf dein lokales Blender zugreifen. Blender MCP funktioniert nur in Claude Desktop oder Claude Code auf demselben Rechner wie Blender.

## Start-Prompt für den neuen Chat (Claude Desktop mit Blender MCP)

Am kürzesten: nimm `ROBI_PROMPT_KOMPLETT.md`. Er enthält schon die Sparregeln, die MCP-Arbeitsweise und alle Maße. Alternativ: Füge den Prompt aus `NEUER_CHAT_PROMPT_PRAEZISE.md` ein, hänge das Character Sheet an und setze **diesen Block davor**:

---

Du hast über **Blender MCP** direkten Zugriff auf mein laufendes Blender 5.0. Arbeite so:

- **Erst schauen:** Rufe zuerst die Szeneninfo ab und mach einen Viewport-Screenshot, bevor du etwas änderst.
- **Kleine Code-Blöcke:** Führe Python immer in kleinen Blöcken aus, höchstens ein Bauteil pro Ausführung. Lieber viele kleine Schritte als ein großes Skript.
- **Nach jedem Bauteil prüfen:** Stell die Ansicht auf orthografisch Front und auf 3/4 und mach Viewport-Screenshots. Vergleiche sie mit dem Character Sheet und nenne mir die Abweichungen (Form, Proportion, Farbe). Korrigiere sie, bevor du weitermachst.
- **Fertige Teile nicht neu bauen:** Alles kommt in die Collection `RoBi_v2`. Bestehende Teile änderst du gezielt, statt sie neu zu erzeugen.
- **Vorhandene Dateien:** Sie liegen in `<HIER DEINEN PFAD EINTRAGEN>/blender/`. Das sind `robi.glb` (Gelenke und 9 Animationen), `robi_zimmer.glb`, `gesichter/`, `robi_blender_setup.py`. Importiere `robi.glb` zuerst als **Referenz** in eine eigene Collection `Referenz_alt`, halbtransparent, damit Maße und Gelenke passen.
- **Fragen statt raten:** Frag mich, bevor du etwas löschst, das du nicht selbst erzeugt hast.
- **Kurz berichten:** Schreib nach jedem Schritt in 2–3 Sätzen auf Deutsch, was du gemacht hast, und zeig den Screenshot.

---

## Token sparen

**Kein Browser- oder Computer-Use für Blender.** Blender ist ein Desktop-Programm. Browser-Use kommt gar nicht heran. Computer-Use braucht für jeden Klick einen Screenshot, und jeder Screenshot kostet viele Token. Ein Modell bauen hieße Hunderte Klicks. Python-Code ist 10- bis 50-mal günstiger.

**Am günstigsten: Claude Code + Blender ohne Oberfläche**
Claude Code (Terminal) auf deinem Rechner, Blender läuft im Hintergrund:
```
blender -b robi_v2.blend -P bauteil.py
```
- Der Code steckt in Dateien. Claude ändert nur einzelne Zeilen (Parameter) und muss nicht jedes Mal das ganze Skript neu schreiben.
- Jedes Skript rendert ein kleines Kontrollbild (512 px), das Claude ansieht. Mehr Bilder braucht es nicht.

**Mit Blender MCP sparsam arbeiten**
- Screenshots klein halten (max. 512 px) und nur einen pro fertigem Bauteil.
- Szeneninfo nur einmal am Anfang abfragen. Danach gezielt einzelne Objekte abfragen.
- Wiederkehrende Funktionen einmal als Hilfsmodul in Blender anlegen (`robi_lib`) und danach nur noch aufrufen.

**Allgemein**
- Pro Meilenstein ein neuer Chat. Am Ende des alten Chats eine Zusammenfassung mit Stand, Parametern und nächstem Schritt erstellen lassen und damit den neuen Chat starten.
- Für Routineschritte (Materialien, Licht) reicht ein kleineres Modell. Das größte Modell nur für Formen und Rig nehmen.

### Spar-Block für den Prompt
---
Arbeite token-sparsam:
- Kein Computer-Use und keine Klicks. Arbeite nur mit Python über `execute_blender_code` bzw. Skriptdateien.
- Leg alle wiederverwendbaren Funktionen einmal als Text-Datenblock `robi_lib` in Blender an. Später rufst du nur noch diese Funktionen mit Parametern auf und schickst nicht erneut den ganzen Code.
- Mach höchstens **einen** Viewport-Screenshot pro fertigem Bauteil, mit max. 512 px. Frag die Szeneninfo nur einmal am Anfang ab.
- Antworte kurz: ein Satz zum Ergebnis, Abweichungen als Stichpunkte, kein Code im Chat außer dem, der ausgeführt wird.
- Wenn ein Meilenstein fertig ist, schreib eine Übergabe in höchstens 15 Zeilen: Parameter, Objektnamen, nächster Schritt. Damit starte ich den nächsten Chat.
---
