import flet as ft
from pynput import keyboard as pynput_keyboard
from datacenter import *
import asyncio

def _planet(page: ft.Page) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    content = ft.Text("explore", size=16)

    keys_pressed = {"right": False, "left": False}
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

    def dialogue():
        return ft.Container(
            ft.Container(
                content=ft.Text("feur"),
                bgcolor=ft.Colors.with_opacity(0.6, "blue"),
                alignment=ft.Alignment.CENTER_RIGHT,
                height=200,
            ),
            alignment=ft.Alignment.BOTTOM_CENTER
        )


    """===========================================================plaine===================================================================================="""


    def expl_plaine(e):
        page.clean()
        sprite = ft.Container(
            content=ft.Image(src="assets/imgs/icons/type_resurrector.png", width=80, height=60),
            left=0,
            bottom=50,
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )
        biome=ft.Container(
            content=ft.Image(src="assets/imgs/icons/biome_plain.png"),
            expand=True,
        ) # À REGLER LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
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
            while running[0]:
                if keys_pressed["right"]:
                    sprite.left = (sprite.left or 0) + 15
                if keys_pressed["left"]:
                    sprite.left = (sprite.left or 0) - 15
                #print(f"biome.height: {biome.bottom}, page.height: {page.height}")
                sprite.bottom = (biome.bottom / 4) + (page.height-biome.bottom) # Garder le sprite à une hauteur fixe peu importe la taille de la fenêtre # laaaaaaaaaaaaaaaa ausssiiiiiiiii
                page.update()
                await asyncio.sleep(0.025)  # 40 FPS

        game_container = ft.Container(
            content=ft.Stack([
                biome,
                ft.Container(
<<<<<<< HEAD
                    ft.Image(src="assets/imgs/icons/biome_plain.png",
                             width= 200,
                             height= 100),
                ),
                sprite,
            ]),
=======
                    content=ft.Image(src="assets/imgs/icons/arriere_plaine.jpeg"),
                ),
                ft.Container(
                    content=ft.Image(src="assets/imgs/icons/biome_plain.png", width=50, height=50),
                    right=0,
                    bottom=400
                ),
                sprite,
                dialogue()]),
>>>>>>> 2bcdc308f4f164e3999f19c777c133da95470234
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