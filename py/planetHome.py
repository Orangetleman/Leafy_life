import flet as ft
from pynput import keyboard as pynput_keyboard
from datacenter import *
from style import *
import asyncio
import pyglet
import threading
import random

# Charge la musique
'''music = pyglet.media.load("assets/musics/frogmusic.wav", streaming=False)
music_player = pyglet.media.Player()
music_player.queue(music)
music_player.loop = True
music_player.play()

# Lance pyglet en arrière-plan
threading.Thread(target=pyglet.app.run, daemon=True).start()'''


def _planet(page: ft.Page, navigate) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    plaine = ft.Text("explore plaine", size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR)
    foret = ft.Text("explore foret", size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR)
    montagne = ft.Text("explore montagne", size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR)
    lac = ft.Text("explore lac", size=30, color=PLANET_EXPLORE_BUTTON_TEXT_COLOR)


    scene_actu = [0]
    keys_pressed = {"right": False, "left": False, "space": False}
    dialogue_active = [False]
    running = [True]
    focused = [True]

    def on_press(key):
        if not focused[0]:
            return
        if dialogue_active[0]:
            return
        try:
            if key.char in ("d", "D"):
                keys_pressed["right"] = True
            elif key.char in ("q", "Q"):
                keys_pressed["left"] = True
        except AttributeError:
            if key == pynput_keyboard.Key.right:
                keys_pressed["right"] = True
            elif key == pynput_keyboard.Key.left:
                keys_pressed["left"] = True
            elif key == pynput_keyboard.Key.space:
                keys_pressed["space"] = True

    def on_release(key):
        try:
            if key.char in ("d", "D"):
                keys_pressed["right"] = False
            elif key.char in ("q", "Q"):
                keys_pressed["left"] = False
        except AttributeError:
            if key == pynput_keyboard.Key.right:
                keys_pressed["right"] = False
            elif key == pynput_keyboard.Key.left:
                keys_pressed["left"] = False
            elif key == pynput_keyboard.Key.space:
                keys_pressed["space"] = False

    def on_window_event(e):
        if e.type == ft.WindowEventType.FOCUS:
            focused[0] = True
        elif e.type == ft.WindowEventType.BLUR:
            focused[0] = False
            keys_pressed["right"] = False
            keys_pressed["left"] = False

    def dialogue(e, scene, dialogue_active):
        i_scene = [0]

        def next_dialogue(key):
            if key == pynput_keyboard.Key.space:
                if i_scene[0] < len(scene) - 1:
                    i_scene[0] += 1
                    if i_scene[0] % 2 == 0:
                        npc_msg.content.value = scene[i_scene[0]]
                        chara_msg.visible = False
                        npc_msg.visible = True
                    else:
                        chara_msg.content.value = scene[i_scene[0]]
                        chara_msg.visible = True
                        npc_msg.visible = False
                    page.update()
                else:
                    dialogue_box.visible = False
                    dialogue_active[0] = False
                    page.update()
                    listener.stop()

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

    def tp(e,biome):
        page.clean()
        running[0] = True
        event = random.choice(EVENTS)
        biome_icon = next(b["icon"] for b in BIOMES if b["name"] == biome)

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

        new_sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )

        preset = [
            ft.Container(
                content=ft.Image(src=biome_icon, fit="cover"),
                expand=True,
            ),
        ]

        id = None
        emplacement = random.choice([ft.Alignment.CENTER_LEFT, ft.Alignment.CENTER_RIGHT])
        if event== "enemy":
            id = random.choice(ENEMIES)
            preset.append(ft.Container(
                content=ft.Image(src=id["visual"], width=80, height=60),
                alignment=emplacement,
            ))
        elif event== "npc":
            id = random.choice(NPCS)
            preset.append(ft.Container(
                content=ft.Image(src=id["visual"], width=80, height=60),
                alignment=emplacement,
            ))
        elif event== "empty":
            id = random.choice(OBJECTS)
            the_object = ft.Container(
                content=ft.Image(src=id["visual"], width=180, height=160),
                alignment=emplacement,
                visible= True
            )
            preset.append(the_object)

        preset.append(new_sprite)
        preset.append(bouton_retour)
        preset.append(dialogue(e,LORE[scene_actu[0]]['dialogue'],dialogue_active))

        new_listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
        new_listener.start()

        def stop_tp_screen(e=None):
            running[0] = False
            new_listener.stop()

        page.stop_current_screen = stop_tp_screen
        page.window.on_event = on_window_event

        first_sip = [True]
        async def tp_game_loop():
            biome_img_ratio = 1250 / 649
            new_sprite.left = page.width / 2
            while running[0]:
                if dialogue_active[0]:
                    await asyncio.sleep(0.025)
                    continue
                if keys_pressed["right"]:
                    new_sprite.left = new_sprite.left + 15
                if keys_pressed["left"]:
                    new_sprite.left = new_sprite.left - 15

                biome_height = page.width / biome_img_ratio
                new_sprite.bottom = (biome_height / 4) + (page.height - biome_height)

                if new_sprite.left < 0:
                    stop_tp_screen()
                    tp(e,biome)
                    return
                if new_sprite.left > page.width - 150:
                    stop_tp_screen()
                    tp(e,biome)
                    return
                if event== "enemy" and ((new_sprite.left < 200 and emplacement == ft.Alignment.CENTER_LEFT) or (new_sprite.left > (page.width - 300) and emplacement == ft.Alignment.CENTER_RIGHT)) and keys_pressed["space"]:
                    stop_tp_screen()
                    keys_pressed["space"] = False
                    combat(e, biome, id)
                    return
                """if event=="npc" and ((new_sprite.left < 200 and emplacement == ft.Alignment.CENTER_LEFT) or (new_sprite.left > (page.width - 300) and emplacement == ft.Alignment.CENTER_RIGHT)):
                    wandering_shop()"""
                if event== "empty" and ((new_sprite.left < 200 and emplacement == ft.Alignment.CENTER_LEFT) or (new_sprite.left > (page.width - 300) and emplacement == ft.Alignment.CENTER_RIGHT)) and keys_pressed["space"]:
                    if first_sip[0] == True and id["gives"] == "Eau minérale":
                        inventory_manager.append_item(ITEMS[1],3)
                        first_sip[0] = False
                        print("eau recuperee")
                        the_object.visible = False
                        page.update()
                    keys_pressed["space"] = False

                page.update()
                await asyncio.sleep(0.025)

        event_scene = ft.Container(
            content=ft.Stack(preset),
            expand=True,
        )

        page.add(event_scene)
        page.run_task(tp_game_loop)

    def combat(e, biome, enemy):
        page.clean()
        def end():
            if enemy.pv == 0:
                bravo = dialogue(e,victoire,dialogue_active)
                preset.append(bravo)
                page.update
                #wait 3 sec
                if keys_pressed["space"]:
                    keys_pressed["space"] = False
                    tp(e)
        leafsprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            bottom=page.height * PLANET_COMBAT_MENU_HEIGHT_RATIO,
            left=20,
        )
        enemysprite = ft.Container(
            content=ft.Image(src=enemy["visual"], width=150, height=180),
            bottom=page.height * PLANET_COMBAT_MENU_HEIGHT_RATIO,
            right=20,
        )
        menu = ft.Container(
            bottom=0, left=0,
            width=page.width,
            height=page.height * PLANET_COMBAT_MENU_HEIGHT_RATIO,
            bgcolor=ft.Colors.with_opacity(PLANET_COMBAT_MENU_BG_COLOR[0], PLANET_COMBAT_MENU_BG_COLOR[1]),
        )
        """CHRIS A AJOUTER BOUTONS (atk,competence et boite_leaf) + BARRE PV ET INFOS LEAF STP"""

        preset = [
            ft.Container(
                content=ft.Image(src="assets/imgs/icons/arriere_plain.png", fit="cover"),
                expand=True,
            ),
            leafsprite,
            enemysprite,
            menu,
        ]

        layout = ft.Container(content=ft.Stack(preset))
        page.add(layout)

    def atk(leaf, enemy):
        malus = "-" + leaf.atk
        dgts = ft.Container(ft.Text(malus, size=20), visible=True)
        leaf.left = page.width - 20
        page.update()
        page.add(dgts)
        dgts.visible = False
        leaf.left = 20
        page.update()
        enemy.pv -= leaf.atk

    def competence(leaf, enemy):
        if leaf.type == 'dps':
            leaf.atk *= 2
            atk(leaf, enemy)
            leaf.atk /= 2
            return None
        elif leaf.type == 'tank':
            bouclier = ft.Container(ft.Image(src='leaf_type_tank.png', width=100, height=100), visible=True)
            page.add(bouclier)
            enemy.atk /= 2
            tour = 2
            return tour
        else:
            return None

    def boite_leaf():
        pass
    """CHRISSS FAIS ICI"""

    planet = ft.Stack([
        ft.Container(
            ft.Image(src="assets/imgs/icons/biome_plain.png"),
            alignment=ft.Alignment.CENTER,
            expand=True,
        ),
        ft.Container(
            content=ft.Row(
                [ft.ElevatedButton(plaine, on_click=lambda e, b="plain": tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)],
            ),
            bottom=30, left=30,
        ),
        ft.Container(
            content=ft.Row(
                [ft.ElevatedButton(foret, on_click=lambda e, b="forest": tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)],
            ),
            bottom=30, right=30,
        ),
        ft.Container(
            content=ft.Row(
                [ft.ElevatedButton(montagne, on_click=lambda e, b="mountain": tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)],
            ),
            top=30, right=30,
        ),
        ft.Container(
            content=ft.Row(
                [ft.ElevatedButton(lac, on_click=lambda e, b="lake": tp(e, b), bgcolor=PLANET_EXPLORE_BUTTON_BG_COLOR)],
            ),
            top=30, left=30,
        ),
    ], expand=True)

    def retourneur(e):
        page.clean()
        navigate("planet")

    return planet