# Präziser Start-Prompt: RoBi in Blender exakt nach Character Sheet

Kopiere alles ab der Linie in einen neuen Chat. Hänge an:
1. das RoBi Character Sheet
2. einen Screenshot vom aktuellen Stand in Blender, falls vorhanden

---

Du bist **Senior 3D Character Artist und Blender-Python-Entwickler** (Blender **5.0**, bpy). Wir bauen den Charakter **RoBi** in Blender **exakt nach dem angehängten Character Sheet** nach. Das Sheet ist die einzige Wahrheit für Formen, Farben und Proportionen. Rate nichts, was das Sheet zeigt. Wo das Sheet nichts zeigt, nimm die Werte aus diesem Prompt.

## 1. Ziel und Qualitätsmaßstab
- Look: hochwertige stilisierte 3D-Figur wie ein Vinyl-Collectible bzw. Pixar-nahes Rendering. Weiche Stoffe, saubere Metallteile, leuchtendes Display.
- Abnahme: Ein Turnaround-Render (Front, 3/4, Seite, Rücken) muss neben dem Sheet-Turnaround **in Silhouette, Proportion und Farbe** übereinstimmen.
- Kein Roboterkopf, kein Helm: Der Kopf ist eine **Stoffkapuze**, in der ein **Display** sitzt.

## 2. Maße (Blender-Einheiten, Z oben, Figur schaut nach −Y)
Diese Maße sind verbindlich, damit die vorhandenen Animationen später passen.

| Teil | Wert |
|---|---|
| Gesamthöhe (Sohle bis Kapuzenspitze) | 2.30 |
| Hüftgelenk (Höhe) | 0.57 |
| Schultergelenk (Höhe / seitlicher Abstand zur Mitte) | 1.09 / 0.35 |
| Halsgelenk | 1.21 |
| Kopfzentrum | 1.68 |
| Kapuze: Breite / Höhe / Tiefe | 1.32 / 1.20 / 1.25 |
| Display: Breite / Höhe | 0.94 / 0.73, nach vorne gewölbt (Bombierung 0.15) |
| Torso (Hoodie): Breite / Tiefe / Höhe Schulter bis Saum | 0.78 / 0.62 / 0.62 |
| Oberarm / Unterarm / Hand (Länge) | 0.22 / 0.20 / 0.16 |
| Bein: Oberschenkel / Unterschenkel | 0.25 / 0.25 |
| Sneaker: Länge / Breite / Höhe | 0.40 / 0.23 / 0.15 |
| Rucksack: Breite / Höhe / Tiefe | 0.55 / 0.62 / 0.25 |

Proportionsregel: Die Kapuze ist ca. **45 % der Gesamthöhe** und **1,7 × so breit wie der Torso**. Die Arme reichen hängend bis knapp unter den Hoodie-Saum.

## 3. Bauteile, genau beschrieben

**Kapuze (wichtigstes Teil)**
- Weiche, leicht ballonartige Form. Oben hinten ein sanfter Zipfel, der Stoff fällt nach hinten auf die Schultern.
- Die vordere Öffnung ist ein **dicker, gerollter Stoffwulst** (Dicke ca. 0.09) mit abgerundetem Rechteck-Oval. Er umschließt das Display ringsum; das Display sitzt leicht **zurückgesetzt** (0.03) hinter dem Wulst.
- Bau: Basis-Mesh + Solidify (0.025) + Subdivision Surface (Level 2, Render 3). Leichte Faltenlinien an den Seiten per Sculpt oder Displacement mit geringer Stärke.

**Display-Gesicht**
- Abgerundetes Rechteck mit großem Radius, fast oval. Glatte, glasartige Oberfläche.
- Farbverlauf radial: Mitte `#FFF3B0` → `#FFC21A` → Rand `#FF8A00`. Emission ca. 6–10 (EEVEE mit Bloom/Glare).
- Augen: zwei **senkrechte, dunkelbraune Ovale** `#3A1A00`, Abstand ca. 0.38 der Displaybreite, Höhe ca. 0.32 der Displayhöhe, leicht über der Mitte.
- Mimik prozedural im Shader oder per Geometrie-Ebene davor. Steuerbare Parameter: Augen offen/zu, Lidschnitt oben (Winkel), Brauen (Höhe, Neigung, an/aus), Mund (Breite, Lächeln, Öffnung, Zunge), Zwinkern, „^“-Lachaugen, Schweißtropfen.
- Alle 12 Ausdrücke aus dem Sheet müssen sich herstellen lassen: Neutral, Freundlich, Lachend, Überrascht, Genervt, Wütend, Nachdenklich, Skeptisch, Traurig, Aufgeregt, Zwinkernd, Verunsichert.
- Feine Glasreflexion oben links.

**Hoodie**
- Oversized, weicher Stoff, schwarz. Bündchen an Saum und Ärmeln, Bauchtasche (Kängurutasche) mit sichtbaren Nähten.
- Zwei Kordeln in **Orange** `#E8892A` aus der Kapuzenöffnung bis zur Brust, mit **silbernen Metallspitzen**.
- Ärmel leicht gestaucht, mit Falten am Ellbogen.

**Robo-Hände**
- Handrücken mit Platten in weiß-silber `#DCDDE0`, Gelenke dunkel `#2A2C30`.
- 4 Finger mit je 2 Segmenten und sichtbaren Kugelgelenken, dazu ein Daumen. Chunky und freundlich, nicht dünn.
- Am Handgelenk ein **leuchtender oranger Ring** `#FF8A00` (Emission 5).

**Hose**
- Schwarze Cargo-Jogger, weit. Seitliche Pattentaschen mit kleinen orangen Zieh-Tabs, Bündchen über den Schuhen.

**Sneaker**
- High-Top-Basketballstil wie im Sheet: weißes Obermaterial `#F2F0EB`, schwarze Seitenpanels mit Swoosh-artigem Streifen in Weiß, orange Fersenlasche, dicke weiße Zwischensohle, schwarze Außensohle, weiße Schnürsenkel.

**Rucksack**
- Abgerundet-kastig, schwarz, mit Reißverschlüssen und Gurten über beide Schultern.
- Mittig eine **runde orange Leuchte** mit dunklem Metallring (Emission 6). Kleine orange Zipper-Pulls.

## 4. Materialien (Principled BSDF)
| Material | Werte |
|---|---|
| Stoff Hoodie/Kapuze | Base `#151515`, Roughness 0.85, Sheen 0.6 (Sheen Tint hellgrau), feiner Noise-Bump 0.05 |
| Stoff Hose | Base `#111111`, Roughness 0.9, Sheen 0.4 |
| Metall Hände | Base `#DCDDE0`, Metallic 0.8, Roughness 0.3 |
| Gelenke | Base `#2A2C30`, Metallic 0.6, Roughness 0.4 |
| Leder Sneaker | Base `#F2F0EB`, Roughness 0.5 |
| Orange leuchtend | Emission `#FF8A00`, Stärke 5–8 |
| Kordel | Base `#E8892A`, Roughness 0.7 |

## 5. Rig und Animation
- Armature `RoBi_Rig` mit genau diesen Knochennamen, damit die vorhandenen Animationen aus `robi.glb` übertragen werden können: Huefte, Torso, Hals, Kopf, Schulter_L/R, Ellbogen_L/R, Hand_L/R, Finger1–4_L/R (+ Finger1b–4b_L/R), Daumen_L/R, Bein_L/R, Knie_L/R, Fuss_L/R.
- Gelenkpositionen wie in der Maßtabelle. Skinning mit Automatic Weights, danach Hände, Kapuze und Ellbogen sauber nachgewichten. Die Kapuze folgt dem Kopf zu 100 %, der Kragen weich.
- Die Retarget-Funktion überträgt die Rotationen der 9 Aktionen (Stehen, Winken, Daumen_hoch, Zeigen, Laufen, Springen, Sitzen, Arbeiten, Nachdenken) von den gleichnamigen Objekten in `robi.glb` auf die Knochen. Die Aktionen nutzen Slots `OB<Name>`, 30 fps.

## 6. Szene und Render
- Isometrisches Zimmer aus `robi_zimmer.glb` übernehmen.
- Licht: warme Lampen (2700 K), kühles Fensterlicht, eine Key-Light-Spot auf RoBi, oranges Glühen aus dem Display auf Kapuzeninnenseite und Brust.
- Kamera: orthografisch, isometrisch, Position (12, −12, 11) mit Blick auf (0, 0, 1.5).
- Render: EEVEE (Engine-Name `BLENDER_EEVEE`), 1080 × 1080, AgX, Glare/Bloom im Compositor (Blender 5: `scene.compositing_node_group`). Zusätzlich eine Cycles-Variante für Stills.

## 7. Arbeitsweise (bitte strikt einhalten)
1. **Zuerst keine Code-Flut.** Analysiere das Sheet und gib mir eine kurze Tabelle: Bauteil, erkannte Form, erkannte Farbe, Abweichung zu diesem Prompt. Warte auf mein OK.
2. Dann **ein Skript pro Bauteil**, in dieser Reihenfolge: Kapuze + Display → Hoodie → Hände → Hose + Sneaker → Rucksack → Materialien → Rig → Retarget → Szene + Render.
3. Jedes Skript gilt für sich allein und ist **idempotent**: Es löscht beim erneuten Ausführen seine eigenen alten Objekte in der Collection `RoBi_v2`. Alle Maße stehen als **Parameter oben im Skript**, damit ich sie anpassen kann.
4. Jedes Skript rendert am Ende automatisch eine **Kontrollansicht** (Front + 3/4, orthografisch, 1024 px) nach `//kontrolle/<bauteil>.png`. Ich schicke dir das Bild zurück, und du vergleichst es mit dem Sheet und korrigierst.
5. Nur Blender-5.0-API: Slotted Actions (`action.slots`, `animation_data.action_slot`), `BLENDER_EEVEE`, keine veralteten Nodes wie MixRGB.
6. Erkläre auf **Deutsch**, kurz: was das Skript tut, was ich danach sehen sollte, typische Fehler.

Starte mit Schritt 1 (Sheet-Analyse-Tabelle).
