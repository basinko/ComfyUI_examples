# RoBi in Blender

Getestet mit **Blender 5.0**. Die Szene sollte auch in Blender 4.4 und neuer laufen, denn dort gibt es die nötigen „Action Slots“.

## Inhalt

| Datei | Was |
|---|---|
| `robi.glb` | RoBi: Modell, 39 benannte Gelenke und 9 Animationen |
| `robi_zimmer.glb` | Das Zimmer, im selben Koordinatensystem |
| `gesichter/gesicht_001–012.png` | Die 12 Display-Ausdrücke als Texturen |
| `robi_blender_setup.py` | Richtet alles in Blender ein |
| `robi_blender_test.png` | Test-Render aus Blender (Cycles) |

## In 3 Schritten

1. Lade den ganzen Ordner `blender/` herunter und lass die Dateien zusammen.
2. Blender öffnen → Arbeitsbereich **Scripting** → **Öffnen** → `robi_blender_setup.py` → **Skript ausführen** (▶).
3. Im 3D-Viewport mit **N** die Seitenleiste öffnen → Reiter **RoBi**.

## Steuerung

- **Aktion**: Stehen, Winken, Daumen hoch, Zeigen, Laufen, Springen, Sitzen, Arbeiten, Nachdenken. Mit der Leertaste abspielen.
- **Ausdruck**: einer der 12 Display-Ausdrücke. **Ausdruck keyen** setzt dafür einen Keyframe im aktuellen Frame. So wechselt das Gesicht während der Animation.
  - Der Wert liegt auf dem Objekt **RoBi** als Eigenschaft `Ausdruck` (1–12). Du kannst ihn auch dort keyen: Objekt-Eigenschaften → Benutzerdefinierte Eigenschaften.
  - Reihenfolge: 1 Neutral · 2 Freundlich · 3 Lachend · 4 Überrascht · 5 Genervt · 6 Wütend · 7 Nachdenklich · 8 Skeptisch · 9 Traurig · 10 Aufgeregt · 11 Zwinkernd · 12 Verunsichert
- **Kamera**: `Iso_Kamera` (orthografisch, isometrisch). Zum Heranzoomen `Kamera_Ziel` verschieben und den Orthografischen Maßstab der Kamera verkleinern.
- **Render**: Die Szene ist auf EEVEE gestellt (1080 × 1080). Für die schönsten Ergebnisse auf Cycles umschalten.

## Gut zu wissen

- Jedes Gelenk ist ein eigenes Objekt in einer Hierarchie (RoBi → Rig → Huefte → Torso → Schulter_L → …), kein Armature-Rig. Posieren und Keyframes setzen geht direkt durch Drehen der Objekte.
- Die Animationen sind Bild für Bild aus der Web-Szene übernommen (30 fps). Du kannst sie in Blender wie normale Keyframes bearbeiten.
- Die Formen sind noch die einfachen Grundformen aus der Web-Version. Der nächste Schritt für Sheet-Qualität ist, Hoodie, Hände und Sneaker in Blender sauber neu zu modellieren. Danach kommt ein echtes Armature-Rig, z. B. mit Rigify. Die Gelenkpositionen aus dieser Datei kannst du dafür als Vorlage nehmen.
