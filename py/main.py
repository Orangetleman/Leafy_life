# -*- coding: utf-8 -*-
"""
Leafy Life - Point d'entrée Flet.
Remplace index.html + main.js + router.js.
Gère la navigation entre les vues (écrans) et la barre de navigation.
"""

import flet as ft

from leafs import LEAFS
from datacenter import *

# ---- Données de test (équivalent du seed dans navbar.js) ----
def _seed_test_data():
    for key in (0, 2, 4, 6, 8):
        leafmanager.add_leaf(LEAFS[key])


def _build_navbar(navigate) -> ft.Row:
    return ft.Row(
        [
            ft.Button("Leafs",      on_click=lambda e: navigate("leafs")),
            ft.Button("Shop",       on_click=lambda e: navigate("shop")),
            ft.Button("Inventory",  on_click=lambda e: navigate("inventory")),
            ft.Button("Planet",     on_click=lambda e: navigate("planet")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
    )

def _build_leafs_home(page: ft.Page) -> list:
    """
    Contenu de l'écran Leafs (équivalent de js/screens/leafs/leafsHome.js).
    Retourne la liste des contrôles du corps de la vue.
    """
    title = ft.Text("Vos leafs", size=22, weight=ft.FontWeight.BOLD)
    list_container = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=8,
    )

    def on_search_change(e):
        query = (e.control.value or "").strip().lower()
        list_container.controls.clear()
        for leaf in leafmanager.owned:
            if not query or query in leaf.name.lower():
                list_container.controls.append(
                    ft.ListTile(
                        title=ft.Text(leaf.name),
                        leading=ft.Image(src=leaf.img, width=48, height=48, fit=ft.ImageFit.CONTAIN),
                    )
                )
        page.update()

    search = ft.TextField(
        hint_text="🔍 Rechercher...",
        on_change=on_search_change,
        expand=True,
    )

    for leaf in leafmanager.owned:
        list_container.controls.append(
            ft.ListTile(
                title=ft.Text(leaf.name),
                leading=ft.Image(src=leaf.img, width=48, height=48, fit=ft.ImageFit.CONTAIN),
            )
        )

    return [
        ft.Container(
            content=ft.Column(
                [
                    ft.Row([title], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([search], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Container(content=list_container, expand=True),
                ],
                expand=True,
            ),
            padding=16,
            bgcolor="#f0f8ff",
            border_radius=8,
        )
    ]


def _build_placeholder(title: str) -> list:
    """Vue de remplacement pour les écrans non encore migrés."""
    return [
        ft.Container(
            content=ft.Text(f"{title} – Écran en cours de migration.", size=16),
            padding=20,
            alignment=ft.Alignment(0, 0),
        )
    ]


'''def main(page: ft.Page) -> None:
    page.title = "Leafy Life"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    def route_change(e: ft.RouteChangeEvent) -> None:
        route = e.route or "/leafs"
        page.views.clear()
        navbar = _build_navbar(page)

        # Vue racine : Leafs par défaut
        if route in ("/", "/leafs"):
            body = _build_leafs_home(page)
            page.views.append(
                ft.View(
                    "/leafs",
                    [ft.Container(content=navbar, padding=8, bgcolor="#131313"), *body],
                    padding=0,
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        elif route == "/shop":
            page.views.append(
                ft.View(
                    "/shop",
                    [ft.Container(content=navbar, padding=8, bgcolor="#131313"), *_build_placeholder("Shop")],
                    padding=0,
                )
            )
        elif route == "/inventory":
            page.views.append(
                ft.View(
                    "/inventory",
                    [ft.Container(content=navbar, padding=8, bgcolor="#131313"), *_build_placeholder("Inventory")],
                    padding=0,
                )
            )
        elif route == "/planet":
            page.views.append(
                ft.View(
                    "/planet",
                    [ft.Container(content=navbar, padding=8, bgcolor="#131313"), *_build_placeholder("Planet")],
                    padding=0,
                )
            )
        else:
            page.views.append(
                ft.View(
                    "/leafs",
                    [ft.Container(content=navbar, padding=8, bgcolor="#131313"), *_build_leafs_home(page)],
                    padding=0,
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        page.update()

    input = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)        #test de flet, exemple simple pour boutons + boite de texte

    def minus_click(e):
        input.value = str(int(input.value) - 1)

    def plus_click(e):
        input.value = str(int(input.value) + 1)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                input,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
        )
    )                                                                                  #a voir pour une flexibox

       

    def view_pop(e: ft.ViewPopEvent) -> None:
        page.views.pop()
        if page.views:
            top = page.views[-1]
            page.go(top.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    _seed_test_data()
    page.go(page.route or "/leafs")'''
def main(page: ft.Page) -> None:
    page.title = "Leafy Life"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1a1a1a"

    def show_screen(name: str):
        page.clean()
        
        if name == "leafs":
            body = _build_leafs_home(page)
        elif name == "shop":
            body = _build_placeholder("Shop")
        elif name == "inventory":
            body = _build_placeholder("Inventory")
        elif name == "planet":
            body = _build_placeholder("Planet")
        else:
            body = _build_leafs_home(page)

        page.add(
            ft.Container(content=_build_navbar(show_screen), padding=8, bgcolor="#131313"),
            *body,
        )

    show_screen("leafs")

if __name__ == "__main__":
    #ft.run(target=main, assets_dir="assets")
    ft.run(main)
