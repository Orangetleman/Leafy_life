import flet as ft
from pynput import keyboard as pynput_keyboard
from datacenter import *
import asyncio
import pyglet
import threading

# Charge la musique
music = pyglet.media.load("assets/musics/frogmusic.wav", streaming=False)
music_player = pyglet.media.Player()
music_player.queue(music)
music_player.loop = True
music_player.play()

# Lance pyglet en arrière-plan
threading.Thread(target=pyglet.app.run, daemon=True).start()


def _planet(page: ft.Page) -> list:
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
                    dialogue_box.visible = False  # 👈 cache tout quand c'est fini
                    dialogue_box.update()
                    listener.stop()  # 👈 arrête le listener pynput


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


    """===========================================================plaine===================================================================================="""


    def expl_plaine(e):
        page.clean()
        sprite = ft.Container(
            content=ft.Image(src="assets/imgs/icons/type_resurrector.png", width=80, height=60),
            left=0,
            bottom=50,
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )
        listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        def stop_game(e=None):
            print("stop_game appelé")
            running[0] = False
            listener.stop()
            print("listener stoppé, running:", running[0])

        page.stop_current_screen = stop_game
        page.window.on_event = on_window_event

        async def game_loop():
            biome_img_ratio = 1250 / 649
            while running[0]:
                if keys_pressed["right"]:
                    sprite.left = (sprite.left or 0) + 15
                if keys_pressed["left"]:
                    sprite.left = (sprite.left or 0) - 15
                
                biome_height = page.width / biome_img_ratio
                sprite.bottom = (biome_height / 4) + (page.height - biome_height)
                page.update()
                await asyncio.sleep(0.025)  # 40 FPS

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
                dialogue(e,s1)]),
            expand=True
        )

        page.add(game_container)
        page.run_task(game_loop)

    """===========================================================foret===================================================================================="""


    return [ft.Stack([
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
    ])]