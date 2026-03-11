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

    content = ft.Text("explore", size=16)

    keys_pressed = {"right": False, "left": False, "space":False}
    running = [True]
    focused = [True]

    def on_press(key):
            if not focused[0]:
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

    
    def on_window_event(e):
        if e.type == ft.WindowEventType.FOCUS:
            focused[0] = True
        elif e.type == ft.WindowEventType.BLUR:
            focused[0] = False
            keys_pressed["right"] = False
            keys_pressed["left"] = False

    def dialogue(e, scene):
        i_scene = [0]

        def next_dialogue(key):
            if key == pynput_keyboard.Key.space:
                if i_scene[0] < len(scene) - 1:  
                    i_scene[0] += 1
                    if i_scene[0]%2==0:
                        npc_msg.content.value = scene[i_scene[0]] 
                        chara_msg.visible = False
                        npc_msg.visible = True
                    else:
                        chara_msg.content.value = scene[i_scene[0]] 
                        chara_msg.visible = True
                        npc_msg.visible = False
                    chara_msg.update()
                    npc_msg.update()
                else:
                    dialogue_box.visible = False  
                    dialogue_box.update()
                    listener.stop()  


        msg=scene[i_scene[0]]
        
        chara_msg = ft.Container(
                content=ft.Text(msg,size= 30),
                bgcolor=ft.Colors.with_opacity(0.6, "green"),
                alignment=ft.Alignment.CENTER_RIGHT,
                height=200,
                visible=False
            )
        
        npc_msg = ft.Container(
                content=ft.Text(msg,size= 30),
                bgcolor=ft.Colors.with_opacity(0.6, "green"),
                alignment=ft.Alignment.CENTER_LEFT,
                height=200,
                visible=True
            )
        
        dialogue_box = ft.Container(content= ft.Stack([chara_msg, npc_msg]),
            alignment=ft.Alignment.BOTTOM_CENTER
        )
        
        listener = pynput_keyboard.Listener(on_press=next_dialogue)
        listener.start()

        return dialogue_box
    
    def tp(e):
        page.clean()
        running[0] = True
        event = random.choice(EVENTS["plain"])

        le_txt = ft.Text('planet', size=30)

        bouton_retour = ft.Container(
            content=ft.Row(
                [ft.ElevatedButton(le_txt, on_click=retourneur)],  # ← ajouter []
                alignment=ft.Alignment.TOP_LEFT,
            )
        )

        new_sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )

        preset = [
            ft.Container(
                content=ft.Image(src="assets/imgs/icons/arriere_plain.png", fit="cover"),
                expand=True,
            ),
        ]

        emplacement = random.choice([ft.Alignment.CENTER_LEFT, ft.Alignment.CENTER_RIGHT])
        if event["type"] == "enemy":
            enemyid = random.choice(ENEMIES)
            preset.append(ft.Container(
                content=ft.Image(src=enemyid["visual"], width=80, height=60),
                alignment=emplacement,
            ))
        elif event["type"] == "npc":
            npcid = random.choice(NPCS)
            preset.append(ft.Container(
                content=ft.Image(src=npcid["visual"], width=80, height=60),
                alignment=emplacement,
            ))

        preset.append(new_sprite)
        preset.append(bouton_retour)
        

        new_listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
        new_listener.start()

        def stop_tp_screen(e=None):
            running[0] = False
            new_listener.stop()

        page.stop_current_screen = stop_tp_screen
        page.window.on_event = on_window_event

        async def tp_game_loop():
            biome_img_ratio = 1250 / 649
            new_sprite.left = page.width / 2  # ← init immédiate, pas après sleep
            while running[0]:
                if keys_pressed["right"]:
                    new_sprite.left = new_sprite.left + 15
                if keys_pressed["left"]:
                    new_sprite.left = new_sprite.left - 15

                biome_height = page.width / biome_img_ratio
                new_sprite.bottom = (biome_height / 4) + (page.height - biome_height)

                if new_sprite.left < 0:
                    stop_tp_screen()
                    tp(e)
                    return
                if new_sprite.left > page.width - 150:
                    stop_tp_screen()
                    tp(e)
                    return
                if (new_sprite.left < 100 and emplacement == ft.Alignment.CENTER_LEFT) or (new_sprite.left > (page.width - 200) and emplacement == ft.Alignment.CENTER_RIGHT):
                    combat()


                page.update()
                await asyncio.sleep(0.025)
        
        event_scene = ft.Container(
            content=ft.Stack(preset),
            expand=True,
        )

        page.add(event_scene)
        page.run_task(tp_game_loop)

    def combat():
        page.clean()
        page.add(ft.Container(content=ft.Text('FEUR', size=800)))



    """===========================================================plaine===================================================================================="""
    listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
    def stop_game(e=None):
            print("stop_game appelé")
            running[0] = False
            listener.stop()
            print("listener stoppé, running:", running[0])

    def expl_plaine(e):
        running[0] = True
        page.clean()
        sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )
        
        listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        page.stop_current_screen = stop_game
        page.window.on_event = on_window_event


        le_txt = ft.Text('planet', size=30)

        bouton_retour = ft.Container(
            content=ft.Row(
                [ft.ElevatedButton(le_txt, on_click=retourneur)],
                alignment=ft.Alignment.TOP_LEFT,
            )
        )

        game_container = ft.Container(
            content=ft.Stack([
                ft.Container(
                    content=ft.Image(
                        src="assets/imgs/icons/arriere_plain.png",
                        fit="cover",
                    ),
                    expand=True,
                ),
                
                ft.Container(
                    content=ft.Image(src="assets/imgs/icons/biome_plain.png", width=50, height=50),
                    right=0,
                    bottom=400
                ),
                sprite,
                dialogue(e,s1),bouton_retour]),
            expand=True
        )

        async def game_loop():
            biome_img_ratio = 1250 / 649
            sprite.left=page.width/2
            while running[0]:
                if keys_pressed["right"]:
                    sprite.left = (sprite.left) + 15
                if keys_pressed["left"]:
                    sprite.left = (sprite.left) - 15
                
                biome_height = page.width / biome_img_ratio
                sprite.bottom = (biome_height / 4) + (page.height - biome_height)

                if sprite.left < 0:
                    stop_game()
                    tp(e)
                    return
                if sprite.left > page.width - 150:
                    stop_game()
                    tp(e)
                    return
                page.update()
                await asyncio.sleep(0.025)  # 40 FPS

        page.add(game_container)
        page.run_task(game_loop)

    """===========================================================foret===================================================================================="""



    
    planet = ft.Stack([
        ft.Container(
            ft.Image(src="assets/imgs/icons/biome_plain.png"),
            expand=True
        ),
        ft.Container(
            content=ft.Row(
                [ft.IconButton(content, on_click=expl_plaine)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=300,
            height=300,
        )
    ])

    def retourneur(e):
        stop_game()
        page.clean()
        navigate("planet")

    return planet