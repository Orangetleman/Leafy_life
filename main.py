# -*- coding: utf-8 -*-
"""
Leafy Life - Point d'entrée Flet.
Remplace index.html + main.js + router.js.
Gère la navigation entre les vues (écrans) et la barre de navigation.
"""

import flet as ft

from js.css.styles import COLOR_NAVBAR_BG
from js.data.leafs import LEAFS
from js.gameplay.leafs.leaf_manager import leaf_manager
from js.screens.leafs.leafs_home import build_leafs_home
from js.screens.navigation.navbar import build_navbar


def _seed_test_data():
    """Données de test (équivalent du seed dans navbar.js)."""
    for key in (0, 2, 4, 6, 8):
        leaf_manager.add_leaf(LEAFS[key])


def _build_placeholder(title: str) -> list:
    """Vue de remplacement pour les écrans non encore migrés."""
    return [
        ft.Container(
            content=ft.Text(f"{title} – Écran en cours de migration.", size=16),
            padding=20,
            alignment=ft.alignment.center,
        )
    ]


def main(page: ft.Page) -> None:
    page.title = "Leafy Life"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(e) -> None:
        # Au premier appel, e peut être None ou un événement sans .route : utiliser page.route
        route = getattr(e, "route", None) if e is not None else None
        if route is None or route == "":
            route = "/leafs"
        page.controls.clear()
        page.views.clear()
        navbar = build_navbar(page)
        navbar_container = ft.Container(
            content=navbar,
            padding=8,
            bgcolor=COLOR_NAVBAR_BG,
        )

        if route in ("/", "/leafs"):
            body = build_leafs_home(page)
            page.views.append(
                ft.View(
                    "/leafs",
                    [navbar_container, *body],
                    padding=0,
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        elif route == "/shop":
            page.views.append(
                ft.View(
                    "/shop",
                    [navbar_container, *_build_placeholder("Shop")],
                    padding=0,
                )
            )
        elif route == "/inventory":
            page.views.append(
                ft.View(
                    "/inventory",
                    [navbar_container, *_build_placeholder("Inventory")],
                    padding=0,
                )
            )
        elif route == "/planet":
            page.views.append(
                ft.View(
                    "/planet",
                    [navbar_container, *_build_placeholder("Planet")],
                    padding=0,
                )
            )
        else:
            body = build_leafs_home(page)
            page.views.append(
                ft.View(
                    "/leafs",
                    [navbar_container, *body],
                    padding=0,
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        page.update()

    def view_pop(e: ft.ViewPopEvent) -> None:
        page.views.pop()
        if page.views:
            top = page.views[-1]
            page.push_route(top.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    _seed_test_data()

    # Affichage initial : ajouter le contenu directement à la page (les Views ne s'affichent pas toujours au premier paint)
    navbar = build_navbar(page)
    navbar_container = ft.Container(
        content=navbar,
        padding=8,
        bgcolor=COLOR_NAVBAR_BG,
    )
    body = build_leafs_home(page)
    for control in [navbar_container, *body]:
        page.add(control)
    page.route = "/leafs"
    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
