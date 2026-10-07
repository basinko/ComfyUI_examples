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
     {
       "mcpServers": {
         "blender": { "command": "uvx", "args": ["blender-mcp"] }
       }
     }
     ```
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

Füge den Prompt aus `NEUER_CHAT_PROMPT_PRAEZISE.md` ein, hänge das Character Sheet an und setze **diesen Block davor**:

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
