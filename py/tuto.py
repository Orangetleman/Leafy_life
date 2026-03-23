import flet as ft
import flet.canvas as cv



def _tuto(page: ft.Page):
    page.clean()
    tab = ["assets/imgs/biomes/arriere_plain.png","assets/imgs/biomes/arriere_forest.png","assets/imgs/biomes/arriere_lake.png"]
    i = [0]
    img = ft.Image(src="assets/imgs/biomes/arriere_plain.png", border_radius=100)
    imgcont = ft.Container(img,alignment=ft.Alignment.CENTER, expand=True,padding=100)

    def apres():
        i[0] +=1
        if i[0] > len(tab)-1:
            i[0]-=1
        img.src = tab[i[0]]
        page.update()
        
    def avant():
        i[0] -=1
        if i[0] < 0:
            i[0] +=1
        img.src = tab[i[0]]
        page.update()
        
    
    suivant = ft.Container(content=ft.Text(">", size=100, color="blue"), alignment=ft.Alignment.CENTER_RIGHT, on_click=apres)
    precedent = ft.Container(content=ft.Text("<", size=100, color="blue"), alignment=ft.Alignment.CENTER_LEFT, on_click=avant)
    
    return ft.Row([precedent,imgcont,suivant])

