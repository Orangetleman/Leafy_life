import flet as ft
import flet.canvas as cv



def _tuto(page: ft.Page):
    page.clean()
    tab = ["assets/imgs/biomes/arriere_plain.png","assets/imgs/biomes/arriere_forest.png","assets/imgs/biomes/arriere_lake.png"]
    i = [0]
    img = [ft.Image(src="assets/imgs/biomes/arriere_plain.png", border_radius=100)]
    imgcont = [ft.Container(img[0],alignment=ft.Alignment.CENTER, expand=True,padding=100)]

    def apres():
        i[0] +=1
        if i[0] > len(tab)-1:
            i[0]-=1
        img[0] = ft.Image(src=tab[i[0]], border_radius=100)
        imgcont[0] = ft.Container(img[0],alignment=ft.Alignment.CENTER, expand=True,padding=100)
        
    def avant():
        i[0] -=1
        if i[0] < 0:
            i[0] +=1
        img[0] = ft.Image(src=tab[i[0]], border_radius=100)
        imgcont[0] = ft.Container(img[0],alignment=ft.Alignment.CENTER, expand=True,padding=100)
        
    
    suivant = ft.Container(content=ft.Text(">", size=100, color="blue"), alignment=ft.Alignment.CENTER_RIGHT, on_click=apres)
    precedent = ft.Container(content=ft.Text("<", size=100, color="blue"), alignment=ft.Alignment.CENTER_LEFT, on_click=avant)
    
    return ft.Row([precedent,imgcont[0],suivant])

