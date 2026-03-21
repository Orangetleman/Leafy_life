import flet as ft
import flet.canvas as cv
from pynput import keyboard as pynput_keyboard
from datacenter import *
from shopHome import _build_shop_home
from style import *
import asyncio
import threading
import random

# Charge la musique
'''
import pyglet
music = pyglet.media.load("assets/musics/frogmusic.wav", streaming=False)
music_player = pyglet.media.Player()
music_player.queue(music)
music_player.loop = True
music_player.play()
threading.Thread(target=pyglet.app.run, daemon=True).start()
'''

biomes_state = {
    "pp":       True,
    "ff":       False,
    "mm":       False,
    "ll":       False,
    "plaine":   True,
    "foret":    False,
    "montagne": False,
    "lac":      False,
}

scene_actu = [0]

# ── Config biomes : (img_w_original, img_h_original, ground_ratio_depuis_le_bas) ─────────
BIOME_LAYOUT = {
    "plain":    (10000, 5192, 601  / 2596),
    "forest":   (1888,  999,  100  / 333 ),
    "lake":     (1888,  999,  41   / 111 ),
    "mountain": (1888,  999,  31   / 111 ),
}

SPRITE_SPEED  = 30
SPRITE_W      = 150
ENTITY_MARGIN = 80

# ── Planète : dimensions originales de l'image ───────────────────────────────────────────
PLANET_IMG_W = 439
PLANET_IMG_H = 435

# ── Points d'ancrage sur l'image planète (px dans l'image originale 439x435) ────────────
# Ces coordonnées sont depuis le coin HAUT GAUCHE de l'image
BIOME_ANCHORS = {
    "plain":    (130, 320),
    "forest":   (300, 280),
    "mountain": (300, 80),
    "lake":     (100, 160),
}

# Clé biomes_state → clé BIOME_ANCHORS
BIOME_KEY_MAP = {
    "plaine":   "plain",
    "foret":    "forest",
    "montagne": "mountain",
    "lac":      "lake",
}

# Distance du bord de la fenêtre pour les boutons
BUTTON_MARGIN_X = 40
BUTTON_MARGIN_Y = 40
BTN_H = 50  # hauteur boutons de navigation entre biomes

# Taille affichée de la planète (la même image pour tous, mise à l'échelle dynamiquement)
# La planète s'affiche dans un Container expand=True centré → on calcule sa taille réelle
# en fonction de la page via min(page_w, page_h) * PLANET_DISPLAY_RATIO
PLANET_DISPLAY_RATIO = 0.55   # la planète occupe ~55% du plus petit côté de la fenêtre


def compute_layout(page_w, page_h, biome_name):
    """
    fit=CONTAIN : scale = min(page_w/img_w, page_h/img_h)
    L'image entière est visible, centrée.

    Retour : scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h
    - scale      : facteur d'agrandissement
    - offset_x   : marge gauche (et droite) en px-page entre bord page et bord image
    - offset_y   : marge haut (et bas) en px-page entre bord page et bord image
    - ground_bot : px depuis le bas de la PAGE jusqu'au sol de l'image
    - img_disp_w : largeur de l'image affichée en px-page
    - img_disp_h : hauteur de l'image affichée en px-page
    """
    img_w, img_h, ground_ratio = BIOME_LAYOUT.get(biome_name, (1250, 649, 601 / 2596))
    scale      = min(page_w / img_w, page_h / img_h)
    img_disp_w = img_w * scale
    img_disp_h = img_h * scale
    offset_x   = (page_w - img_disp_w) / 2.0
    offset_y   = (page_h - img_disp_h) / 2.0
    ground_bot = offset_y + img_disp_h * ground_ratio
    return scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h


def compute_planet_layout(page_w, page_h):
    """
    Retourne (planet_disp_w, planet_disp_h, planet_left, planet_top)
    — taille et position de l'image planète dans la page.
    """
    size         = min(page_w, page_h) * PLANET_DISPLAY_RATIO
    planet_disp_w = size * (PLANET_IMG_W / max(PLANET_IMG_W, PLANET_IMG_H))
    planet_disp_h = size * (PLANET_IMG_H / max(PLANET_IMG_W, PLANET_IMG_H))
    planet_left  = (page_w - planet_disp_w) / 2.0
    planet_top   = (page_h - planet_disp_h) / 2.0
    return planet_disp_w, planet_disp_h, planet_left, planet_top


def compute_button_pos(biome_key, page_w, page_h):
    """
    Retourne (left, top, bottom, right) pour le Container du bouton.
    Seuls left/bottom ou right/top sont définis selon le coin.
    """
    corners = {
        "plaine":   "bottom_left",
        "foret":    "bottom_right",
        "montagne": "top_right",
        "lac":      "top_left",
    }
    corner = corners.get(biome_key, "bottom_left")
    if corner == "bottom_left":
        return {"left": BUTTON_MARGIN_X, "bottom": BUTTON_MARGIN_Y}
    elif corner == "bottom_right":
        return {"right": BUTTON_MARGIN_X, "bottom": BUTTON_MARGIN_Y}
    elif corner == "top_right":
        return {"right": BUTTON_MARGIN_X, "top": BUTTON_MARGIN_Y}
    elif corner == "top_left":
        return {"left": BUTTON_MARGIN_X, "top": BUTTON_MARGIN_Y}


def build_trail_canvas(page_w, page_h, active_biome_keys, button_refs):
    """
    Construit un Canvas SVG avec les traits courbes reliant les biomes actifs
    à leurs boutons respectifs.
    button_refs : dict biome_key → ft.Container du bouton (pour lire sa position)
    """
    planet_disp_w, planet_disp_h, planet_left, planet_top = compute_planet_layout(page_w, page_h)
    scale_x = planet_disp_w / PLANET_IMG_W
    scale_y = planet_disp_h / PLANET_IMG_H

    shapes = []
    for bk in active_biome_keys:
        anchor_key = BIOME_KEY_MAP.get(bk)
        if anchor_key not in BIOME_ANCHORS:
            continue

        ax, ay = BIOME_ANCHORS[anchor_key]
        px = planet_left + ax * scale_x
        py = planet_top  + ay * scale_y

        corner = {
            "plaine":   "bottom_left",
            "foret":    "bottom_right",
            "montagne": "top_right",
            "lac":      "top_left",
        }.get(bk, "bottom_left")

        if corner == "bottom_left":
            bx = BUTTON_MARGIN_X + 100
            by = page_h - BUTTON_MARGIN_Y - BTN_H / 2
        elif corner == "bottom_right":
            bx = page_w - BUTTON_MARGIN_X - 100
            by = page_h - BUTTON_MARGIN_Y - BTN_H / 2
        elif corner == "top_right":
            bx = page_w - BUTTON_MARGIN_X - 100
            by = BUTTON_MARGIN_Y + BTN_H / 2
        elif corner == "top_left":
            bx = BUTTON_MARGIN_X + 100
            by = BUTTON_MARGIN_Y + BTN_H / 2

        # Point de contrôle de Bézier légèrement décalé vers le centre de la page
        cx_ = (px + bx) / 2 + (page_w / 2 - (px + bx) / 2) * 0.65
        cy_ = (py + by) / 2 + (page_h / 2 - (py + by) / 2) * 0.01

        shapes.append(cv.Path(
            [
                cv.Path.MoveTo(px, py),
                cv.Path.QuadraticTo(cx_, cy_, bx, by),
            ],
            paint=ft.Paint(
                stroke_width=3,
                color="#ffffff",
                style=ft.PaintingStyle.STROKE,
            ),
        ))
        shapes.append(cv.Circle(
            x=bx, y=by, radius=5,
            paint=ft.Paint(color="#ffffff", style=ft.PaintingStyle.FILL),
        ))
        shapes.append(cv.Circle(
            x=px, y=py, radius=5,
            paint=ft.Paint(color="#ffffff", style=ft.PaintingStyle.FILL),
        ))

    return cv.Canvas(
        shapes=shapes,
        width=page_w,
        height=page_h,
    )


def _planet(page: ft.Page, navigate) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    keys_pressed    = {"right": False, "left": False, "space": False}
    dialogue_active = [False]
    running         = [True]
    focused         = [True]

    def on_press(key):
        if not focused[0] or dialogue_active[0]:
            return
        try:
            if key.char in ("d", "D"):   keys_pressed["right"] = True
            elif key.char in ("q", "Q"): keys_pressed["left"]  = True
        except AttributeError:
            if   key == pynput_keyboard.Key.right: keys_pressed["right"] = True
            elif key == pynput_keyboard.Key.left:  keys_pressed["left"]  = True
            elif key == pynput_keyboard.Key.space: keys_pressed["space"] = True

    def on_release(key):
        try:
            if key.char in ("d", "D"):   keys_pressed["right"] = False
            elif key.char in ("q", "Q"): keys_pressed["left"]  = False
        except AttributeError:
            if   key == pynput_keyboard.Key.right: keys_pressed["right"] = False
            elif key == pynput_keyboard.Key.left:  keys_pressed["left"]  = False
            elif key == pynput_keyboard.Key.space: keys_pressed["space"] = False

    def on_window_event(e):
        if e.type == ft.WindowEventType.FOCUS:
            focused[0] = True
        elif e.type == ft.WindowEventType.BLUR:
            focused[0] = False
            keys_pressed["right"] = False
            keys_pressed["left"]  = False
    page.window.on_event = on_window_event

    def dialogue(e, scene, dialogue_active, on_end=None):
        i_scene = [0]
        dialogue_active[0] = True

        def next_dialogue(key):
            if key == pynput_keyboard.Key.space:
                if i_scene[0] < len(scene) - 1:
                    i_scene[0] += 1
                    if i_scene[0] % 2 == 0:
                        npc_msg.content.value = scene[i_scene[0]]
                        chara_msg.visible = False
                        npc_msg.visible   = True
                    else:
                        chara_msg.content.value = scene[i_scene[0]]
                        chara_msg.visible = True
                        npc_msg.visible   = False
                    page.run_thread(page.update)
                else:
                    dialogue_box.visible = False
                    dialogue_active[0]   = False
                    page.run_thread(page.update)
                    def finish():
                        listener.stop()
                        if on_end:
                            on_end()
                    threading.Thread(target=finish, daemon=True).start()

        msg = scene[i_scene[0]]
        chara_msg = ft.Container(
            content=ft.Text(msg, size=PLANET_DIALOGUE_TEXT_SIZE),
            bgcolor=ft.Colors.with_opacity(PLANET_DIALOGUE_BG_COLOR[0], PLANET_DIALOGUE_BG_COLOR[1]),
            alignment=ft.Alignment.CENTER_RIGHT,
            height=PLANET_DIALOGUE_HEIGHT,
            visible=False,
        )
        npc_msg = ft.Container(
            content=ft.Text(msg, size=PLANET_DIALOGUE_TEXT_SIZE),
            bgcolor=ft.Colors.with_opacity(PLANET_DIALOGUE_BG_COLOR[0], PLANET_DIALOGUE_BG_COLOR[1]),
            alignment=ft.Alignment.CENTER_LEFT,
            height=PLANET_DIALOGUE_HEIGHT,
            visible=True,
        )
        dialogue_box = ft.Container(
            content=ft.Stack([chara_msg, npc_msg]),
            alignment=ft.Alignment.BOTTOM_CENTER,
        )
        listener = pynput_keyboard.Listener(on_press=next_dialogue)
        listener.start()
        return dialogue_box

    # ── Écran planète ─────────────────────────────────────────────────────────────────────
    def build_planet_screen():
        """Construit et retourne le Stack de l'écran planète."""
        pw = page.width  or 800
        ph = (page.height or 600) - getattr(page, "navbar_height", 60)

        planet_disp_w, planet_disp_h, planet_left, planet_top = compute_planet_layout(pw, ph)

        # Image planète selon l'état des biomes
        if   biomes_state["ll"]: planet_src = "assets/imgs/icons/biome_lake.png"
        elif biomes_state["mm"]: planet_src = "assets/imgs/icons/biome_mountain.png"
        elif biomes_state["ff"]: planet_src = "assets/imgs/icons/biome_forest.png"
        else:                    planet_src = "assets/imgs/icons/biome_plain.png"

        planet_img = ft.Container(
            content=ft.Image(src=planet_src, width=planet_disp_w, height=planet_disp_h, fit="fill"),
            left=planet_left,
            top=planet_top,
        )

        # Traits SVG
        active_biome_keys = [bk for bk in ["plaine", "foret", "montagne", "lac"] if biomes_state[bk]]
        trail_canvas_obj  = build_trail_canvas(pw, ph, active_biome_keys, {})

        # Boutons
        btn_containers = []
        for bk in ["plaine", "foret", "montagne", "lac"]:
            if not biomes_state[bk]:
                continue
            biome_str = {"plaine": "plain", "foret": "forest", "montagne": "mountain", "lac": "lake"}[bk]
            label     = {"plaine": "explore plaine", "foret": "explore foret",
                        "montagne": "explore montagne", "lac": "explore lac"}[bk]
            pos = compute_button_pos(bk, pw, ph)
            btn = ft.Container(
                content=ft.ElevatedButton(
                    ft.Text(label, size=20, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR),
                    on_click=lambda e, b=biome_str: tp(e, b),
                    bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR,
                ),
                height=BTN_H,
                **pos, # Développe le dictionnaire pour attribuer les caractéristiques de pos au Container
            )
            btn_containers.append(btn)

        children = [planet_img, trail_canvas_obj] + btn_containers
        return ft.Stack(children, expand=True)

    # ─────────────────────────────────────────────────────────────────────────────────────
    def tp(e, biome):
        page.on_resize = None
        page.clean()
        running[0]            = True
        event                 = random.choice(EVENTS)
        biome_icon            = next(b["icon"] for b in BIOMES if b["name"] == biome)
        keys_pressed["space"] = False
        dialogue_active[0]    = False

        scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h = \
            compute_layout(page.width, page.height, biome)

        layout = {
            "offset_x":   offset_x,
            "offset_y":   offset_y,
            "ground_bot": ground_bot,
            "img_disp_w": img_disp_w,
        }

        bg_img = ft.Image(src=biome_icon, width=img_disp_w, height=img_disp_h, fit="fill")
        bg     = ft.Container(content=bg_img, left=offset_x, top=offset_y)

        sprite_ratio  = [0.5]
        sprite_page_x = [offset_x + img_disp_w * sprite_ratio[0]]

        new_sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=SPRITE_W, height=180),
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )
        new_sprite.bottom = ground_bot
        new_sprite.left   = sprite_page_x[0]

        entity_id        = None
        entity_container = None
        entity_side_left = random.choice([True, False])

        ENEMY_W, ENEMY_H = 120, 140
        NPC_W,   NPC_H   = 100, 120
        EMPTY_W, EMPTY_H = 120, 100

        def _make_entity(src, w, h, visible=True):
            return ft.Container(content=ft.Image(src=src, width=w, height=h), visible=visible)

        if event == "enemy":
            entity_id        = random.choice(ENEMIES)
            entity_container = _make_entity(entity_id["visual"], ENEMY_W, ENEMY_H)
            entity_w         = ENEMY_W
        elif event == "npc":
            entity_id        = random.choice(NPCS)
            entity_container = _make_entity(entity_id["visual"], NPC_W, NPC_H)
            entity_w         = NPC_W
        elif event == "empty":
            entity_id        = random.choice(OBJECTS)
            entity_container = _make_entity(entity_id["visual"], EMPTY_W, EMPTY_H)
            entity_w         = EMPTY_W
        else:
            entity_id        = LORE[scene_actu[0]]["visual"] if scene_actu[0] < len(LORE) else "assets/imgs/icons/leaf.png"
            entity_container = _make_entity(entity_id, NPC_W, NPC_H)
            entity_w         = NPC_W

        if entity_side_left:
            entity_ratio = ENTITY_MARGIN / img_disp_w
        else:
            entity_ratio = 1.0 - (ENTITY_MARGIN + entity_w) / img_disp_w

        entity_page_x = offset_x + img_disp_w * entity_ratio
        entity_container.bottom = ground_bot
        entity_container.left   = entity_page_x

        bouton_retour = ft.Container(
            content=ft.Row([ft.Container(
                content=ft.Text("planète", size=20, color=PLANET_BACK_BUTTON_TEXT_COLOR),
                bgcolor=PLANET_BACK_BUTTON_BG_COLOR,
                padding=10,
                border_radius=PLANET_BACK_BUTTON_BORDER_RADIUS,
                on_click=retourneur,
            )], alignment=ft.Alignment.TOP_LEFT),
        )

        preset = [bg, entity_container, new_sprite, bouton_retour]

        def update_layout(w, h):
            s, ox, oy, g, dw, dh = compute_layout(w, h, biome)
            layout.update({"offset_x": ox, "offset_y": oy, "ground_bot": g, "img_disp_w": dw})
            bg_img.width  = dw
            bg_img.height = dh
            bg.left = ox
            bg.top  = oy
            sprite_page_x[0] = ox + dw * sprite_ratio[0]
            new_sprite.bottom = g
            new_sprite.left   = sprite_page_x[0]
            entity_container.bottom = g
            entity_container.left   = ox + dw * entity_ratio

        def on_resize(ev):
            update_layout(ev.width, ev.height)
            page.update()

        page.on_resize = on_resize

        new_listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
        new_listener.start()

        def stop_tp_screen(ev=None):
            running[0]     = False
            page.on_resize = None
            new_listener.stop()

        page.stop_current_screen = stop_tp_screen
        page.window.on_event     = on_window_event

        first_sip = [True]

        async def tp_game_loop():
            while running[0]:
                moved = False
                if not dialogue_active[0]:
                    if keys_pressed["right"]:
                        sprite_page_x[0] += SPRITE_SPEED
                        moved = True
                    if keys_pressed["left"]:
                        sprite_page_x[0] -= SPRITE_SPEED
                        moved = True

                ox = layout["offset_x"]
                dw = layout["img_disp_w"]
                px = sprite_page_x[0]

                img_left  = ox
                img_right = ox + dw

                if dw > 0:
                    sprite_ratio[0] = (px - ox) / dw

                if px <= img_left:
                    stop_tp_screen(); tp(e, biome); return
                if px + SPRITE_W >= img_right:
                    stop_tp_screen(); tp(e, biome); return
                if scene_actu[0] == 0:
                    stop_tp_screen(); declenche_scene(e, biome, scene_actu[0]); return
                if event == "lore" and scene_actu[0] >= len(LORE):
                    if "lore" in EVENTS: EVENTS.remove("lore")
                    stop_tp_screen(); tp(e, biome); return

                ent_px = ox + dw * entity_ratio
                near   = abs(px - ent_px) < 170

                if event == "npc" and near and keys_pressed["space"]:
                    stop_tp_screen(); keys_pressed["space"] = False; shop(e, biome); return
                if event == "enemy" and near and keys_pressed["space"]:
                    stop_tp_screen(); keys_pressed["space"] = False; combat(e, biome, entity_id); return
                if event == "empty" and near and keys_pressed["space"]:
                    if first_sip[0] and entity_id["gives"] == "Eau minérale":
                        inventory_manager.append_item(ITEMS[1], 3)
                        first_sip[0] = False
                        entity_container.visible = False
                        page.update()
                    keys_pressed["space"] = False
                if event == "lore" and near and keys_pressed["space"]:
                    keys_pressed["space"] = False; stop_tp_screen(); declenche_scene(e, biome, scene_actu[0]); return

                if moved:
                    new_sprite.left = sprite_page_x[0]
                    page.update()

                await asyncio.sleep(0.025)

        page.add(ft.Stack(preset, expand=True))
        page.run_task(tp_game_loop)

    # ─────────────────────────────────────────────────────────────────────────────────────
    def shop(e, biome):
        page.clean()
        page.on_resize = None
        def on_back(ev):
            page.clean()
            tp(ev, biome)
        shop_ui = _build_shop_home(page, "wandering", biome, on_back=on_back)
        page.add(ft.Container(content=ft.Column(controls=shop_ui, expand=True), expand=True, padding=0))

    def combat(e, biome, enemy):
        page.clean()
        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)
        scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h = compute_layout(page.width, page.height, biome)
        bg_img = ft.Image(src=biome_icon, width=img_disp_w, height=img_disp_h, fit="fill")
        bg     = ft.Container(content=bg_img, left=offset_x, top=offset_y)
        leaf_page_x  = offset_x + img_disp_w * 0.10
        enemy_page_x = offset_x + img_disp_w * 0.90 - SPRITE_W
        leafsprite = ft.Container(content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=SPRITE_W, height=180), bottom=ground_bot, left=leaf_page_x)
        enemysprite = ft.Container(content=ft.Image(src=enemy["visual"], width=SPRITE_W, height=180), bottom=ground_bot, left=enemy_page_x)
        menu = ft.Container(bottom=0, left=0, width=page.width, height=page.height * PLANET_COMBAT_MENU_HEIGHT_RATIO,
                            bgcolor=ft.Colors.with_opacity(PLANET_COMBAT_MENU_BG_COLOR[0], PLANET_COMBAT_MENU_BG_COLOR[1]))
        """CHRIS A AJOUTER BOUTONS (atk, competence, boite_leaf) + BARRE PV ET INFOS LEAF"""
        preset = [bg, leafsprite, enemysprite, menu]
        def on_resize_combat(ev):
            s, ox, oy, g, dw, dh = compute_layout(ev.width, ev.height, biome)
            bg_img.width = dw; bg_img.height = dh; bg.left = ox; bg.top = oy
            leafsprite.bottom = g;  leafsprite.left  = ox + dw * 0.10
            enemysprite.bottom = g; enemysprite.left = ox + dw * 0.90 - SPRITE_W
            page.update()
        page.on_resize = on_resize_combat
        page.add(ft.Stack(preset, expand=True))

    def atk(leaf, enemy):
        malus = f"-{leaf.atk}"
        dgts  = ft.Container(ft.Text(malus, size=20), visible=True)
        leaf.left = page.width - 20; page.update(); page.add(dgts)
        dgts.visible = False; leaf.left = 20; page.update()
        enemy["hp"] -= leaf.atk

    def competence(leaf, enemy):
        if leaf.type == 1:
            leaf.atk_boost = leaf.atk; atk(leaf, enemy); leaf.atk_boost = 0
        elif leaf.type == 3:
            page.add(ft.Container(ft.Image(src="assets/imgs/icons/leaf_type_tank.png", width=100, height=100), visible=True))
            enemy["atk"] = max(1, enemy["atk"] // 2); return 2
        return None

    def open_leaf_selection_interface():
        pass
    """CHRISSS FAIS ICI"""

    # ─────────────────────────────────────────────────────────────────────────────────────
    def declenche_scene(e, biome, n):
        if hasattr(page, "stop_current_screen"):
            page.stop_current_screen()
        """if scene_actu[0] >= len(LORE):
            tp(e, biome); return
        dialogue_active[0] = True
        
        page.clean()
        
        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)
        locuteur   = LORE[n]["visual"]
        
        scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h = compute_layout(page.width, page.height, biome)
        
        bg_img     = ft.Image(src=biome_icon, width=img_disp_w, height=img_disp_h, fit="fill")
        bg         = ft.Container(content=bg_img, left=offset_x, top=offset_y)
        sprite     = ft.Container(content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=SPRITE_W, height=180),
                                  bottom=ground_bot, left=offset_x + img_disp_w * 0.10)
        npc_sprite = ft.Container(content=ft.Image(src=locuteur, width=SPRITE_W, height=180),
                                  bottom=ground_bot, left=offset_x + img_disp_w * 0.90 - SPRITE_W)
        
        def on_resize_scene(ev):
            s, ox, oy, g, dw, dh = compute_layout(ev.width, ev.height, biome)
            bg_img.width = dw; bg_img.height = dh; bg.left = ox; bg.top = oy
            sprite.bottom = g;     sprite.left     = ox + dw * 0.10
            npc_sprite.bottom = g; npc_sprite.left = ox + dw * 0.90 - SPRITE_W
            page.update()
            
        page.on_resize = on_resize_scene
        
        def on_end():
            page.on_resize = None
            scene_actu[0] += 1
            if scene_actu[0] == 2:
                biomes_state["pp"] = False; biomes_state["foret"] = True; biomes_state["ff"] = True
            if scene_actu[0] == 3:
                biomes_state["ff"] = False; biomes_state["montagne"] = True; biomes_state["mm"] = True
            if scene_actu[0] == 4:
                biomes_state["mm"] = False; biomes_state["lac"] = True; biomes_state["ll"] = True
            if not LORE[n]["combat"]:
                if LORE[n]["add"] is not None:
                    leafmanager.add_leaf(LEAFS[LORE[n]["add"]])
                if scene_actu[0] in (2, 3, 4):
                    navigate("planet")
                else:
                    tp(e, biome)
            else:
                enemy = next(b for b in ENEMIES if b["visual"] == locuteur)
                combat(e, biome, enemy)
        
        paroles = dialogue(e, LORE[n]["dialogue"], dialogue_active, on_end=on_end)
        page.add(ft.Stack([bg, npc_sprite, sprite, paroles], expand=True))"""
        if scene_actu[0]>=len(LORE):
            tp(e,biome)
        else:
            dialogue_active[0] = True
            page.clean()

            biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)
            locuteur   = LORE[n]["visual"]
            if not LORE[n]["combat"]:
                entity = next(b for b in LEAFS.values() if b["img"] == locuteur)
            else:
                entity = next(b for b in ENEMIES if b["visual"] == locuteur)

            scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h = compute_layout(page.width, page.height, biome)

            bg_img = ft.Image(src=biome_icon, width=img_disp_w, height=img_disp_h, fit="fill")
            bg     = ft.Container(content=bg_img, left=offset_x, top=offset_y)

            sprite = ft.Container(
                content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=SPRITE_W, height=180),
                bottom=ground_bot,
                left=offset_x + img_disp_w * 0.10,
            )
            npc_sprite = ft.Container(
                content=ft.Image(src=locuteur, width=SPRITE_W, height=180),
                bottom=ground_bot,
                left=offset_x + img_disp_w * 0.90 - SPRITE_W,
            )

            def on_resize_scene(ev):
                s, ox, oy, g, dw, dh = compute_layout(ev.width, ev.height, biome)
                bg_img.width  = dw
                bg_img.height = dh
                bg.left = ox
                bg.top  = oy
                sprite.bottom     = g
                sprite.left       = ox + dw * 0.10
                npc_sprite.bottom = g
                npc_sprite.left   = ox + dw * 0.90 - SPRITE_W
                page.update()

            page.on_resize = on_resize_scene

            def on_end():
                page.on_resize = None
                
                boite = explique(entity)
                if boite is not None:
                    page.overlay.append(boite)
                    page.update()
                    def toi(key):
                        if key == pynput_keyboard.Key.space:
                            listener.stop()
                            page.overlay.remove(boite)
                            page.update()
                            suite()
                    listener = pynput_keyboard.Listener(on_press=toi)
                    listener.start()
                else:
                    suite()

            def suite():
                scene_actu[0] += 1
                if scene_actu[0] == 2:
                    biomes_state["pp"]     = False
                    biomes_state["foret"]  = True
                    biomes_state["ff"]     = True
                    biomes_state["f2"]     = True

                if scene_actu[0] == 3:
                    biomes_state["ff"]       = False
                    biomes_state["montagne"] = True
                    biomes_state["mm"]       = True
                    biomes_state["f3"]       = True

                if scene_actu[0] == 4:
                    biomes_state["mm"]  = False
                    biomes_state["lac"] = True
                    biomes_state["ll"]  = True
                    biomes_state["f4"]  = True

                if not LORE[n]["combat"]:
                    if LORE[n]["add"] != None:
                        leafmanager.add_leaf(LEAFS[LORE[n]["add"]])
                    if scene_actu[0] in (2, 3, 4):
                        navigate("planet")
                    else:
                        tp(e, biome)
                else:
                    enemy = next(b for b in ENEMIES.values() if b["visual"] == locuteur)
                    combat(e, biome, enemy)

            paroles = dialogue(e, LORE[n]["dialogue"], dialogue_active, on_end=on_end)
            preset  = [bg, npc_sprite, sprite, paroles]
            page.add(ft.Stack(preset, expand=True))

    def explique(entity):
        if entity["met"] == False:
            boite = ft.Container(
                content=ft.Text(entity["prez"], size=20, color="white"),
                bgcolor='black',
                alignment=ft.Alignment.CENTER_LEFT,
                height=page.height,   
                width=page.width * 0.5,      
                padding=20,
                border=ft.border.all(3, "green"),
                border_radius=ft.border_radius.all(20),
            )
            entity["met"] = True
            return boite
        else:
            return None
    # ─────────────────────────────────────────────────────────────────────────────────────
    def retourneur(e):
        page.on_resize = None
        page.clean()
        navigate("planet")

    # Construit l'écran planète initial et branche le resize
    initial_stack = build_planet_screen()

    def on_planet_resize(ev):
        new_stack = build_planet_screen()
        if hasattr(page, "body_container"):
            page.body_container.content = ft.Column(controls=[new_stack], expand=True)
            page.update()
        else:
            page.controls.clear()
            page.add(new_stack)
            page.update()

    page.on_resize = on_planet_resize

    return initial_stack