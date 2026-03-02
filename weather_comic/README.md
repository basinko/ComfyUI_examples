# Kira Wetter-Comic

Automatische Wetter-Comic Generierung mit dem Charakter **Kira** -- eine fröhliche Manga-Wetterfee, die jeden Tag das aktuelle Wetter in einem kurzen Comic-Format präsentiert. Optimiert für lokale deutsche Zielgruppen.

## Charakter: Kira

| Eigenschaft | Beschreibung |
|---|---|
| **Name** | Kira |
| **Stil** | Anime/Manga Comic Art |
| **Haare** | Kurz, pink |
| **Augen** | Leuchtend grün |
| **Outfit** | Hellblaues Blazer mit weißer Bluse (Wetter-Moderatorin) |
| **Persönlichkeit** | Fröhlich, energisch, nahbar |
| **Zielgruppe** | Lokale Community, Social Media, Stadt-Newsletter |

## Workflows

### 1. Einfache Version (`workflow_kira_simple.json`)

Ein einfacher Single-Panel Workflow -- ideal zum Einstieg und schnellen Anpassen.

**So geht's:**
1. Lade `workflow_kira_simple.json` in [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
2. Passe den Prompt im Node "Kira Wetter Prompt" an das heutige Wetter an
3. Klicke auf "Queue Prompt"

**Workflow-Aufbau:**
```
CheckpointLoader → CLIPTextEncode (Positiv + Negativ) → KSampler → VAEDecode → SaveImage
```

### 2. Multi-Panel Comic Strip (`workflow_kira_weather_comic.json`)

Fortgeschrittener 3-Panel Comic Strip mit Area Composition -- jedes Panel zeigt eine andere Szene.

**Die 3 Panels:**

| Panel | Position | Inhalt |
|---|---|---|
| **Panel 1** | Links | Kira grüßt -- "Guten Morgen!" |
| **Panel 2** | Mitte | Wetter-Anzeige mit Symbolen |
| **Panel 3** | Rechts | Kira's Outfit-Tipp für den Tag |

**Workflow-Aufbau:**
```
CheckpointLoader → 4x CLIPTextEncode (Base + 3 Panels)
                  → 3x ConditioningSetArea (Panel Layout)
                  → 3x ConditioningCombine (Zusammenführen)
                  → KSampler → VAEDecode → SaveImage
```

## Wetter-Prompts Anpassen

Passe die Prompts je nach aktuellem Wetter an. Hier sind Vorlagen:

### Sonnig & Warm (Frühling/Sommer)
```
cute anime girl Kira with short pink hair, green eyes, wearing light
spring outfit with sunglasses, cheerful smile, bright sunny sky, golden
sunlight, cherry blossoms, German city background, comic art style
```

### Bewölkt & Mild
```
cute anime girl Kira with short pink hair, green eyes, wearing cozy
cardigan, gentle smile, overcast sky with soft clouds, mild autumn day,
colorful leaves, German town square background, comic art style
```

### Regnerisch
```
cute anime girl Kira with short pink hair, green eyes, holding a colorful
umbrella, playful expression, rain drops, puddles reflecting city lights,
cozy atmosphere, German street with cafes, comic art style
```

### Winterlich & Kalt
```
cute anime girl Kira with short pink hair, green eyes, wearing warm
winter coat scarf and beanie, rosy cheeks, snowy landscape, snowflakes
falling, Christmas market background, German half-timbered houses,
warm lighting, comic art style
```

### Stürmisch
```
cute anime girl Kira with short pink hair, green eyes, windswept hair,
holding onto hat, dramatic stormy sky, strong wind effects, autumn
leaves blowing, German city background, dynamic pose, comic art style
```

## Tägliche Wetter-Informationen Einbauen

Um das aktuelle Wetter einzubauen, passe den Prompt mit diesen Elementen an:

1. **Temperatur-Bereich** -- Wähle Kiras Outfit passend zur Temperatur
2. **Wetter-Symbole** -- Füge `sun icon`, `cloud icon`, `rain drops` etc. zum Prompt hinzu
3. **Jahreszeit** -- Passe den Hintergrund an (Kirschblüten, bunte Blätter, Schnee)
4. **Tageszeit** -- `morning golden light`, `afternoon sun`, `evening warm glow`

### Beispiel: Frühlingshafter Tag (12-18°C, sonnig)

```
comic book art style, cute anime girl Kira with short pink hair and
bright green eyes, wearing a stylish light spring jacket and sunglasses
on head, cheerful confident pose, sunny sky with a few fluffy clouds,
thermometer showing warm spring temperature, spring flowers blooming,
German city panorama with church spires, cherry blossom petals floating,
speech bubble, manga style, vibrant colors, high quality comic art
```

## Empfohlene Modelle

- **SDXL 1.0** (`sd_xl_1.0.safetensors`) -- Standard, gute Qualität
- **Animagine XL** -- Spezialisiert auf Anime-Stil
- **CounterfeitXL** -- Hochwertige Anime/Manga Ausgabe

## Tipps für die lokale Zielgruppe

- Füge lokale Wahrzeichen in den Hintergrund ein (z.B. `Cologne Cathedral`, `Brandenburg Gate`)
- Nutze deutsche Jahreszeit-Elemente (Weihnachtsmarkt, Maifest, Biergarten)
- Poste den Comic morgens zwischen 6-8 Uhr auf Social Media
- Ergänze den generierten Comic mit Text-Overlays für Temperatur und Wochentag
- Verwende konsistente Seeds für wiedererkennbaren Kira-Stil
