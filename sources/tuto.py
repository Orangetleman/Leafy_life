import flet as ft
import flet.canvas as cv

def _tuto(page: ft.Page):
    page.clean()
    tab = ["assets/imgs/tuto/tuto1.png","assets/imgs/tuto/tuto2.png","assets/imgs/tuto/tuto3.png","assets/imgs/tuto/tuto4.png","assets/imgs/tuto/tuto5.png","assets/imgs/tuto/tuto6.png"]
    i = [0]
    img = ft.Image(src=tab[i[0]], border_radius=50)
    imgcont = ft.Container(img, expand=True, margin=50, border_radius=75,
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(15, "#7a6a00"),
                            width=page.width * 0.7,
                            height=page.height * 0.8,
                            bgcolor="#274f9ec6")

    def next(e):
        if i[0] < len(tab)-1:
            i[0] += 1
            img.src = tab[i[0]]
            precedent.visible = True
            if i[0] == len(tab)-1:
                suivant.visible = False
        page.update()

    def before(e):
        if i[0] > 0:
            i[0] -= 1
            img.src = tab[i[0]]
            suivant.visible = True
            if i[0] == 0:
                precedent.visible = False
        page.update()

    def on_resize(e):
        imgcont.width  = page.width * 0.7   # ← on applique directement au container
        imgcont.height = page.height * 0.8
        page.update()

    page.on_resized = on_resize  # ← sans parenthèses

    suivant  = ft.Container(content=ft.Text(">", size=100, color="blue"), alignment=ft.Alignment.CENTER_RIGHT, on_click=lambda e: next(e))
    precedent = ft.Container(content=ft.Text("<", size=100, color="blue"), visible=False, alignment=ft.Alignment.CENTER_LEFT, on_click=lambda e: before(e))

    return ft.Row([precedent, imgcont, suivant], expand=True)