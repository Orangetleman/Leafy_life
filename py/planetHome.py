import flet as ft
from datacenter import ENEMIES

def _planet(page: ft.Page) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    content=ft.Text("explore", size=16)

    def expl_plaine(e):
        page.clean()
        page.add(
            ft.Stack([
                ft.Container(
                    content= ft.Image(
                    src="assets/imgs/icons/arriere_plaine.png"),
                    expand=True,
                    ),
                ft.Container(content= ft.Image(src=ENEMIES[0]["visual"]),expand=True)
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
    


