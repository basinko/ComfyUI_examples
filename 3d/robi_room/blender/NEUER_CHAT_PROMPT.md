# Übergabe: RoBi in Blender weiterentwickeln

Kopiere alles ab der Linie in einen neuen Chat. Hänge dein Character Sheet von RoBi als Bild an.

---

Ich entwickle den stilisierten 3D-Charakter **RoBi** und will ihn jetzt in **Blender 5.0** auf Character-Sheet-Qualität bringen und animieren. Mein Character Sheet hängt als Bild an.

## Der Charakter (laut Sheet)
- Großer Kopf, kompakter Körper, kurze Arme und Beine, klare Silhouette
- Schwarzer Hoodie mit großer Kapuze; das Gesicht ist ein **gelb-orange leuchtendes Display** mit zwei dunklen ovalen Augen und gezeichneter Mimik
- Orange Kordeln mit Metallspitzen, Bauchtasche, schwarzer Rucksack mit runder oranger Leuchte
- **Robo-Hände** (weiß/silber, Gelenke, oranger Leuchtring am Handgelenk)
- Schwarze Cargohose mit Seitentaschen; Sneaker schwarz/weiß mit orangem Akzent
- Farbpalette: Schwarz, Dunkelgrau, Grau, Creme, Hautbeige, Orange
- Stimmung: warmes, filmisches Licht; dunkles, gemütliches, isometrisches Zimmer

## Was es schon gibt
Repo `basinko/ComfyUI_examples`, Branch `ccr-7365bf07-70lavj`, Ordner `3d/robi_room/blender/`:
- `robi.glb`: RoBi aus einfachen Grundformen. **39 benannte Gelenk-Objekte** in einer Hierarchie (kein Armature): RoBi → Rig → Huefte → Torso → Hals → Kopf → Display; Torso → Schulter_L/R → Ellbogen_L/R → Hand_L/R → Finger1–4_L/R (+ Finger1b–4b) und Daumen_L/R; Huefte → Bein_L/R → Knie_L/R → Fuss_L/R; dazu Rucksack, Laptop, Laptop_Deckel.
- **9 Animationen** als Blender-Aktionen mit Slots (`OB<Objektname>`), 30 fps: Stehen, Winken, Daumen_hoch, Zeigen, Laufen, Springen, Sitzen, Arbeiten, Nachdenken
- `robi_zimmer.glb`: isometrisches Zimmer (dunkle Wände, Holzboden, Bett, Schreibtisch, Sessel, Teppich, Lampen, Bilder, Uhr), im selben Koordinatensystem
- `gesichter/gesicht_001–012.png`: 12 Display-Ausdrücke (1 Neutral, 2 Freundlich, 3 Lachend, 4 Überrascht, 5 Genervt, 6 Wütend, 7 Nachdenklich, 8 Skeptisch, 9 Traurig, 10 Aufgeregt, 11 Zwinkernd, 12 Verunsichert)
- `robi_blender_setup.py`: importiert beides, baut das Display-Material (12 Texturen, Auswahl über die keybare Eigenschaft `RoBi["Ausdruck"]`; die UVs werden im Shader vertikal gespiegelt), setzt Lampen, Fensterlicht, Gesichts-Glow, eine orthografische Iso-Kamera und eine Seitenleiste „RoBi“ zum Wechseln von Aktion und Ausdruck. Getestet in Blender 5.0.1 mit Cycles.

## Was ich jetzt will (in dieser Reihenfolge)
1. **Neu modellieren auf Sheet-Qualität:** weicher Stoff-Hoodie mit Falten (Kapuze mit dicker Öffnung um das Display), richtig modellierte Robo-Hände, Sneaker, Cargohose, Rucksack. Proportionen und Gelenkpositionen aus `robi.glb` sollen als Vorlage dienen.
2. **Echtes Rig:** Armature, z. B. mit Rigify oder einem eigenen einfachen Rig, mit Fingern und IK für die Beine. Die vorhandenen 9 Animationen sollen auf das neue Rig übertragen werden, damit sie nicht verloren gehen.
3. **Display-Gesicht animierbar halten:** entweder weiter mit den 12 Texturen oder besser prozedural, sodass Augen, Lider, Brauen und Mund einzeln animierbar sind.
4. **Look-Dev:** Stoff-Shader mit Fuzz/Sheen, Metall für die Hände, Glühen des Displays mit Bloom/Glare, warmes Lampenlicht wie auf dem Sheet.
5. **Showreel:** alle Aktionen nacheinander als MP4 (1080 × 1080, 30 fps) rendern, mit Kamerafahrt, die RoBi folgt.

## Wie du mir helfen sollst
- Arbeite mit **Python-Skripten für Blender 5.0** (bpy). Dabei beachten: Slotted Actions, Engine-Name `BLENDER_EEVEE`, der Compositor nutzt `scene.compositing_node_group`.
- Zerleg die Arbeit in kleine Schritte. Jeder Schritt bekommt ein Skript, das ich im Scripting-Tab ausführe, und eine kurze Erklärung, was ich danach sehen sollte.
- Wenn etwas manuell besser geht (z. B. Sculpting), erklär mir die Schritte in der Blender-Oberfläche auf Deutsch.

Fang mit Schritt 1 an: Schlag mir vor, wie wir den Hoodie und die Kapuze aufbauen.
