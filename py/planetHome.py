import flet as ft
from pynput import keyboard as pynput_keyboard
from datacenter import *
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
# ground_ratio : fraction de la hauteur de l'image (depuis le bas) où se trouve le sol.
BIOME_LAYOUT = {
    "plain":    (10000, 5192, 601  / 2596),
    "forest":   (1888,  999,  100  / 333 ),
    "lake":     (1888,  999,  41   / 111 ),
    "mountain": (1888,  999,  31   / 111 ),
}

# Vitesse de référence en pixels de l'image ORIGINALE par frame.
# Elle sera multipliée par scale pour donner la vitesse en pixels-écran.
BASE_SPEED = 15

# Marge horizontale fixe (px depuis le bord de la page) pour les entités.
ENTITY_MARGIN = 80


def compute_layout(page_w, page_h, biome_name):
    """
    Calcule les paramètres de disposition pour un biome donné, en tenant
    compte du comportement fit='cover' de l'image de fond.

    Avec cover : scale = max(page_w / img_w, page_h / img_h)
    L'image est centrée → elle peut déborder horizontalement (offset_x)
    et/ou verticalement (offset_y) de façon symétrique.

    Paramètres
    ----------
    page_w, page_h  : dimensions actuelles de la fenêtre (pixels écran)
    biome_name      : clé dans BIOME_LAYOUT

    Retour
    ------
    ground_bot : pixels depuis le bas de la PAGE jusqu'au sol de l'image.
                Utiliser comme `.bottom` pour poser un sprite sur le sol.
    scale      : facteur d'agrandissement (cover). Permet de convertir une
                coordonnée en pixels-image-originale → pixels-écran :
                     px_ecran = px_image * scale
    offset_x   : débordement horizontal de l'image de chaque côté de la page.
                Permet de convertir une position image → position page :
                     page_x = img_x * scale - offset_x
                Et l'inverse :
                    img_x  = (page_x + offset_x) / scale
    speed      : vitesse du sprite en pixels-écran par frame.
                 = BASE_SPEED * scale  (constante en espace-image).
    """
    img_w, img_h, ground_ratio = BIOME_LAYOUT.get(biome_name, (1250, 649, 601 / 2596))

    scale    = max(page_w / img_w, page_h / img_h)
    disp_w   = img_w * scale          # largeur de l'image affichée (≥ page_w)
    disp_h   = img_h * scale          # hauteur de l'image affichée (≥ page_h)

    offset_x = max(0.0, (disp_w - page_w) / 2.0)   # débordement horizontal
    offset_y = max(0.0, (disp_h - page_h) / 2.0)   # débordement vertical

    # Hauteur du sol depuis le bas de l'image affichée, ramenée à la page
    ground_bot = max(0.0, disp_h * ground_ratio - offset_y)
    speed      = BASE_SPEED * scale

    return ground_bot, scale, offset_x, speed


# ─────────────────────────────────────────────────────────────────────────────────────────

def _planet(page: ft.Page, navigate) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    plaine   = ft.Text("explore plaine",   size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR)
    foret    = ft.Text("explore foret",    size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR)
    montagne = ft.Text("explore montagne", size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR)
    lac      = ft.Text("explore lac",      size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR)

    keys_pressed    = {"right": False, "left": False, "space": False}
    dialogue_active = [False]
    running         = [True]
    focused         = [True]

    # ── Callbacks clavier ─────────────────────────────────────────────────────────────────

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

    # ── Système de dialogue ───────────────────────────────────────────────────────────────

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
    # ── Exploration d'un biome ────────────────────────────────────────────────────────────
    # ─────────────────────────────────────────────────────────────────────────────────────

    def tp(e, biome):
        page.clean()
        running[0]            = True
        event                 = random.choice(EVENTS)
        biome_icon            = next(b["icon"] for b in BIOMES if b["name"] == biome)
        keys_pressed["space"] = False
        dialogue_active[0]    = False

        # ── Layout dynamique ──────────────────────────────────────────────────────────
        # layout stocke les valeurs courantes recalculées à chaque resize.
        layout = {"bottom": 0.0, "scale": 1.0, "offset_x": 0.0, "speed": float(BASE_SPEED)}

        # sprite_img_x : position du sprite en pixels de l'IMAGE ORIGINALE (non scalée).
        # Conversion vers la page : page_x = sprite_img_x[0] * scale - offset_x
        # Conversion depuis la page : sprite_img_x[0] = (page_x + offset_x) / scale
        sprite_img_x = [0.0]

        # ── Fond ──────────────────────────────────────────────────────────────────────
        bg = ft.Container(
            content=ft.Image(src=biome_icon, fit="cover"),
            expand=True,
        )

        # ── Bouton retour ─────────────────────────────────────────────────────────────
        bouton_retour = ft.Container(
            content=ft.Row(
                [ft.Container(
                    content=ft.Text("planète", size=20, color=PLANET_BACK_BUTTON_TEXT_COLOR),
                    bgcolor=PLANET_BACK_BUTTON_BG_COLOR,
                    padding=10,
                    border_radius=PLANET_BACK_BUTTON_BORDER_RADIUS,
                    on_click=retourneur,
                )],
                alignment=ft.Alignment.TOP_LEFT,
            ),
        )

        # ── Sprite joueur ─────────────────────────────────────────────────────────────
        new_sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )

        # ── Entité : positionnée en absolu dans le Stack ──────────────────────────────
        # entity_side_left=True  → entité à gauche  (attribut .left=ENTITY_MARGIN)
        # entity_side_left=False → entité à droite  (attribut .right=ENTITY_MARGIN)
        # .bottom sera mis à jour par update_layout() à chaque resize.
        # .left / .right sont des marges fixes depuis le bord de la PAGE : Flet les
        # recalcule automatiquement lors d'un resize, pas besoin de les retoucher.
        entity_id        = None
        entity_container = None
        entity_side_left = random.choice([True, False])

        if event == "enemy":
            entity_id = random.choice(ENEMIES)
            if entity_side_left:
                entity_container = ft.Container(
                    content=ft.Image(src=entity_id["visual"], width=80, height=60),
                    left=ENTITY_MARGIN,
                )
            else:
                entity_container = ft.Container(
                    content=ft.Image(src=entity_id["visual"], width=80, height=60),
                    right=ENTITY_MARGIN,
                )

        elif event == "npc":
            entity_id = random.choice(NPCS)
            if entity_side_left:
                entity_container = ft.Container(
                    content=ft.Image(src=entity_id["visual"], width=80, height=60),
                    left=ENTITY_MARGIN,
                )
            else:
                entity_container = ft.Container(
                    content=ft.Image(src=entity_id["visual"], width=80, height=60),
                    right=ENTITY_MARGIN,
                )

        elif event == "empty":
            entity_id = random.choice(OBJECTS)
            if entity_side_left:
                entity_container = ft.Container(
                    content=ft.Image(src=entity_id["visual"], width=180, height=160),
                    left=ENTITY_MARGIN,
                    visible=True,
                )
            else:
                entity_container = ft.Container(
                    content=ft.Image(src=entity_id["visual"], width=180, height=160),
                    right=ENTITY_MARGIN,
                    visible=True,
                )

        else:  # lore
            entity_id = LORE[scene_actu[0]]["visual"]
            if entity_side_left:
                entity_container = ft.Container(
                    content=ft.Image(src=entity_id, width=80, height=60),
                    left=ENTITY_MARGIN,
                )
            else:
                entity_container = ft.Container(
                    content=ft.Image(src=entity_id, width=80, height=60),
                    right=ENTITY_MARGIN,
                )

        # ── Premier calcul du layout ──────────────────────────────────────────────────
        g_bot, scale, offset_x, spd = compute_layout(page.width, page.height, biome)
        layout.update({"bottom": g_bot, "scale": scale, "offset_x": offset_x, "speed": spd})

        # Sprite au centre de la page, converti en coordonnée image-originale
        start_page_x    = page.width / 2.0
        sprite_img_x[0] = (start_page_x + offset_x) / scale

        new_sprite.bottom = g_bot
        new_sprite.left   = start_page_x          # = sprite_img_x[0] * scale - offset_x

        entity_container.bottom = g_bot

        # ── Preset ────────────────────────────────────────────────────────────────────
        preset = [bg, entity_container, new_sprite, bouton_retour]

        # ── Recalcul au resize ────────────────────────────────────────────────────────
        def update_layout():
            """
            Appelée à chaque redimensionnement.
            - Recompute scale, offset_x, ground_bot, speed.
            - Replace le sprite à la même position SUR L'IMAGE (sprite_img_x conservé).
            - Replace l'entité au bon niveau de sol (.bottom).
            - .left / .right de l'entité ne sont PAS modifiés : Flet les gère nativement.
            """
            g_bot, scale, offset_x, spd = compute_layout(page.width, page.height, biome)
            layout.update({"bottom": g_bot, "scale": scale, "offset_x": offset_x, "speed": spd})

            # Position page du sprite conservant sa position image
            new_sprite.bottom = g_bot
            new_sprite.left   = sprite_img_x[0] * scale - offset_x

            if entity_container is not None:
                entity_container.bottom = g_bot

        def on_resize(ev):
            update_layout()
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
                        # Déplacement en espace-image : constant quel que soit le zoom
                        sprite_img_x[0] += BASE_SPEED
                        moved = True
                    if keys_pressed["left"]:
                        sprite_img_x[0] -= BASE_SPEED
                        moved = True

                # Conversion image → page pour la frame courante
                page_x = sprite_img_x[0] * layout["scale"] - layout["offset_x"]

                # ── Détection de proximité avec l'entité ──────────────────────────────
                # L'entité est à ENTITY_MARGIN depuis le bord gauche ou droit de la page.
                if entity_side_left:
                    near = page_x < 250
                else:
                    near = page_x > page.width - 300

                # ── Sorties latérales → nouvelle zone ─────────────────────────────────
                if page_x < -50:
                    stop_tp_screen()
                    tp(e, biome)
                    return
                if page_x > page.width + 50:
                    stop_tp_screen()
                    tp(e, biome)
                    return

                # ── Interactions ──────────────────────────────────────────────────────
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

                # ── Rendu ─────────────────────────────────────────────────────────────
                if moved:
                    new_sprite.left = page_x
                    page.update()

                await asyncio.sleep(0.025)

        page.add(ft.Stack(preset, expand=True))
        page.run_task(tp_game_loop)

    # ─────────────────────────────────────────────────────────────────────────────────────
    # ── Combat ───────────────────────────────────────────────────────────────────────────
    # ─────────────────────────────────────────────────────────────────────────────────────

    def combat(e, biome, enemy):
        page.clean()
        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)

        # En combat, seul ground_bot est utile (les sprites sont aux bords de la page).
        # Les positions .left=20 et .right=20 sont relatives aux bords → auto-resize.
        g_bot, _, _, _ = compute_layout(page.width, page.height, biome)

        bg = ft.Container(
            content=ft.Image(src=biome_icon, fit="cover"),
            expand=True,
        )

        leafsprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            bottom=g_bot, left=20,
        )
        enemysprite = ft.Container(
            content=ft.Image(src=enemy["visual"], width=150, height=180),
            bottom=g_bot, right=20,
        )
        menu = ft.Container(
            bottom=0, left=0,
            width=page.width,
            height=page.height * PLANET_COMBAT_MENU_HEIGHT_RATIO,
            bgcolor=ft.Colors.with_opacity(
                PLANET_COMBAT_MENU_BG_COLOR[0],
                PLANET_COMBAT_MENU_BG_COLOR[1],
            ),
        )
        """CHRIS A AJOUTER BOUTONS (atk, competence, boite_leaf) + BARRE PV ET INFOS LEAF"""

        preset = [bg, leafsprite, enemysprite, menu]

        def on_resize_combat(ev):
            g, _, _, _ = compute_layout(page.width, page.height, biome)
            leafsprite.bottom  = g
            enemysprite.bottom = g
            page.update()

        page.on_resize = on_resize_combat
        page.add(ft.Stack(preset, expand=True))

    # ─────────────────────────────────────────────────────────────────────────────────────
    # ── Actions de combat (stubs) ─────────────────────────────────────────────────────────
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
        if leaf.type == 1:    # attacker
            leaf.atk_boost = leaf.atk
            atk(leaf, enemy)
            leaf.atk_boost = 0
        elif leaf.type == 3:  # tank
            bouclier = ft.Container(
                ft.Image(src="assets/imgs/icons/leaf_type_tank.png", width=100, height=100),
                visible=True,
            )
            page.add(bouclier)
            enemy["atk"] = max(1, enemy["atk"] // 2)
            return 2
        return None

    def boite_leaf():
        pass
    """CHRISSS FAIS ICI"""

    # ─────────────────────────────────────────────────────────────────────────────────────
    # ── Scène de lore ─────────────────────────────────────────────────────────────────────
    # ─────────────────────────────────────────────────────────────────────────────────────

    def declenche_scene(e, biome, n):
        if hasattr(page, "stop_current_screen"):
            page.stop_current_screen()
        dialogue_active[0] = True
        page.clean()

        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)
        locuteur   = LORE[n]["visual"]

        g_bot, _, _, _ = compute_layout(page.width, page.height, biome)

        bg = ft.Container(
            content=ft.Image(src=biome_icon, fit="cover"),
            expand=True,
        )

        # Sprites aux bords de la page : .left/right auto-resize, seul .bottom doit suivre.
        sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            bottom=g_bot, left=20,
        )
        npc_sprite = ft.Container(
            content=ft.Image(src=locuteur, width=150, height=180),
            bottom=g_bot, right=20,
        )

        def on_resize_scene(ev):
            g, _, _, _ = compute_layout(page.width, page.height, biome)
            sprite.bottom     = g
            npc_sprite.bottom = g
            page.update()

        page.on_resize = on_resize_scene

        def on_end():
            page.on_resize = None
            scene_actu[0] += 1
            if not LORE[n]["combat"]:
                tp(e, biome)
            else:
                enemy = next(b for b in ENEMIES if b["visual"] == locuteur)
                combat(e, biome, enemy)

        paroles = dialogue(e, LORE[n]["dialogue"], dialogue_active, on_end=on_end)
        preset  = [bg, npc_sprite, sprite, paroles]
        page.add(ft.Stack(preset, expand=True))

    # ─────────────────────────────────────────────────────────────────────────────────────
    # ── Écran planète : sélection du biome ───────────────────────────────────────────────
    # ─────────────────────────────────────────────────────────────────────────────────────

    planet = ft.Stack([
        ft.Container(
            ft.Image(src="assets/imgs/icons/biome_plain.png"),
            alignment=ft.Alignment.CENTER,
            expand=True,
        ),
        ft.Container(
            content=ft.Row([ft.ElevatedButton(
                plaine, on_click=lambda e, b="plain": tp(e, b),
                bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR,
            )]),
            bottom=30, left=30,
        ),
        ft.Container(
            content=ft.Row([ft.ElevatedButton(
                foret, on_click=lambda e, b="forest": tp(e, b),
                bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR,
            )]),
            bottom=30, right=30,
        ),
        ft.Container(
            content=ft.Row([ft.ElevatedButton(
                montagne, on_click=lambda e, b="mountain": tp(e, b),
                bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR,
            )]),
            top=30, right=30,
        ),
        ft.Container(
            content=ft.Row([ft.ElevatedButton(
                lac, on_click=lambda e, b="lake": tp(e, b),
                bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR,
            )]),
            top=30, left=30,
        ),
    ], expand=True)

    def retourneur(e):
        page.on_resize = None
        page.clean()
        navigate("planet")

    return planet