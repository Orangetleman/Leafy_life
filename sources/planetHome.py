import flet as ft
import flet.canvas as cv
from pynput import keyboard as pynput_keyboard
from datacenter import *
from shopHome import _build_shop_home
from style import *
import asyncio
import threading
import random


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

# ── Config biomes ─────────────────────────────────────────────────────────────────────────
BIOME_LAYOUT = {
    "plain":    (10000, 5192, 601  / 2596),
    "forest":   (1888,  999,  100  / 333 ),
    "lake":     (1888,  999,  41   / 111 ),
    "mountain": (1888,  999,  31   / 111 ),
}

SPRITE_SPEED  = 30
SPRITE_W      = 150
ENTITY_MARGIN = 80

# ── Planète ───────────────────────────────────────────────────────────────────────────────
PLANET_IMG_W = 439
PLANET_IMG_H = 435

BIOME_ANCHORS = {
    "plain":    (130, 320),
    "forest":   (300, 280),
    "mountain": (300, 80),
    "lake":     (100, 160),
}

BIOME_KEY_MAP = {
    "plaine":   "plain",
    "foret":    "forest",
    "montagne": "mountain",
    "lac":      "lake",
}

BUTTON_MARGIN_X    = 40
BUTTON_MARGIN_Y    = 40
BTN_H              = 50
PLANET_DISPLAY_RATIO = 0.55


# ─────────────────────────────────────────────────────────────────────────────────────────
def compute_layout(page_w, page_h, biome_name):
    img_w, img_h, ground_ratio = BIOME_LAYOUT.get(biome_name, (1250, 649, 601 / 2596))
    scale      = min(page_w / img_w, page_h / img_h)
    img_disp_w = img_w * scale
    img_disp_h = img_h * scale
    offset_x   = (page_w - img_disp_w) / 2.0
    offset_y   = (page_h - img_disp_h) / 2.0
    ground_bot = offset_y + img_disp_h * ground_ratio
    return scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h


def compute_planet_layout(page_w, page_h):
    size          = min(page_w, page_h) * PLANET_DISPLAY_RATIO
    planet_disp_w = size * (PLANET_IMG_W / max(PLANET_IMG_W, PLANET_IMG_H))
    planet_disp_h = size * (PLANET_IMG_H / max(PLANET_IMG_W, PLANET_IMG_H))
    planet_left   = (page_w - planet_disp_w) / 2.0
    planet_top    = (page_h - planet_disp_h) / 2.0
    return planet_disp_w, planet_disp_h, planet_left, planet_top


def compute_button_pos(biome_key, page_w, page_h):
    corners = {
        "plaine":   "bottom_left",
        "foret":    "bottom_right",
        "montagne": "top_right",
        "lac":      "top_left",
    }
    corner = corners.get(biome_key, "bottom_left")
    if corner == "bottom_left":  return {"left":  BUTTON_MARGIN_X, "bottom": BUTTON_MARGIN_Y}
    if corner == "bottom_right": return {"right": BUTTON_MARGIN_X, "bottom": BUTTON_MARGIN_Y}
    if corner == "top_right":    return {"right": BUTTON_MARGIN_X, "top":    BUTTON_MARGIN_Y}
    if corner == "top_left":     return {"left":  BUTTON_MARGIN_X, "top":    BUTTON_MARGIN_Y}


def build_trail_canvas(page_w, page_h, active_biome_keys, button_refs):
    planet_disp_w, planet_disp_h, planet_left, planet_top = compute_planet_layout(page_w, page_h)
    scale_x = planet_disp_w / PLANET_IMG_W
    scale_y = planet_disp_h / PLANET_IMG_H
    shapes  = []

    for bk in active_biome_keys:
        anchor_key = BIOME_KEY_MAP.get(bk)
        if anchor_key not in BIOME_ANCHORS:
            continue
        ax, ay = BIOME_ANCHORS[anchor_key]
        px = planet_left + ax * scale_x
        py = planet_top  + ay * scale_y

        corner = {"plaine": "bottom_left", "foret": "bottom_right",
                "montagne": "top_right",  "lac":   "top_left"}.get(bk, "bottom_left")

        if corner == "bottom_left":
            bx = BUTTON_MARGIN_X + 100;           by = page_h - BUTTON_MARGIN_Y - BTN_H / 2
        elif corner == "bottom_right":
            bx = page_w - BUTTON_MARGIN_X - 100;  by = page_h - BUTTON_MARGIN_Y - BTN_H / 2
        elif corner == "top_right":
            bx = page_w - BUTTON_MARGIN_X - 100;  by = BUTTON_MARGIN_Y + BTN_H / 2
        elif corner == "top_left":
            bx = BUTTON_MARGIN_X + 100;           by = BUTTON_MARGIN_Y + BTN_H / 2

        cx_ = (px + bx) / 2 + (page_w / 2 - (px + bx) / 2) * 0.65
        cy_ = (py + by) / 2 + (page_h / 2 - (py + by) / 2) * 0.01

        shapes.append(cv.Path(
            [cv.Path.MoveTo(px, py), cv.Path.QuadraticTo(cx_, cy_, bx, by)],
            paint=ft.Paint(stroke_width=3, color="#ffffff", style=ft.PaintingStyle.STROKE),
        ))
        shapes.append(cv.Circle(x=bx, y=by, radius=5, paint=ft.Paint(color="#ffffff", style=ft.PaintingStyle.FILL)))
        shapes.append(cv.Circle(x=px, y=py, radius=5, paint=ft.Paint(color="#ffffff", style=ft.PaintingStyle.FILL)))

    return cv.Canvas(shapes=shapes, width=page_w, height=page_h)


# ─────────────────────────────────────────────────────────────────────────────────────────
def _planet(page: ft.Page, navigate, on_close=None) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    keys_pressed    = {"right": False, "left": False, "space": False}
    dialogue_active = [False]
    running         = [True]
    focused         = [True]

    def start_keyboard_listener():
        def on_press(key):
            if not running[0]: return False
            try:
                k = key.char.lower()
                if k in ('d'): keys_pressed["right"]     = True
                if k in ('q', 'a'): keys_pressed["left"] = True
            except AttributeError:
                if key == pynput_keyboard.Key.right: keys_pressed["right"] = True
                if key == pynput_keyboard.Key.left:  keys_pressed["left"]  = True
                if key == pynput_keyboard.Key.space: keys_pressed["space"] = True

        def on_release(key):
            if not running[0]: return False
            try:
                k = key.char.lower()
                if k in ('d'): keys_pressed["right"]     = False
                if k in ('q', 'a'): keys_pressed["left"] = False
            except AttributeError:
                if key == pynput_keyboard.Key.right: keys_pressed["right"] = False
                if key == pynput_keyboard.Key.left:  keys_pressed["left"]  = False
                if key == pynput_keyboard.Key.space: keys_pressed["space"] = False

        with pynput_keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()


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
                        chara_msg.visible = False; npc_msg.visible = True
                    else:
                        chara_msg.content.value = scene[i_scene[0]]
                        chara_msg.visible = True;  npc_msg.visible = False
                    page.run_thread(page.update)
                else:
                    dialogue_box.visible = False
                    dialogue_active[0]   = False
                    page.run_thread(page.update)
                    def finish():
                        listener.stop()
                        if on_end:
                            page.run_thread(on_end)
                    threading.Thread(target=finish, daemon=True).start()

        msg = scene[i_scene[0]]
        chara_msg = ft.Container(
            content=ft.Text(msg, size=PLANET_DIALOGUE_TEXT_SIZE),
            bgcolor=ft.Colors.with_opacity(PLANET_DIALOGUE_BG_COLOR[0], PLANET_DIALOGUE_BG_COLOR[1]),
            alignment=ft.Alignment.CENTER_RIGHT, height=PLANET_DIALOGUE_HEIGHT, visible=False,
        )
        npc_msg = ft.Container(
            content=ft.Text(msg, size=PLANET_DIALOGUE_TEXT_SIZE),
            bgcolor=ft.Colors.with_opacity(PLANET_DIALOGUE_BG_COLOR[0], PLANET_DIALOGUE_BG_COLOR[1]),
            alignment=ft.Alignment.CENTER_LEFT, height=PLANET_DIALOGUE_HEIGHT, visible=True,
        )
        dialogue_box = ft.Container(
            content=ft.Stack([chara_msg, npc_msg]),
            alignment=ft.Alignment.BOTTOM_CENTER,
        )
        listener = pynput_keyboard.Listener(on_press=next_dialogue)
        listener.start()
        return dialogue_box

    # ── Sélection de leaf ─────────────────────────────────────────────────────────────────
    def open_leaf_selection_interface(page, current_leaf_ref, on_selected, exclude_current=True):
        def close(e=None):
            # Retire l'overlay de page.overlay plutôt que de le cacher — évite l'accumulation
            # d'overlays invisibles qui alourdit chaque page.update() avec le temps.
            if overlay in page.overlay:
                page.overlay.remove(overlay)
            page.update()

        def make_leaf_row(leaf):
            is_current  = exclude_current and current_leaf_ref[0] and leaf.id == current_leaf_ref[0].id
            is_disabled = leaf.hp <= 0 or leaf.nutrients <= 0 or leaf.hydration <= 0

            hp_ratio = leaf.hp / leaf.STAT_MAX["hp"] if leaf.STAT_MAX["hp"] > 0 else 0
            hp_bar   = ft.ProgressBar(
                value=hp_ratio,
                color=PLANET_LEAF_SELECT_HP_BAR_OK_COLOR if hp_ratio > 0.3 else PLANET_LEAF_SELECT_HP_BAR_LOW_COLOR,
                bgcolor=PLANET_LEAF_SELECT_HP_BAR_BG_COLOR, height=8, border_radius=4, expand=True,
            )

            def open_info(e, l=leaf):
                from leafsHome import open_leaf_modal
                open_leaf_modal(page, l)

            info_btn = ft.Container(
                content=ft.Text("I", size=10, weight=ft.FontWeight.BOLD, color=PLANET_LEAF_SELECT_INFO_BTN_COLOR),
                width=20, height=20, border_radius=10,
                bgcolor=PLANET_LEAF_SELECT_INFO_BTN_BG_COLOR,
                border=ft.border.all(1, PLANET_LEAF_SELECT_INFO_BTN_COLOR),
                alignment=ft.Alignment(0, 0), on_click=open_info, tooltip="Infos du leaf",
            )

            def on_leaf_click(e, l=leaf):
                if is_disabled or is_current:
                    return
                current_leaf_ref[0] = l
                on_selected(l)
                close()

            row = ft.Container(
                content=ft.Stack([
                    ft.Row([
                        ft.Container(
                            content=ft.Image(src=leaf.img, width=50, height=50, fit="contain"),
                            width=55, height=55,
                            bgcolor=ft.Colors.with_opacity(0.3, "black"),
                            border_radius=8, padding=3,
                        ),
                        ft.Column([
                            ft.Text(leaf.name, size=14, weight=ft.FontWeight.BOLD, color=PLANET_LEAF_SELECT_TITLE_COLOR),
                            ft.Text(f"ATK: {leaf.atk + leaf.atk_boost}  |  {LEAFS_TYPE[leaf.type]['name']}",
                                    size=11, color=PLANET_LEAF_SELECT_INFO_COLOR),
                            ft.Row([hp_bar,
                                    ft.Text(f"{leaf.hp}/{leaf.STAT_MAX['hp']}", size=10, color=PLANET_LEAF_SELECT_INFO_COLOR)],
                                    spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ], expand=True, spacing=4),
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Container(content=info_btn, right=4, top=4),
                ]),
                padding=10, border_radius=8,
                border=ft.border.all(2, PLANET_LEAF_SELECT_ROW_BORDER_ACTIVE_COLOR if is_current else PLANET_LEAF_SELECT_ROW_BORDER_COLOR),
                bgcolor=ft.Colors.with_opacity(0.5 if is_current else (0.2 if is_disabled else 0.15), "black"),
                opacity=0.4 if is_disabled else (0.7 if is_current else 1.0),
                on_click=on_leaf_click if not is_disabled and not is_current else None,
                tooltip="Déjà en combat" if is_current else ("Indisponible" if is_disabled else None),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            )

            def on_hover(e, r=row):
                if not is_disabled and not is_current:
                    r.bgcolor = ft.Colors.with_opacity(0.35 if e.data else 0.15, "black")
                    r.update()

            row.on_hover = on_hover
            return row

        leaf_list = ft.Column(
            controls=[make_leaf_row(l) for l in leafmanager.owned],
            scroll=ft.ScrollMode.AUTO, spacing=8, expand=True,
        )

        overlay = ft.Container(
            visible=True, expand=True,
            bgcolor=ft.Colors.with_opacity(PLANET_LEAF_SELECT_OVERLAY_BG_COLOR[0], PLANET_LEAF_SELECT_OVERLAY_BG_COLOR[1]),
            alignment=ft.Alignment(0, 0),
            content=ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.BASIC,
                on_tap=close,
                content=ft.Container(
                    expand=True, alignment=ft.Alignment(0, 0),
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Choisir un Leaf", size=18, weight=ft.FontWeight.BOLD, color=PLANET_LEAF_SELECT_TITLE_COLOR),
                                ft.TextButton("Fermer", on_click=close, style=ft.ButtonStyle(color=PLANET_LEAF_SELECT_TITLE_COLOR)),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(color=PLANET_LEAF_SELECT_PANEL_BORDER_COLOR),
                            leaf_list,
                        ], spacing=10, expand=True),
                        bgcolor=ft.Colors.with_opacity(PLANET_LEAF_SELECT_PANEL_BG_COLOR[0], PLANET_LEAF_SELECT_PANEL_BG_COLOR[1]),
                        border=ft.border.all(2, PLANET_LEAF_SELECT_PANEL_BORDER_COLOR),
                        border_radius=12, padding=16, width=420, height=500,
                        on_click=lambda e: None,
                    )
                )
            )
        )

        page.overlay.append(overlay)
        page.update()

    # ── Écran planète ─────────────────────────────────────────────────────────────────────
    def build_planet_screen():
        pw = page.width or 800
        ph = (page.height or 600) - getattr(page, "navbar_height", 60)

        planet_disp_w, planet_disp_h, planet_left, planet_top = compute_planet_layout(pw, ph)

        if   biomes_state["ll"]: planet_src = "assets/imgs/icons/biome_lake.png"
        elif biomes_state["mm"]: planet_src = "assets/imgs/icons/biome_mountain.png"
        elif biomes_state["ff"]: planet_src = "assets/imgs/icons/biome_forest.png"
        else:                    planet_src = "assets/imgs/icons/biome_plain.png"

        planet_img = ft.Container(
            content=ft.Image(src=planet_src, width=planet_disp_w, height=planet_disp_h, fit="fill"),
            left=planet_left, top=planet_top,
        )

        active_biome_keys = [bk for bk in ["plaine", "foret", "montagne", "lac"] if biomes_state[bk]]
        trail_canvas_obj  = build_trail_canvas(pw, ph, active_biome_keys, {})

        biome_musics = {
            "plaine":   "assets/musics/plain.wav",
            "foret":    "assets/musics/forest.wav",
            "montagne": "assets/musics/mountain.wav",
            "lac":      "assets/musics/lake.wav",
        }

        btn_containers = []
        for bk in ["plaine", "foret", "montagne", "lac"]:
            if not biomes_state[bk]:
                continue
            biome_str = {"plaine": "plain", "foret": "forest", "montagne": "mountain", "lac": "lake"}[bk]
            label     = {"plaine": "explore plaine", "foret": "explore foret",
                        "montagne": "explore montagne", "lac": "explore lac"}[bk]
            pos = compute_button_pos(bk, pw, ph)

            def make_handler(b, k):
                def handler(e):
                    if biome_musics[k]:
                        music.play(biome_musics[k], loop=True)
                    tp(e, b)
                return handler

            btn = ft.Container(
                content=ft.ElevatedButton(
                    ft.Text(label, size=20, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR),
                    on_click=make_handler(biome_str, bk),   
                    bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR,
                ),
                height=BTN_H, **pos,
            )
            btn_containers.append(btn)

        return ft.Stack([planet_img, trail_canvas_obj] + btn_containers, expand=True)

    # ─────────────────────────────────────────────────────────────────────────────────────
    def tp(e, biome):
        page.on_resize = None
        page.clean()
        running[0]            = True
        # ── Tirage pondéré de l'événement ─────────────────────────────────────────────
        event                 = choose_event()
        biome_icon            = next(b["icon"] for b in BIOMES if b["name"] == biome)
        keys_pressed["space"] = False
        dialogue_active[0]    = False

        scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h = \
            compute_layout(page.width, page.height, biome)
        layout = {"offset_x": offset_x, "offset_y": offset_y,
                "ground_bot": ground_bot, "img_disp_w": img_disp_w}

        bg_img = ft.Image(src=biome_icon, width=img_disp_w, height=img_disp_h, fit="fill")
        bg     = ft.Container(content=bg_img, left=offset_x, top=offset_y)

        sprite_ratio  = [0.5]
        sprite_page_x = [offset_x + img_disp_w * sprite_ratio[0]]

        new_sprite_img = ft.Image(src="assets/imgs/leafs/Froggy.png", width=SPRITE_W, height=180)
        new_sprite = ft.Container(
            content=new_sprite_img,
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )
        new_sprite.bottom = ground_bot
        new_sprite.left   = sprite_page_x[0]

        entity_id = None; entity_container = None
        entity_side_left = random.choice([True, False])
        ENEMY_W, ENEMY_H = 120, 140
        NPC_W,   NPC_H   = 100, 120
        EMPTY_W, EMPTY_H = 120, 100

        def _make_entity(src, w, h, visible=True):
            return ft.Container(content=ft.Image(src=src, width=w, height=h), visible=visible)

        if event == "enemy":
            entity_id = random.choice([b for b in ENEMIES[:10] if b["biome"] == [biome]]); entity_container = _make_entity(entity_id["visual"], ENEMY_W, ENEMY_H); entity_w = ENEMY_W
        elif event == "npc":
            entity_id = random.choice([b for b in NPCS[:7] if b["biome"] == biome]);   entity_container = _make_entity(entity_id["visual"], NPC_W, NPC_H);     entity_w = NPC_W
        elif event == "empty":
            entity_id = random.choice(OBJECTS); entity_container = _make_entity(entity_id["visual"], EMPTY_W, EMPTY_H); entity_w = EMPTY_W
        else:
            entity_id = LORE[scene_actu[0]]["visual"] if scene_actu[0] < len(LORE) else "assets/imgs/icons/leaf.png"
            entity_container = _make_entity(entity_id, NPC_W, NPC_H); entity_w = NPC_W

        entity_ratio  = (ENTITY_MARGIN / img_disp_w) if entity_side_left \
                        else (1.0 - (ENTITY_MARGIN + entity_w) / img_disp_w)
        entity_page_x = offset_x + img_disp_w * entity_ratio
        entity_container.bottom = ground_bot
        entity_container.left   = entity_page_x

        bouton_retour = ft.Container(content=ft.Row([ft.Container(
            content=ft.Text("planète", size=20, color=PLANET_BACK_BUTTON_TEXT_COLOR),
            bgcolor=PLANET_BACK_BUTTON_BG_COLOR, padding=10,
            border_radius=PLANET_BACK_BUTTON_BORDER_RADIUS, on_click=retourneur,
        )], alignment=ft.Alignment.TOP_LEFT))

        preset = [bg, entity_container, new_sprite, bouton_retour]

        def update_layout(w, h):
            s, ox, oy, g, dw, dh = compute_layout(w, h, biome)
            layout.update({"offset_x": ox, "offset_y": oy, "ground_bot": g, "img_disp_w": dw})
            bg_img.width = dw; bg_img.height = dh; bg.left = ox; bg.top = oy
            sprite_page_x[0] = ox + dw * sprite_ratio[0]
            new_sprite.bottom = g; new_sprite.left = sprite_page_x[0]
            entity_container.bottom = g; entity_container.left = ox + dw * entity_ratio

        page.on_resize = lambda ev: (update_layout(ev.width, ev.height), page.update())

        page.run_thread(start_keyboard_listener)

        def stop_tp_screen(ev=None):
            running[0] = False; page.on_resize = None

        page.stop_current_screen = stop_tp_screen
        page.window.on_event     = on_window_event

        first_sip = [True]

        async def tp_game_loop():
            while running[0]:
                moved = False
                if not dialogue_active[0]:
                    if keys_pressed["right"]: sprite_page_x[0] += SPRITE_SPEED; moved = True; new_sprite_img.src = "assets/imgs/leafs/Froggyd.png"
                    if keys_pressed["left"]:  sprite_page_x[0] -= SPRITE_SPEED; moved = True; new_sprite_img.src = "assets/imgs/leafs/Froggy.png"

                ox = layout["offset_x"]; dw = layout["img_disp_w"]; px = sprite_page_x[0]
                if dw > 0: sprite_ratio[0] = (px - ox) / dw

                if px <= ox:                    stop_tp_screen(); tp(e, biome); return
                if px + SPRITE_W >= ox + dw:    stop_tp_screen(); tp(e, biome); return
                if scene_actu[0] == 0:
                    stop_tp_screen(); declenche_scene(e, biome, scene_actu[0]); return
                if event == "lore" and scene_actu[0] >= len(LORE):
                    if "lore" in EVENTS: EVENTS.remove("lore")
                    stop_tp_screen(); tp(e, biome); return

                ent_px = ox + dw * entity_ratio
                near   = abs(px - ent_px) < 170

                if keys_pressed["space"]:
                    keys_pressed["space"] = False
                    if event == "npc" and entity_id["name"] != "rien"  and near:
                        stop_tp_screen(); shop(e, biome); return
                    if event == "enemy" and entity_id["name"] != "rien" and near:
                        running[0] = False; stop_tp_screen(); combat(e, biome, entity_id); return
                    if event == "empty" and near:
                        if first_sip[0]:
                            if entity_id["gives"] == "Eau minérale":
                                inventory_manager.append_item(ITEMS[1], 3)
                            elif entity_id["gives"] == "Herbe":
                                inventory_manager.append_item(ITEMS[4], 2)
                            first_sip[0] = False; entity_container.visible = False; page.update()
                    if event == "lore" and near:
                        stop_tp_screen()
                        declenche_scene(e, biome, scene_actu[0]); return

                if moved: new_sprite.left = sprite_page_x[0]; page.update()
                await asyncio.sleep(0.025)

        page.add(ft.Stack(preset, expand=True))
        page.update()
        page.run_task(tp_game_loop)

    # ─────────────────────────────────────────────────────────────────────────────────────
    def shop(e, biome):
        page.clean(); page.on_resize = None
        def on_back(ev): page.clean(); tp(ev, biome)
        shop_ui = _build_shop_home(page, "wandering", biome, on_back=on_back)
        page.add(ft.Container(content=ft.Column(controls=shop_ui, expand=True), expand=True, padding=0))

    # ── Combat ────────────────────────────────────────────────────────────────────────────
    def combat(e, biome, enemy):
        page.clean()
        music.play("assets/musics/combat.wav", loop=True)
        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)

        # ── État ──────────────────────────────────────────────────────────────────────
        current_leaf_ref = [leafmanager.owned[0] if leafmanager.owned else None]
        enemy_hp         = [enemy["hp"]]
        enemy_hp_max     = enemy["hp"]
        shield_hp        = [0]
        shield_max       = [0]
        player_turn      = [True]
        combat_over      = [False]

        # ── Layout ────────────────────────────────────────────────────────────────────
        scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h = compute_layout(page.width, page.height, biome)

        bg_img = ft.Image(src=biome_icon, width=img_disp_w, height=img_disp_h, fit="fill")
        bg     = ft.Container(content=bg_img, left=offset_x, top=offset_y)

        lx = offset_x + img_disp_w * 0.10
        ex = offset_x + img_disp_w * 0.90 - SPRITE_W

        leafsprite = ft.Container(
            content=ft.Image(src=current_leaf_ref[0].img if current_leaf_ref[0] else "assets/imgs/leafs/Froggyd.png",
                            width=SPRITE_W, height=180),
            bottom=ground_bot, left=lx,
            animate_position=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        )

        shield_visual = ft.Container(
            content=ft.Image(src="assets/imgs/icons/leaf_type_tank.png", width=50, height=50),
            bottom=ground_bot + 40, left=lx - 15,
            visible=False, opacity=0.85,
            animate_position=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        )

        enemysprite = ft.Container(
            content=ft.Image(src=enemy["visual"], width=SPRITE_W, height=180),
            bottom=ground_bot, left=ex,
        )

        # ── Barre de vie ennemi au-dessus du sprite ────────────────────────────────────
        enemy_hp_bar_ingame  = ft.ProgressBar(
            value=1.0,
            color=PLANET_COMBAT_ENEMY_HP_BAR_INGAME_COLOR,
            bgcolor=PLANET_COMBAT_ENEMY_HP_BAR_INGAME_BG_COLOR,
            height=8, border_radius=4, width=SPRITE_W,
        )
        enemy_hp_label_ingame = ft.Text(
            f"{enemy['name']}  {enemy_hp[0]}/{enemy_hp_max}",
            size=10, color=PLANET_COMBAT_ENEMY_HP_LABEL_COLOR,
            text_align=ft.TextAlign.CENTER,
        )
        enemy_hp_container_ingame = ft.Container(
            content=ft.Column(
                [enemy_hp_label_ingame, enemy_hp_bar_ingame],
                spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bottom=ground_bot + 195,   # juste au-dessus du sprite (hauteur 180 + marge)
            left=ex,
            width=SPRITE_W,
        )

        damage_text = ft.Container(
            content=ft.Text("", size=28, weight=ft.FontWeight.BOLD, color=PLANET_COMBAT_DAMAGE_TEXT_COLOR),
            visible=False, bottom=ground_bot + 200, left=ex,
        )

        heal_text = ft.Container(
            content=ft.Text("", size=28, weight=ft.FontWeight.BOLD, color=PLANET_COMBAT_HEAL_TEXT_COLOR),
            visible=False, bottom=ground_bot + 200, left=lx,
        )

        # ── Widgets du menu ────────────────────────────────────────────────────────────
        leaf_img_w    = ft.Image(src="", width=50, height=50, fit="contain")
        leaf_name_t   = ft.Text("", size=13, weight=ft.FontWeight.BOLD, color=PLANET_COMBAT_MENU_LEAF_NAME_COLOR)
        leaf_hp_bar   = ft.ProgressBar(value=1.0, color=PLANET_COMBAT_MENU_LEAF_HP_BAR_COLOR, bgcolor=PLANET_COMBAT_MENU_LEAF_HP_BAR_BG_COLOR, height=8, border_radius=4, width=110)
        leaf_hp_t     = ft.Text("", size=10, color=PLANET_COMBAT_MENU_LEAF_INFO_COLOR)
        leaf_atk_t    = ft.Text("", size=10, color=PLANET_COMBAT_MENU_LEAF_INFO_COLOR)
        leaf_type_t   = ft.Text("", size=10, color=PLANET_COMBAT_MENU_LEAF_INFO_COLOR)
        shield_hp_t   = ft.Text("", size=10, color=PLANET_COMBAT_MENU_SHIELD_TEXT_COLOR, visible=False)
        enemy_hp_bar  = ft.ProgressBar(value=1.0, color=PLANET_COMBAT_MENU_ENEMY_HP_BAR_COLOR, bgcolor=PLANET_COMBAT_MENU_ENEMY_HP_BAR_BG_COLOR, height=8, border_radius=4, width=110)
        enemy_hp_t    = ft.Text(f"{enemy_hp[0]}/{enemy_hp_max}", size=10, color=PLANET_COMBAT_MENU_LEAF_INFO_COLOR)
        action_status = ft.Text("À votre tour", size=13, color=PLANET_COMBAT_STATUS_PLAYER_COLOR, italic=True)

        def refresh_menu():
            leaf = current_leaf_ref[0]
            if leaf is None:
                return
            leaf_img_w.src       = leaf.img
            leaf_name_t.value    = leaf.name
            hp_r = leaf.hp / leaf.STAT_MAX["hp"] if leaf.STAT_MAX["hp"] > 0 else 0
            leaf_hp_bar.value    = hp_r
            leaf_hp_bar.color    = PLANET_COMBAT_MENU_LEAF_HP_BAR_COLOR if hp_r > 0.3 else PLANET_COMBAT_MENU_LEAF_HP_BAR_LOW_COLOR
            leaf_hp_t.value      = f"HP: {leaf.hp}/{leaf.STAT_MAX['hp']}"
            leaf_atk_t.value     = f"ATK: {leaf.atk + leaf.atk_boost}"
            leaf_type_t.value    = f"Type: {LEAFS_TYPE[leaf.type]['name']}"
            # Bouclier
            if shield_hp[0] > 0:
                shield_hp_t.visible = True
                shield_hp_t.value   = f"🛡 {shield_hp[0]}/{shield_max[0]}"
            else:
                shield_hp_t.visible = False
            # Ennemi — menu latéral
            e_r = max(0, enemy_hp[0]) / enemy_hp_max if enemy_hp_max > 0 else 0
            enemy_hp_bar.value = e_r
            enemy_hp_t.value   = f"{max(0, enemy_hp[0])}/{enemy_hp_max}"
            # Ennemi — barre en jeu
            enemy_hp_bar_ingame.value  = e_r
            enemy_hp_label_ingame.value = f"{enemy['name']}  {max(0, enemy_hp[0])}/{enemy_hp_max}"
            # Sprite leaf
            leafsprite.content = ft.Image(src=leaf.img, width=SPRITE_W, height=180)
            page.update()

        # ── Logique de combat ──────────────────────────────────────────────────────────
        async def animate_attack_player(dmg):
            """Leaf avance vers l'ennemi, dégâts, revient."""
            orig = leafsprite.left
            leafsprite.left   = ex - SPRITE_W + 10
            if shield_hp[0] > 0:
                shield_visual.left = ex - SPRITE_W + 10 - 15
            page.update()
            await asyncio.sleep(0.25)
            damage_text.content.value = f"-{dmg}"
            damage_text.left    = ex
            damage_text.visible = True
            page.update()
            await asyncio.sleep(0.5)
            leafsprite.left = orig
            if shield_hp[0] > 0:
                shield_visual.left = orig - 15
            damage_text.visible = False
            page.update()
            await asyncio.sleep(0.2)

        async def animate_attack_enemy(dmg):
            """Ennemi avance vers le leaf, dégâts, revient."""
            orig = enemysprite.left
            old_enemy_hp_x = enemy_hp_container_ingame.left
            enemysprite.left = lx + SPRITE_W - 10
            enemy_hp_container_ingame.left = lx + SPRITE_W - 10
            page.update()
            await asyncio.sleep(0.25)
            damage_text.content.value = f"-{dmg}"
            damage_text.left    = leafsprite.left
            damage_text.visible = True
            page.update()
            await asyncio.sleep(0.5)
            enemysprite.left = orig
            enemy_hp_container_ingame.left = old_enemy_hp_x
            damage_text.visible = False
            page.update()
            await asyncio.sleep(0.2)

        def leaf_is_viable(leaf):
            # Retourne True si le leaf peut encore combattre.
            return leaf is not None and leaf.hp > 0

        def apply_damage_to_player(dmg):
            remaining = dmg
            if shield_hp[0] > 0:
                absorbed = min(shield_hp[0], remaining)
                shield_hp[0] -= absorbed
                remaining    -= absorbed
                if shield_hp[0] <= 0:
                    shield_visual.visible = False
            if remaining > 0 and current_leaf_ref[0]:
                current_leaf_ref[0].stat_update("hp", -remaining)
            # Si le leaf actif vient de mourir, on passe automatiquement au suivant.
            # Le bouclier est réinitialisé car il était lié au leaf mort.
            # check_end() détectera ensuite s'il n'en reste plus aucun.
            if current_leaf_ref[0] and current_leaf_ref[0].hp <= 0:
                next_leaf = next((l for l in leafmanager.owned if leaf_is_viable(l)), None)
                current_leaf_ref[0]   = next_leaf
                shield_hp[0]          = 0
                shield_visual.visible = False

        def check_end():
            if enemy_hp[0] <= 0:
                return "win"
            if all(l.hp <= 0 for l in leafmanager.owned):
                return "lose"
            return None

        def set_buttons(enabled):
            btn_atk.disabled  = not enabled
            btn_comp.disabled = not enabled
            page.update()

        async def enemy_turn_async():
            action_status.value = "Tour de l'ennemi..."; action_status.color = PLANET_COMBAT_STATUS_ENEMY_COLOR
            set_buttons(False)
            await asyncio.sleep(0.4)
            dmg = enemy["atk"]
            await animate_attack_enemy(dmg)
            apply_damage_to_player(dmg)
            refresh_menu()
            result = check_end()
            if result == "lose":
                await end_combat(False); return
            # Si le leaf actif est mort mais qu'il en reste d'autres, forcer la
            # sélection d'un nouveau leaf avant que le joueur puisse agir.
            if not leaf_is_viable(current_leaf_ref[0]):
                action_status.value = "Votre leaf est KO ! Choisissez-en un autre."
                action_status.color = PLANET_COMBAT_STATUS_ENEMY_COLOR
                page.update()
                open_leaf_selection_interface(page, current_leaf_ref, lambda l: refresh_menu())
                # Les boutons restent désactivés jusqu'à ce qu'un leaf soit choisi.
                # refresh_menu() met à jour l'affichage mais n'active pas les boutons —
                # le joueur doit fermer la sélection pour continuer.
            player_turn[0] = True
            action_status.value = "À votre tour"; action_status.color = PLANET_COMBAT_STATUS_PLAYER_COLOR
            set_buttons(True)

        async def do_attack(e):
            if not player_turn[0] or combat_over[0]: return
            player_turn[0] = False; set_buttons(False)
            leaf = current_leaf_ref[0]
            # Sécurité : ne jamais attaquer avec un leaf mort ou absent
            if not leaf_is_viable(leaf): player_turn[0] = True; set_buttons(True); return
            dmg = leaf.atk + leaf.atk_boost
            await animate_attack_player(dmg)
            enemy_hp[0] -= dmg
            refresh_menu()
            result = check_end()
            if result == "win": await end_combat(True); return
            await enemy_turn_async()

        async def do_competence(e):
            if not player_turn[0] or combat_over[0]: return
            leaf = current_leaf_ref[0]
            # Sécurité : ne jamais utiliser une compétence avec un leaf mort ou absent
            if not leaf_is_viable(leaf): player_turn[0] = True; set_buttons(True); return
            leaf_type = leaf.type

            if leaf_type == 1:
                # Attacker : +50% ATK de base + 5% par niveau (fonctionnel dès niveau 0)
                player_turn[0] = False; set_buttons(False)
                bonus = int(leaf.atk * (0.50 + leaf.level * 0.05))
                dmg   = leaf.atk + leaf.atk_boost + bonus
                await animate_attack_player(dmg)
                enemy_hp[0] -= dmg
                refresh_menu()
                result = check_end()
                if result == "win": await end_combat(True); return
                await enemy_turn_async()

            elif leaf_type == 2:
                # Healer : soigne 10% des HP max cible + 5% par niveau (fonctionnel dès niveau 0)
                def on_heal_selected(target_leaf):
                    heal = max(3, int(target_leaf.STAT_MAX["hp"] * (0.10 + leaf.level * 0.05)))
                    target_leaf.stat_update("hp", heal)
                    heal_text.content.value = f"+{heal}"
                    heal_text.left    = leafsprite.left
                    heal_text.visible = True
                    page.update()
                    async def hide_and_continue():
                        await asyncio.sleep(0.8)
                        heal_text.visible = False
                        refresh_menu()
                        await enemy_turn_async()
                    player_turn[0] = False; set_buttons(False)
                    page.run_task(hide_and_continue)
                open_leaf_selection_interface(page, [None], on_heal_selected, exclude_current=False)

            elif leaf_type == 3:
                # Tank : bouclier 20% HP max + 10% par niveau (fonctionnel dès niveau 0)
                player_turn[0] = False; set_buttons(False)
                shield_max[0]  = max(5, int(leaf.hp_max * (0.20 + leaf.level * 0.10)))
                shield_hp[0]   = shield_max[0]
                shield_visual.visible = True
                shield_visual.left    = leafsprite.left - 15
                refresh_menu()
                action_status.value = f"Bouclier actif ! ({shield_hp[0]} HP)"; action_status.color = PLANET_COMBAT_STATUS_SHIELD_COLOR
                page.update()
                await asyncio.sleep(0.5)
                await enemy_turn_async()

        async def end_combat(victory):
            combat_over[0] = True
            keys_pressed["left"] = False
            keys_pressed["right"] = False
            set_buttons(False)
            if victory:
                reward = enemy.get("reward")
                if reward:
                    inventory_manager.append_money(reward.get("currency", "O2"), reward.get("amount", 0))
                    action_status.value = f"Victoire ! 🎉  +{reward['amount']} {reward['currency']}"
                else:
                    action_status.value = "Victoire ! 🎉"
                action_status.color = PLANET_COMBAT_STATUS_VICTORY_COLOR
                page.update()
                await asyncio.sleep(2)
                for l in leafmanager.owned:
                    l.reset_combat_boosts()
                music.stop()
                biome_musics = {
                    "plain":   "assets/musics/plain.wav",
                    "forest":    "assets/musics/forest.wav",
                    "montain": "assets/musics/mountain.wav",
                    "lake":      "assets/musics/lake.wav",
                }
                music.play(biome_musics[biome], loop=True)
                tp(None, biome)
            else:
                action_status.value = "Défaite..."; action_status.color = PLANET_COMBAT_STATUS_ENEMY_COLOR
                page.update()
                await asyncio.sleep(2)
                for l in leafmanager.owned:
                    l.reset_combat_boosts()
                music.stop()
                music.play("assets/musics/lobby.wav", loop=True)
                navigate("planet")

        # ── Boutons ────────────────────────────────────────────────────────────────────
        btn_atk = ft.ElevatedButton(
            "⚔️ Attaquer",
            on_click=lambda e: page.run_task(do_attack, e),
            bgcolor=PLANET_COMBAT_BTN_ATK_BG_COLOR, color=PLANET_COMBAT_BTN_TEXT_COLOR, width=130,
        )
        btn_comp = ft.ElevatedButton(
            "✨ Compétence",
            on_click=lambda e: page.run_task(do_competence, e),
            bgcolor=PLANET_COMBAT_BTN_COMP_BG_COLOR, color=PLANET_COMBAT_BTN_TEXT_COLOR, width=130,
        )
        btn_leaf = ft.ElevatedButton(
            "🌿 Changer",
            on_click=lambda e: open_leaf_selection_interface(page, current_leaf_ref, lambda l: refresh_menu()),
            bgcolor=PLANET_COMBAT_BTN_LEAF_BG_COLOR, color=PLANET_COMBAT_BTN_TEXT_COLOR, width=130,
        )

        # ── Menu 3 colonnes ────────────────────────────────────────────────────────────
        col_stats = ft.Container(
            ft.Column([
                ft.Container(content=leaf_img_w, width=55, height=55,
                            bgcolor=ft.Colors.with_opacity(PLANET_COMBAT_MENU_LEAF_IMG_BG_COLOR[0], PLANET_COMBAT_MENU_LEAF_IMG_BG_COLOR[1]),
                            border_radius=8, padding=3),
                leaf_name_t, leaf_hp_bar, leaf_hp_t, leaf_atk_t, leaf_type_t, shield_hp_t,
                ft.Divider(color=PLANET_COMBAT_MENU_DIVIDER_COLOR, height=8),
                ft.Text("Ennemi", size=10, color=PLANET_COMBAT_MENU_ENEMY_LABEL_COLOR),
                enemy_hp_bar, enemy_hp_t,
            ], spacing=3, expand=True),
            padding=10)

        col_actions = ft.Column([
            action_status, btn_atk, btn_comp,
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER, expand=True)

        col_leaf = ft.Column([
            btn_leaf,
        ], alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

        menu = ft.Container(
            content=ft.Row([
                ft.Container(content=col_stats,   expand=True, padding=ft.padding.symmetric(horizontal=8)),
                ft.VerticalDivider(color=PLANET_COMBAT_MENU_DIVIDER_COLOR),
                ft.Container(content=col_actions, expand=True, padding=ft.padding.symmetric(horizontal=8)),
                ft.VerticalDivider(color=PLANET_COMBAT_MENU_DIVIDER_COLOR),
                ft.Container(content=col_leaf,    expand=True, padding=ft.padding.symmetric(horizontal=8)),
            ], expand=True),
            bottom=0, left=0,
            width=page.width,
            height=page.height * PLANET_COMBAT_MENU_HEIGHT_RATIO,
            bgcolor=ft.Colors.with_opacity(PLANET_COMBAT_MENU_BG_COLOR[0], PLANET_COMBAT_MENU_BG_COLOR[1]),
        )

        preset = [bg, leafsprite, shield_visual, enemysprite,
                enemy_hp_container_ingame, damage_text, heal_text, menu]

        def on_resize_combat(ev):
            s, ox, oy, g, dw, dh = compute_layout(ev.width, ev.height, biome)
            bg_img.width = dw; bg_img.height = dh; bg.left = ox; bg.top = oy
            nlx = ox + dw * 0.10; nex = ox + dw * 0.90 - SPRITE_W
            leafsprite.bottom  = g; leafsprite.left  = nlx
            enemysprite.bottom = g; enemysprite.left = nex
            shield_visual.bottom = g + 40
            shield_visual.left   = nlx - 15 if not shield_visual.visible else shield_visual.left
            enemy_hp_container_ingame.bottom = g + 195
            enemy_hp_container_ingame.left   = nex
            menu.width = ev.width; menu.height = ev.height * PLANET_COMBAT_MENU_HEIGHT_RATIO
            page.update()

        page.on_resize = on_resize_combat
        page.add(ft.Stack(preset, expand=True))
        refresh_menu()

        # Sélection de leaf au démarrage du combat
        open_leaf_selection_interface(page, current_leaf_ref, lambda l: refresh_menu())

    # MARQUEUR FIN COMBAT — ne pas supprimer
    # ─────────────────────────────────────────────────────────────────────────────────────
    def declenche_scene(e, biome, n):
        if hasattr(page, "stop_current_screen"):
            page.stop_current_screen()
        if scene_actu[0] >= len(LORE):
            tp(e, biome); return
        dialogue_active[0] = True
        page.clean()
        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)
        locuteur   = LORE[n]["visual"]
        if LORE[n]["entity"] == "leaf":
            entity = next(b for b in LEAFS.values() if b["img"] == locuteur)
        elif LORE[n]["entity"] == "npc":
            entity = next(b for b in NPCS if b["visual"] == locuteur)
        else: #LORE[n]["entity"] == "nmi"
            entity = next(b for b in ENEMIES if b["visual"] == locuteur)
        scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h = compute_layout(page.width, page.height, biome)
        bg_img     = ft.Image(src=biome_icon, width=img_disp_w, height=img_disp_h, fit="fill")
        bg         = ft.Container(content=bg_img, left=offset_x, top=offset_y)
        sprite     = ft.Container(content=ft.Image(src="assets/imgs/leafs/Froggyd.png", width=SPRITE_W, height=180),
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
            boite = explique(entity)
            if boite is not None:
                page.overlay.append(boite)
                page.update()
                def toi(key):
                    if key == pynput_keyboard.Key.space:
                        listener.stop()
                        page.overlay.remove(boite)
                        page.update()
                        page.run_thread(suite)
                listener = pynput_keyboard.Listener(on_press=toi)
                listener.start()
            else:
                suite()

        def suite():
            scene_actu[0] += 1
            page.on_resize = None

            if scene_actu[0] == len(LORE): on_close()
            if scene_actu[0] == 4:
                biomes_state["pp"] = False; biomes_state["foret"] = True; biomes_state["ff"] = True
            if scene_actu[0] == 9:
                biomes_state["ff"] = False; biomes_state["montagne"] = True; biomes_state["mm"] = True
            if scene_actu[0] == 14:
                biomes_state["mm"] = False; biomes_state["lac"] = True; biomes_state["ll"] = True


            if not LORE[n]["combat"]:
                if LORE[n]["add"] is not None:
                    leafmanager.add_leaf(LEAFS[LORE[n]["add"]])
                if scene_actu[0] in (5, 10, 15):
                    music.play("assets/musics/lobby.wav", loop=True)
                    page.overlay.clear()
                    navigate("planet")
                    return
                else:
                    running[0] = False
                    page.overlay.clear()
                    page.update()
                    tp(e, biome)
                    return
            else:
                enemy = next(b for b in ENEMIES if b["visual"] == locuteur)
                page.overlay.clear()
                page.update()
                combat(e, biome, enemy)
                on_planet_resize()
                return
            

        paroles = dialogue(e, LORE[n]["dialogue"], dialogue_active, on_end=on_end)
        preset  = [bg, npc_sprite, sprite, paroles]
        page.add(ft.Stack(preset, expand=True))

    def explique(entity):
        if entity["met"] == False:
            boite = ft.Container(
                content=ft.Text(entity["prez"], size=50, color="white"),
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
            return

    # ─────────────────────────────────────────────────────────────────────────────────────
    def retourneur(e):
        music.play("assets/musics/lobby.wav", loop=True)
        page.on_resize = None; page.clean(); navigate("planet")

    initial_stack = build_planet_screen()

    def on_planet_resize(ev=None):
        new_stack = build_planet_screen()
        if hasattr(page, "body_container"):
            page.body_container.content = ft.Column(controls=[new_stack], expand=True)
            page.update()
        else:
            page.controls.clear(); page.add(new_stack); page.update()

    page.on_resize = on_planet_resize
    return initial_stack
