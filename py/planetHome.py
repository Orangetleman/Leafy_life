import flet as ft
from datacenter import ENEMIES

def _planet(page: ft.Page) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    content=ft.Text("explore", size=16)

    def expl_plaine(e):
        page.clean()
        sprite = ft.Container(content= ft.Image(src="assets/imgs/icons/type_resurrector.png", width=80, height=60),left=0,bottom=400)

        def on_keyboard(e: ft.KeyboardEvent):
            if e.key == "Arrow Right":
                sprite.left += 100
                page.update()
            if e.key == "Arrow Left":
                sprite.left -= 100
                page.update()

        page.on_keyboard_event = on_keyboard  # 👈 écoute le clavier

        page.add(
            ft.Stack([
                ft.Container(
                    content= ft.Image(
                    src="assets/imgs/icons/arriere_plaine.png"),
                    expand=True,
                    ),
                ft.Container(content= ft.Image(src="assets/imgs/icons/biome_plain.png", width=50, height=50),right=0,bottom=400),
                sprite
                ]))
            
        
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