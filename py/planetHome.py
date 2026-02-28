import flet as ft
from datacenter import ENEMIES

def _planet(page: ft.Page) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    content=ft.Text("explore", size=16)

    def expl_plaine(e):
        page.clean()
        sprite = ft.Container(content= ft.Image(src="assets/imgs/icons/type_resurrector.png", width=80, height=60),left=0,bottom=400)
        
        # Dictionnaire pour tracker les touches pressées
        keys_pressed = {"ArrowRight": False, "ArrowLeft": False}
        last_keys = {}
        
        def on_keyboard_event(e: ft.KeyboardEvent):
            print(f"Key pressed: {e.key}")
            # Détecte si c'est un "up" : la touche était pressée avant et ne l'est plus
            if e.key in last_keys:
                keys_pressed[e.key] = False
                del last_keys[e.key]
                print(f"{e.key} released")
            else:
                # C'est un "down"
                if e.key == "D" or e.key == "ArrowRight":
                    keys_pressed["ArrowRight"] = True
                    last_keys["ArrowRight"] = True
                    print("Right pressed")
                elif e.key == "Q" or e.key == "ArrowLeft":
                    keys_pressed["ArrowLeft"] = True
                    last_keys["ArrowLeft"] = True
                    print("Left pressed")
        
        def update_position():
            if keys_pressed["ArrowRight"]:
                sprite.left += 10
            if keys_pressed["ArrowLeft"]:
                sprite.left -= 10
            page.update()
        
        # Mise à jour continuelle de la position
        import time
        import threading
        
        def game_loop():
            while True:
                update_position()
                time.sleep(0.05)  # 50ms = ~20 FPS
        
        thread = threading.Thread(target=game_loop, daemon=True)
        thread.start()

        game_container = ft.Container(
            content=ft.Stack([
                ft.Container(
                    content= ft.Image(src="assets/imgs/icons/arriere_plaine.png"),
                    expand=True,
                ),
                ft.Container(content= ft.Image(src="assets/imgs/icons/biome_plain.png", width=50, height=50),right=0,bottom=400),
                sprite
            ]),
            expand=True
        )
        
        page.on_keyboard_event = on_keyboard_event
        page.add(game_container)
            
        
    return ft.Stack([
            ft.Container(ft.Image(
                src="assets/imgs/icons/biome_plain.png",
                
            ),expand=True),
            ft.Container(
                content=ft.Row(
                    [
                        ft.IconButton(content, on_click=expl_plaine),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=300,
                height=300,
            )
    ])
    

print(ENEMIES[0]["visual"])