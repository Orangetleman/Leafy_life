import flet as ft
from pynput import keyboard as pynput_keyboard
from datacenter import *
from style import *
import asyncio
import threading
import random

scene_actu = [0]

# ── Configuration par biome : (largeur_img, hauteur_img, ratio_sol_depuis_bas) ──────────
# ⚠️ Mettre les vraies dimensions des images pour forest/lake/mountain
BIOME_LAYOUT = {
    "plain":    (10000, 5192,  601  / 2596),
    "forest":   (1888, 999,  100  / 333 ),  # ← mettre les vraies dimensions de arriere_forest.png
    "lake":     (1888, 999,  41   / 111 ),  # ← mettre les vraies dimensions de arriere_lake.png
    "mountain": (1888, 999,  31   / 111 ),  # ← mettre les vraies dimensions de arriere_mountain.png
}
BASE_SPEED = 100  # vitesse de référence en pixels à résolution originale de l'image


def compute_layout(page_w, page_h, biome_name):
    """
    Calcule la position du sol (bottom en px depuis le bas de la page) et la vitesse
    en tenant compte du fit="cover" de l'image de fond.
    Avec cover : scale = max(page_w/img_w, page_h/img_h)
    L'image est centrée → elle peut déborder verticalement.
    """
    img_w, img_h, ground_ratio = BIOME_LAYOUT.get(biome_name, (1250, 649, 601/2596))
    scale      = max(page_w / img_w, page_h / img_h)
    disp_w     = img_w * scale
    disp_h     = img_h * scale
    offset_y   = (disp_h - page_h) / 2          # débordement vertical centré
    ground_bot = max(0, disp_h * ground_ratio - offset_y)
    speed      = BASE_SPEED * (disp_w / img_w)   # vitesse proportionnelle à l'image affichée
    return ground_bot, speed


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

    def on_press(key):
        if not focused[0] or dialogue_active[0]:
            return
        try:
            if key.char in ("d", "D"):   keys_pressed["right"] = True
            elif key.char in ("q", "Q"): keys_pressed["left"]  = True
        except AttributeError:
            if   key == pynput_keyboard.Key.right:  keys_pressed["right"] = True
            elif key == pynput_keyboard.Key.left:   keys_pressed["left"]  = True
            elif key == pynput_keyboard.Key.space:  keys_pressed["space"] = True

    def on_release(key):
        try:
            if key.char in ("d", "D"):   keys_pressed["right"] = False
            elif key.char in ("q", "Q"): keys_pressed["left"]  = False
        except AttributeError:
            if   key == pynput_keyboard.Key.right:  keys_pressed["right"] = False
            elif key == pynput_keyboard.Key.left:   keys_pressed["left"]  = False
            elif key == pynput_keyboard.Key.space:  keys_pressed["space"] = False

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
                        npc_msg.content.value   = scene[i_scene[0]]
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

    # ────────────────────────────────────────────────────────────────────────────────────
    def tp(e, biome):
        page.clean()
        running[0]            = True
        event                 = random.choice(EVENTS)
        biome_icon            = next(b["icon"] for b in BIOMES if b["name"] == biome)
        keys_pressed["space"] = False
        dialogue_active[0]    = False

        # ── Layout dynamique partagé ──────────────────────────────────────────────────
        layout = {"bottom": 0, "speed": BASE_SPEED}

        def update_layout():
            g_bot, spd        = compute_layout(page.width, page.height, biome)
            layout["bottom"]  = g_bot
            layout["speed"]   = spd
            new_sprite.bottom = g_bot
            if entity_container is not None:
                entity_container.bottom = g_bot

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
            )
        )

        # ── Sprite joueur ─────────────────────────────────────────────────────────────
        new_sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )

        preset           = [ft.Container(content=ft.Image(src=biome_icon, fit="cover"), expand=True)]
        entity_id        = None
        entity_container = None
        emplacement      = random.choice([ft.Alignment.CENTER_LEFT, ft.Alignment.CENTER_RIGHT])

        if event == "enemy":
            entity_id        = random.choice(ENEMIES)
            entity_container = ft.Container(
                content=ft.Image(src=entity_id["visual"], width=80, height=60),
                alignment=emplacement,
            )
            preset.append(entity_container)

        elif event == "npc":
            entity_id        = random.choice(NPCS)
            entity_container = ft.Container(
                content=ft.Image(src=entity_id["visual"], width=80, height=60),
                alignment=emplacement,
            )
            preset.append(entity_container)

        elif event == "empty":
            entity_id        = random.choice(OBJECTS)
            entity_container = ft.Container(
                content=ft.Image(src=entity_id["visual"], width=180, height=160),
                alignment=emplacement,
                visible=True,
            )
            preset.append(entity_container)

        else:  # lore
            entity_id        = LORE[scene_actu[0]]["visual"]
            entity_container = ft.Container(
                content=ft.Image(src=entity_id, width=80, height=60),
                alignment=emplacement,
            )
            preset.append(entity_container)

        preset.append(new_sprite)
        preset.append(bouton_retour)

        # ── Initialisation + on_resize ────────────────────────────────────────────────
        update_layout()
        new_sprite.left = page.width / 2

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

        async def tp_game_loop():
            while running[0]:
                moved = False
                if not dialogue_active[0]:
                    if keys_pressed["right"]:
                        new_sprite.left += layout["speed"]
                        moved = True
                    if keys_pressed["left"]:
                        new_sprite.left -= layout["speed"]
                        moved = True

                near_left  = new_sprite.left < 200              and emplacement == ft.Alignment.CENTER_LEFT
                near_right = new_sprite.left > page.width - 300 and emplacement == ft.Alignment.CENTER_RIGHT

                # Sorties latérales
                if new_sprite.left < 0:
                    stop_tp_screen()
                    tp(e, biome)
                    return
                if new_sprite.left > page.width - 150:
                    stop_tp_screen()
                    tp(e, biome)
                    return

                # Interactions
                if event == "enemy" and (near_left or near_right) and keys_pressed["space"]:
                    stop_tp_screen()
                    keys_pressed["space"] = False
                    combat(e, biome, entity_id)
                    return

                if event == "empty" and (near_left or near_right) and keys_pressed["space"]:
                    if first_sip[0] and entity_id["gives"] == "Eau minérale":
                        inventory_manager.append_item(ITEMS[1], 3)
                        first_sip[0]             = False
                        entity_container.visible = False
                        page.update()
                    keys_pressed["space"] = False

                if event == "lore" and (near_left or near_right) and keys_pressed["space"]:
                    keys_pressed["space"] = False
                    stop_tp_screen()
                    declenche_scene(e, biome, scene_actu[0])
                    return

                if moved:
                    page.update()
                await asyncio.sleep(0.025)

        page.add(ft.Container(content=ft.Stack(preset), expand=True))
        page.run_task(tp_game_loop)

    # ────────────────────────────────────────────────────────────────────────────────────
    def combat(e, biome, enemy):
        page.clean()
        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)
        g_bot, _   = compute_layout(page.width, page.height, biome)

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
            bgcolor=ft.Colors.with_opacity(PLANET_COMBAT_MENU_BG_COLOR[0], PLANET_COMBAT_MENU_BG_COLOR[1]),
        )
        """CHRIS A AJOUTER BOUTONS (atk, competence, boite_leaf) + BARRE PV ET INFOS LEAF"""

        preset = [
            ft.Container(content=ft.Image(src=biome_icon, fit="cover"), expand=True),
            leafsprite,
            enemysprite,
            menu,
        ]

        def on_resize_combat(ev):
            g, _ = compute_layout(page.width, page.height, biome)
            leafsprite.bottom  = g
            enemysprite.bottom = g
            page.update()

        page.on_resize = on_resize_combat
        page.add(ft.Container(content=ft.Stack(preset), expand=True))

    # ────────────────────────────────────────────────────────────────────────────────────
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
        if leaf.type == 1:   # attacker
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

    # ────────────────────────────────────────────────────────────────────────────────────
    def declenche_scene(e, biome, n):
        if hasattr(page, "stop_current_screen"):
            page.stop_current_screen()
        dialogue_active[0] = True
        page.clean()

        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)
        locuteur   = LORE[n]["visual"]
        g_bot, _   = compute_layout(page.width, page.height, biome)

        sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            bottom=g_bot, left=20,
        )
        npc_sprite = ft.Container(
            content=ft.Image(src=locuteur, width=150, height=180),
            bottom=g_bot, right=20,
        )

        def on_resize_scene(ev):
            g, _ = compute_layout(page.width, page.height, biome)
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
        preset  = [
            ft.Container(content=ft.Image(src=biome_icon, fit="cover"), expand=True),
            npc_sprite,
            sprite,
            paroles,
        ]
        page.add(ft.Stack(preset, expand=True))

    # ── Écran planète (sélection du biome) ───────────────────────────────────────────────
    planet = ft.Stack([
        ft.Container(ft.Image(src="assets/imgs/icons/biome_plain.png"), alignment=ft.Alignment.CENTER, expand=True),
        ft.Container(
            content=ft.Row([ft.ElevatedButton(plaine,   on_click=lambda e, b="plain":    tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)]),
            bottom=30, left=30,
        ),
        ft.Container(
            content=ft.Row([ft.ElevatedButton(foret,    on_click=lambda e, b="forest":   tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)]),
            bottom=30, right=30,
        ),
        ft.Container(
            content=ft.Row([ft.ElevatedButton(montagne, on_click=lambda e, b="mountain": tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)]),
            top=30, right=30,
        ),
        ft.Container(
            content=ft.Row([ft.ElevatedButton(lac,      on_click=lambda e, b="lake":     tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)]),
            top=30, left=30,
        ),
    ], expand=True)

    def retourneur(e):
        page.on_resize = None
        page.clean()
        navigate("planet")

    return planet