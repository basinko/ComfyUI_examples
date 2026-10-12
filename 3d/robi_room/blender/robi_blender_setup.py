"""RoBi für Blender (getestet mit Blender 5.0).

So benutzt du das Skript:
  1. Lade den kompletten Ordner "blender" herunter (robi.glb, robi_zimmer.glb, gesichter/, dieses Skript).
  2. Blender öffnen → Arbeitsbereich "Scripting" → Öffnen → robi_blender_setup.py → Skript ausführen (▶).
  3. Im 3D-Viewport mit N die Seitenleiste öffnen → Reiter "RoBi".
     Dort wählst du Aktion und Ausdruck. "Ausdruck keyen" setzt einen Keyframe für den aktuellen Frame.

Was das Skript macht:
  - importiert Zimmer und RoBi (glTF, Y-up wird automatisch zu Blender Z-up)
  - legt die 9 Animationen als Aktionen an (Stehen, Winken, Daumen hoch, Zeigen, Laufen, Springen, Sitzen, Arbeiten, Nachdenken)
  - baut ein leuchtendes Display-Material; der Ausdruck kommt aus der Eigenschaft RoBi["Ausdruck"] (1–12) und ist keyframebar
    (Objekt → Eigenschaften → Benutzerdefiniert → Ausdruck, oder über die Seitenleiste)
  - setzt Lampenlichter, Fensterlicht, Gesichtsglühen, Welt, isometrische Kamera und Render-Einstellungen
"""
import bpy, os, math

# ---------------------------------------------------------------- Ordner finden
def _folder():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        pass
    sd = getattr(bpy.context, "space_data", None)
    if sd and getattr(sd, "text", None) and sd.text.filepath:
        return os.path.dirname(bpy.path.abspath(sd.text.filepath))
    raise RuntimeError("Ordner nicht gefunden: Bitte das Skript über Öffnen laden, nicht einfügen.")

FOLDER = _folder()
AKTIONEN = ["Stehen", "Winken", "Daumen_hoch", "Zeigen", "Laufen", "Springen", "Sitzen", "Arbeiten", "Nachdenken"]
AUSDRUECKE = ["Neutral", "Freundlich", "Lachend", "Überrascht", "Genervt", "Wütend",
              "Nachdenklich", "Skeptisch", "Traurig", "Aufgeregt", "Zwinkernd", "Verunsichert"]
FPS = 30


def three_to_blender(x, y, z):
    """three.js (Y-up) → Blender (Z-up)."""
    return (x, -z, y)


def import_into(path, coll_name):
    coll = bpy.data.collections.get(coll_name) or bpy.data.collections.new(coll_name)
    if coll.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(coll)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)
    return new


# ---------------------------------------------------------------- Import
scene = bpy.context.scene
scene.render.fps = FPS
room_objs = import_into(os.path.join(FOLDER, "robi_zimmer.glb"), "Zimmer")
robi_objs = import_into(os.path.join(FOLDER, "robi.glb"), "RoBi")
root = next(o for o in robi_objs if o.name.startswith("RoBi"))
kopf = next(o for o in robi_objs if o.name.startswith("Kopf"))
display = next(o for o in robi_objs if o.name.startswith("Display"))

# Aktionen behalten, gestapelte NLA-Spuren des Importers entfernen (sonst mischen sie sich ein)
for name in AKTIONEN:
    act = bpy.data.actions.get(name)
    if act:
        act.use_fake_user = True
for o in robi_objs:
    ad = o.animation_data
    if ad:
        for tr in list(ad.nla_tracks):
            ad.nla_tracks.remove(tr)


def set_aktion(name):
    act = bpy.data.actions.get(name)
    if not act:
        return
    for o in robi_objs:
        slot = act.slots.get("OB" + o.name)
        if not slot:
            continue
        ad = o.animation_data or o.animation_data_create()
        ad.action = act
        ad.action_slot = slot
    scene.frame_start = 1
    scene.frame_end = max(2, int(round(act.frame_range[1])))


# ---------------------------------------------------------------- Display-Material
root["Ausdruck"] = 1
ui = root.id_properties_ui("Ausdruck")
ui.update(min=1, max=12, description=" · ".join(f"{i + 1} {n}" for i, n in enumerate(AUSDRUECKE)))

# 12 Gesichtstexturen; der Shader wählt per Attribut "Ausdruck" (Objekt-Eigenschaft des Displays) eine davon aus
mat = bpy.data.materials.new("RoBi_Display")
mat.use_nodes = True
nt = mat.node_tree
nt.nodes.clear()
N = nt.nodes.new
attr = N("ShaderNodeAttribute"); attr.attribute_type = "OBJECT"; attr.attribute_name = "Ausdruck"; attr.location = (-1100, 300)
# glTF-UVs und Canvas-Bilder zählen die Zeilen in entgegengesetzter Richtung → V spiegeln
uvn = N("ShaderNodeTexCoord"); uvn.location = (-1350, 0)
mp = N("ShaderNodeMapping"); mp.location = (-1150, 0)
mp.inputs["Location"].default_value[1] = 1.0; mp.inputs["Scale"].default_value[1] = -1.0
nt.links.new(uvn.outputs["UV"], mp.inputs["Vector"])
col_sum = alpha_sum = None
for i in range(12):
    img = bpy.data.images.load(os.path.join(FOLDER, "gesichter", f"gesicht_{i + 1:03d}.png"), check_existing=True)
    tex = N("ShaderNodeTexImage"); tex.image = img; tex.name = f"Gesicht_{i + 1}"; tex.label = AUSDRUECKE[i]
    tex.location = (-900, -i * 280)
    nt.links.new(mp.outputs["Vector"], tex.inputs["Vector"])
    cmp = N("ShaderNodeMath"); cmp.operation = "COMPARE"; cmp.location = (-650, -i * 280 + 120)
    nt.links.new(attr.outputs["Fac"], cmp.inputs[0]); cmp.inputs[1].default_value = i + 1; cmp.inputs[2].default_value = 0.5
    sc = N("ShaderNodeVectorMath"); sc.operation = "SCALE"; sc.location = (-450, -i * 280)
    nt.links.new(tex.outputs["Color"], sc.inputs[0]); nt.links.new(cmp.outputs[0], sc.inputs["Scale"])
    am = N("ShaderNodeMath"); am.operation = "MULTIPLY"; am.location = (-450, -i * 280 - 140)
    nt.links.new(tex.outputs["Alpha"], am.inputs[0]); nt.links.new(cmp.outputs[0], am.inputs[1])
    if col_sum is None:
        col_sum, alpha_sum = sc.outputs[0], am.outputs[0]
    else:
        ca = N("ShaderNodeVectorMath"); ca.operation = "ADD"; ca.location = (-250, -i * 280)
        nt.links.new(col_sum, ca.inputs[0]); nt.links.new(sc.outputs[0], ca.inputs[1]); col_sum = ca.outputs[0]
        aa = N("ShaderNodeMath"); aa.operation = "ADD"; aa.location = (-250, -i * 280 - 140)
        nt.links.new(alpha_sum, aa.inputs[0]); nt.links.new(am.outputs[0], aa.inputs[1]); alpha_sum = aa.outputs[0]
emit = N("ShaderNodeEmission"); emit.inputs["Strength"].default_value = 1.5; emit.location = (0, -60)
transp = N("ShaderNodeBsdfTransparent"); transp.location = (0, 80)
mix = N("ShaderNodeMixShader"); mix.location = (220, 0)
out = N("ShaderNodeOutputMaterial"); out.location = (420, 0)
nt.links.new(col_sum, emit.inputs["Color"])
nt.links.new(alpha_sum, mix.inputs["Fac"])
nt.links.new(transp.outputs[0], mix.inputs[1])
nt.links.new(emit.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], out.inputs["Surface"])
display.data.materials.clear()
display.data.materials.append(mat)
# Das Display übernimmt den Wert von RoBi["Ausdruck"] per Treiber, damit man nur am RoBi-Objekt keyen muss
display["Ausdruck"] = 1
fcu = display.driver_add('["Ausdruck"]')
drv = fcu.driver
drv.type = "AVERAGE"
var = drv.variables.new(); var.name = "a"
var.targets[0].id_type = "OBJECT"; var.targets[0].id = root; var.targets[0].data_path = '["Ausdruck"]'

# ---------------------------------------------------------------- Licht
def add_light(name, kind, loc, energy, color, size=0.2, coll="Licht"):
    c = bpy.data.collections.get(coll) or bpy.data.collections.new(coll)
    if c.name not in scene.collection.children:
        scene.collection.children.link(c)
    data = bpy.data.lights.new(name, kind)
    data.energy = energy; data.color = color
    if kind in ("POINT", "SPOT"):
        data.shadow_soft_size = size
    ob = bpy.data.objects.new(name, data); ob.location = loc
    c.objects.link(ob)
    return ob

warm = (1.0, 0.72, 0.42)
add_light("Nachttisch_L", "POINT", three_to_blender(-2.25, 1.25, -3.35), 150, warm)
add_light("Nachttisch_R", "POINT", three_to_blender(1.85, 1.25, -3.35), 150, warm)
add_light("Schreibtisch", "POINT", three_to_blender(3.15, 1.69, -2.4), 110, warm)
win = add_light("Fenster", "AREA", (-3.85, 1.6, 2.6), 350, (0.8, 0.88, 1.0))
win.data.size = 2.2; win.rotation_euler = (0, math.radians(-90), 0)
key = add_light("Key_RoBi", "SPOT", three_to_blender(5, 7.5, 6), 2500, (1.0, 0.85, 0.7), size=0.6)
key.data.spot_size = math.radians(30); key.data.spot_blend = 0.6
tc = key.constraints.new("TRACK_TO"); tc.target = root; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
glow = add_light("Gesicht_Glow", "POINT", (0, 0, 0), 40, (1.0, 0.6, 0.16), size=0.4)
glow.parent = kopf; glow.location = (0, -1.6, -0.1)   # vor dem Display, im lokalen Raum des Kopfs

world = scene.world or bpy.data.worlds.new("Welt")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value = (0.02, 0.024, 0.03, 1); bg.inputs["Strength"].default_value = 1.0

# ---------------------------------------------------------------- Kamera (isometrisch)
cam_data = bpy.data.cameras.new("Iso_Kamera"); cam_data.type = "ORTHO"; cam_data.ortho_scale = 12.6
cam = bpy.data.objects.new("Iso_Kamera", cam_data); cam.location = (12, -12, 11)
scene.collection.objects.link(cam)
target = bpy.data.objects.new("Kamera_Ziel", None); target.location = (0, 0, 1.5)
scene.collection.objects.link(target)
ct = cam.constraints.new("TRACK_TO"); ct.target = target; ct.track_axis = "TRACK_NEGATIVE_Z"; ct.up_axis = "UP_Y"
scene.camera = cam

# ---------------------------------------------------------------- Render
for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
    try:
        scene.render.engine = eng
        break
    except TypeError:
        continue
scene.render.resolution_x = scene.render.resolution_y = 1080
scene.render.film_transparent = False

# ---------------------------------------------------------------- Seitenleiste "RoBi"
def _upd_aktion(self, ctx):
    set_aktion(self.robi_aktion)

def _upd_ausdruck(self, ctx):
    r = bpy.data.objects.get(root.name)
    if r:
        r["Ausdruck"] = int(self.robi_ausdruck)
        r.update_tag()
        ctx.scene.frame_set(ctx.scene.frame_current)

bpy.types.Scene.robi_aktion = bpy.props.EnumProperty(
    name="Aktion", items=[(n, n.replace("_", " "), "") for n in AKTIONEN], update=_upd_aktion)
bpy.types.Scene.robi_ausdruck = bpy.props.EnumProperty(
    name="Ausdruck", items=[(str(i + 1), n, "") for i, n in enumerate(AUSDRUECKE)], update=_upd_ausdruck)


class ROBI_OT_key_ausdruck(bpy.types.Operator):
    """Setzt einen Keyframe für den Ausdruck im aktuellen Frame"""
    bl_idname = "robi.key_ausdruck"
    bl_label = "Ausdruck keyen"

    def execute(self, ctx):
        r = bpy.data.objects.get(root.name)
        r.keyframe_insert(data_path='["Ausdruck"]', frame=ctx.scene.frame_current)
        for fc in (r.animation_data.action.fcurves if hasattr(r.animation_data.action, "fcurves") else []):
            if fc.data_path == '["Ausdruck"]':
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"
        return {"FINISHED"}


class ROBI_PT_panel(bpy.types.Panel):
    bl_label = "RoBi"
    bl_idname = "ROBI_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RoBi"

    def draw(self, ctx):
        col = self.layout.column(align=True)
        col.prop(ctx.scene, "robi_aktion")
        col.separator()
        col.prop(ctx.scene, "robi_ausdruck")
        col.operator("robi.key_ausdruck", icon="KEY_HLT")
        col.separator()
        col.label(text="Tipp: Leertaste spielt die Aktion ab.")


for cls in (ROBI_OT_key_ausdruck, ROBI_PT_panel):
    try:
        bpy.utils.unregister_class(cls)
    except RuntimeError:
        pass
    bpy.utils.register_class(cls)

scene.robi_aktion = "Stehen"
set_aktion("Stehen")
print("RoBi ist bereit: Seitenleiste (N) → Reiter 'RoBi'.")
