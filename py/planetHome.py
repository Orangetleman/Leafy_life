import flet as ft
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

scene_actu = [0]

# ── Config biomes : (img_w_original, img_h_original, ground_ratio_depuis_le_bas) ─────────
BIOME_LAYOUT = {
    "plain":    (10000, 5192, 601  / 2596),
    "forest":   (1888,  999,  100  / 333 ),
    "lake":     (1888,  999,  41   / 111 ),
    "mountain": (1888,  999,  31   / 111 ),
}

SPRITE_SPEED  = 30    # px-page par frame, constant quelle que soit la résolution
SPRITE_W      = 150  # largeur du sprite joueur en px-page
ENTITY_MARGIN = 80   # marge depuis le bord de l'image affichée, en px-page


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


def _planet(page: ft.Page, navigate) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    plaine   = [ft.Container(content=ft.Row([ft.ElevatedButton(ft.Text("explore plaine",   size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR),   on_click=lambda e, b="plain":    tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)]), bottom=30, left=30,visible= True)]
    foret    = [ft.Container(content=ft.Row([ft.ElevatedButton(ft.Text("explore foret",    size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR),    on_click=lambda e, b="forest":   tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)]), bottom=30, right=30, visible=False)]
    montagne = [ft.Container(content=ft.Row([ft.ElevatedButton(ft.Text("explore montagne", size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR), on_click=lambda e, b="mountain": tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)]), top=30, right=30, visible=False)]
    lac      = [ft.Container(content=ft.Row([ft.ElevatedButton(ft.Text("explore lac",      size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR),      on_click=lambda e, b="lake":     tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)]), top=30, left=30, visible=False)]
    pp =    [ft.Container(ft.Image(src="assets/imgs/icons/biome_plain.png"), alignment=ft.Alignment.CENTER, expand=True, visible= True)]
    ff =    [ft.Container(ft.Image(src="assets/imgs/icons/biome_forest.png"), alignment=ft.Alignment.CENTER, expand=True, visible=False)]
    mm =    [ft.Container(ft.Image(src="assets/imgs/icons/biome_mountain.png"), alignment=ft.Alignment.CENTER, expand=True,visible=False)]
    ll =    [ft.Container(ft.Image(src="assets/imgs/icons/biome_lake.png"), alignment=ft.Alignment.CENTER, expand=True,visible=False)]
    f1 =    [ft.Container(ft.Image(src="assets/imgs/icons/fil.png"), alignment=ft.Alignment.BOTTOM_LEFT, expand=True,visible=True)]
    f2 =    [ft.Container(ft.Image(src="assets/imgs/icons/fil2.png"), alignment=ft.Alignment.BOTTOM_LEFT, expand=True,visible=False)]
    f3 =    [ft.Container(ft.Image(src="assets/imgs/icons/fil3.png"), alignment=ft.Alignment.BOTTOM_LEFT, expand=True,visible=False)]
    f4 =    [ft.Container(ft.Image(src="assets/imgs/icons/fil4.png"), alignment=ft.Alignment.BOTTOM_LEFT, expand=True,visible=False)]

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

    # ─────────────────────────────────────────────────────────────────────────────────────

    def tp(e, biome):
        page.clean()
        running[0]            = True
        event                 = random.choice(EVENTS)
        biome_icon            = next(b["icon"] for b in BIOMES if b["name"] == biome)
        keys_pressed["space"] = False
        dialogue_active[0]    = False

        # ── Layout initial ────────────────────────────────────────────────────────────
        scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h = \
            compute_layout(page.width, page.height, biome)

        # layout stocke uniquement ce dont la boucle a besoin en temps réel
        layout = {
            "offset_x":    offset_x,
            "offset_y":    offset_y,
            "ground_bot":  ground_bot,
            "img_disp_w":  img_disp_w,
        }

        # ── Fond ──────────────────────────────────────────────────────────────────────
        bg_img = ft.Image(src=biome_icon, width=img_disp_w, height=img_disp_h, fit="fill")
        bg     = ft.Container(content=bg_img, left=offset_x, top=offset_y)

        # ── Sprite joueur ─────────────────────────────────────────────────────────────
        # Position en px-page, initialisée au centre de l'image affichée.
        # sprite_ratio : position relative dans l'image (0=bord gauche, 1=bord droit)
        # conservée au resize pour replacer le sprite sans le "téléporter" (il n'est pas vraiment tp mais c'était l'image qui glisait derrière lui).
        sprite_ratio  = [0.5]
        sprite_page_x = [offset_x + img_disp_w * sprite_ratio[0]]

        new_sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=SPRITE_W, height=180),
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )
        new_sprite.bottom = ground_bot
        new_sprite.left   = sprite_page_x[0]

        # ── Entité ────────────────────────────────────────────────────────────────────
        # Position en px-page, exprimée comme ratio sur l'image affichée :
        # côté gauche -> ratio_entity ≈ ENTITY_MARGIN / img_disp_w
        # côté droit  -> ratio_entity ≈ 1 - (ENTITY_MARGIN + largeur_entité) / img_disp_w
        entity_id        = None
        entity_container = None
        entity_side_left = random.choice([True, False])

        # Toutes les tailles en proportion de la hauteur du sprite joueur (180px)
        # pour garder une cohérence visuelle quelle que soit la résolution de l'image.
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
        else:  # lore
            if not scene_actu[0] >= len(LORE):
                entity_id        = LORE[scene_actu[0]]["visual"]
            else:
                entity_id        = "assets/imgs/icons/leaf.png"
            entity_container = _make_entity(entity_id, NPC_W, NPC_H)
            entity_w         = NPC_W

        # entity_ratio : position du COIN GAUCHE de l'entité dans l'image affichée
        # calculé APRÈS avoir fixé entity_w pour être cohérent
        if entity_side_left:
            entity_ratio = ENTITY_MARGIN / img_disp_w
        else:
            entity_ratio = 1.0 - (ENTITY_MARGIN + entity_w) / img_disp_w

        entity_page_x = offset_x + img_disp_w * entity_ratio
        entity_container.bottom = ground_bot
        entity_container.left   = entity_page_x

        # ── Bouton retour ─────────────────────────────────────────────────────────────
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

        # ── Resize ────────────────────────────────────────────────────────────────────
        def update_layout(w, h):
            s, ox, oy, g, dw, dh = compute_layout(w, h, biome)
            layout.update({"offset_x": ox, "offset_y": oy, "ground_bot": g, "img_disp_w": dw})

            # Fond
            bg_img.width  = dw
            bg_img.height = dh
            bg.left = ox
            bg.top  = oy

            # Sprite : conserver sa position relative sur l'image
            sprite_page_x[0] = ox + dw * sprite_ratio[0]
            new_sprite.bottom = g
            new_sprite.left   = sprite_page_x[0]

            # Entité : conserver sa position relative sur l'image
            entity_container.bottom = g
            entity_container.left   = ox + dw * entity_ratio

        def on_resize(ev):
            update_layout(ev.width, ev.height)
            page.update()

        page.on_resize = on_resize

        # ── Listener clavier ──────────────────────────────────────────────────────────
        new_listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
        new_listener.start()

        def stop_tp_screen(ev=None):
            running[0]     = False
            page.on_resize = None
            new_listener.stop()

        page.stop_current_screen = stop_tp_screen
        page.window.on_event     = on_window_event

        first_sip = [True]

        # ── Boucle de jeu ─────────────────────────────────────────────────────────────
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

                ox   = layout["offset_x"]
                dw   = layout["img_disp_w"]
                px   = sprite_page_x[0]

                # Bords de l'image affichée en px-page
                img_left  = ox
                img_right = ox + dw

                # Mise à jour du ratio (pour le resize)
                if dw > 0:
                    sprite_ratio[0] = (px - ox) / dw

                # Sorties latérales
                if px <= img_left:
                    stop_tp_screen()
                    tp(e, biome)
                    return
                if px + SPRITE_W >= img_right:
                    stop_tp_screen()
                    tp(e, biome)
                    return
                if scene_actu[0]==0:
                    stop_tp_screen()
                    declenche_scene(e, biome, scene_actu[0])
                    return
                if event == "lore" and scene_actu[0] >= len(LORE):
                    if len(EVENTS) <= 4:
                        EVENTS.pop(3)
                    stop_tp_screen()
                    tp(e,biome)


                # Proximité entité
                ent_px = ox + dw * entity_ratio
                near   = abs(px - ent_px) < 170

                # Interactions
                if event == "npc" and near and keys_pressed["space"]:
                    stop_tp_screen()
                    keys_pressed["space"] = False
                    shop(e, biome)
                if event == "enemy" and near and keys_pressed["space"]:
                    stop_tp_screen()
                    keys_pressed["space"] = False
                    combat(e, biome, entity_id)
                    return

                if event == "empty" and near and keys_pressed["space"]:
                    if first_sip[0] and entity_id["gives"] == "Eau minérale":
                        inventory_manager.append_item(ITEMS[1], 3)
                        first_sip[0]             = False
                        entity_container.visible = False
                        page.update()
                    keys_pressed["space"] = False

                if event == "lore" and near and keys_pressed["space"]:
                    keys_pressed["space"] = False
                    stop_tp_screen()
                    declenche_scene(e, biome, scene_actu[0])
                    return

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

        def on_back(e):
            page.clean()
            tp(e, biome)

        shop_ui = _build_shop_home(page, "wandering", biome, on_back=on_back)

        page.add(
            ft.Container(
                content=ft.Column(controls=shop_ui, expand=True),
                expand=True,
                padding=0,
            )
        )
    
    def combat(e, biome, enemy):
        page.clean()
        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)

        scale, offset_x, offset_y, ground_bot, img_disp_w, img_disp_h = compute_layout(page.width, page.height, biome)

        bg_img = ft.Image(src=biome_icon, width=img_disp_w, height=img_disp_h, fit="fill")
        bg     = ft.Container(content=bg_img, left=offset_x, top=offset_y)

        # Froggy à 10% depuis la gauche, ennemi à 10% depuis la droite de l'image
        leaf_page_x  = offset_x + img_disp_w * 0.10
        enemy_page_x = offset_x + img_disp_w * 0.90 - SPRITE_W

        """selected_leaf = open_leaf_selection_interface()""" # À FAIRE CHRIS

        leafsprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=SPRITE_W, height=180),
            bottom=ground_bot, left=leaf_page_x,
        )
        enemysprite = ft.Container(
            content=ft.Image(src=enemy["visual"], width=SPRITE_W, height=180),
            bottom=ground_bot, left=enemy_page_x,
        )
        menu = ft.Container(
            # content = creer_combat_menu()
            bottom=0, left=0,
            width=page.width,
            height=page.height * PLANET_COMBAT_MENU_HEIGHT_RATIO,
            bgcolor=ft.Colors.with_opacity(PLANET_COMBAT_MENU_BG_COLOR[0], PLANET_COMBAT_MENU_BG_COLOR[1]),
        )
        """CHRIS A AJOUTER BOUTONS (atk, competence, boite_leaf) + BARRE PV ET INFOS LEAF"""

        preset = [bg, leafsprite, enemysprite, menu]

        def on_resize_combat(ev):
            s, ox, oy, g, dw, dh = compute_layout(ev.width, ev.height, biome)
            bg_img.width  = dw
            bg_img.height = dh
            bg.left = ox
            bg.top  = oy
            leafsprite.bottom  = g
            leafsprite.left    = ox + dw * 0.10
            enemysprite.bottom = g
            enemysprite.left   = ox + dw * 0.90 - SPRITE_W
            page.update()

        page.on_resize = on_resize_combat
        page.add(ft.Stack(preset, expand=True))

    # ─────────────────────────────────────────────────────────────────────────────────────

    def atk(leaf, enemy):
        malus = f"-{leaf.atk}"
        dgts  = ft.Container(ft.Text(malus, size=20), visible=True)
        leaf.left = page.width - 20
        page.update()
        page.add(dgts)
        dgts.visible = False
        leaf.left    = 20
        page.update()
        enemy["hp"] -= leaf.atk

    def competence(leaf, enemy):
        if leaf.type == 1:
            leaf.atk_boost = leaf.atk
            atk(leaf, enemy)
            leaf.atk_boost = 0
        elif leaf.type == 3:
            bouclier = ft.Container(
                ft.Image(src="assets/imgs/icons/leaf_type_tank.png", width=100, height=100),
                visible=True,
            )
            page.add(bouclier)
            enemy["atk"] = max(1, enemy["atk"] // 2)
            return 2
        return None

    def open_leaf_selection_interface():
        pass
    """CHRISSS FAIS ICI""" # J'ai comprsi tkt -_-

    # ─────────────────────────────────────────────────────────────────────────────────────

    def declenche_scene(e, biome, n):
        if hasattr(page, "stop_current_screen"):
            page.stop_current_screen()
        if scene_actu[0]>=len(LORE):
            tp(e,biome)
        else:
            dialogue_active[0] = True
            page.clean()

            biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)
            locuteur   = LORE[n]["visual"]

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
                scene_actu[0] += 1
                if scene_actu == 2:
                    pp[0].visible = False
                    f1[0].visible = False
                    foret[0].visible = True
                    ff[0].visible = True
                    f2[0].visible = True
                    navigate("planet")
                if not LORE[n]["combat"]:
                    if LORE[n]["add"] != None:
                        leafmanager.add_leaf(LEAFS[LORE[n]["add"]])
                    tp(e, biome)
                else:
                    enemy = next(b for b in ENEMIES if b["visual"] == locuteur)
                    combat(e, biome, enemy)

            paroles = dialogue(e, LORE[n]["dialogue"], dialogue_active, on_end=on_end)
            preset  = [bg, npc_sprite, sprite, paroles]
            page.add(ft.Stack(preset, expand=True))

    # ─────────────────────────────────────────────────────────────────────────────────────

    planet = ft.Stack([
        pp[0],
        ff[0],
        mm[0],
        ll[0],
        f1[0],
        f2[0],
        f3[0],
        f4[0],
        plaine[0],
        foret[0],
        montagne[0],
        lac[0]
    ], expand=True)

    def retourneur(e):
        page.on_resize = None
        page.clean()
        navigate("planet")

    return planet