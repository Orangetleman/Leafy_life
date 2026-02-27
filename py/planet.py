import flet as ft

def _planet(page: ft.Page) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    content=ft.Text("explore", size=16)

    def plus_click(e):
        page.clean()
        page.add(ft.Text("caca", size=16))
        
    return [ft.Container(ft.Stack(
        [
            ft.Image(
                src="assets/imgs/icons/biome_plain.png",
                width=1000,
                height=1000,
                fit="cover",
            ),
            ft.Container(
                content=ft.Row(
                    [
                        ft.IconButton(content, on_click=plus_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=300,
                height=300,
            ),
        ]
    ))]


