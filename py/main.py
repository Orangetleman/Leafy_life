# -*- coding: utf-8 -*-
"""
Leafy Life - Point d'entrée Flet.
Remplace index.html + main.js + router.js.
Gère la navigation entre les vues (écrans) et la barre de navigation.
"""

import flet as ft

from datacenter import *
from leafsHome import _build_leafs_home
from planetHome import _planet
from inventoryHome import _build_inventory_home
from shopHome import _build_shop_home

# ---- Données de test (équivalent du seed dans navbar.js) ----
def _seed_test_data():
    inventory_manager.append_money("CO2",1000)
    inventory_manager.append_money("O2",1000)
    for key in range(0, 11):
        leafmanager.add_leaf(LEAFS[key])
    for item in range(1,14):
        inventory_manager.append_item(ITEMS[item], amount=100)


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

def _build_placeholder(title: str) -> list:
    """Vue de remplacement pour les écrans non encore migrés."""
    return [
        ft.Container(
            content=ft.Text(f"{title} – Écran en cours de migration.", size=16),
            padding=20,
            alignment=ft.Alignment(0, 0),
        )
    ]

def main(page: ft.Page) -> None:
    page.title = "Leafy Life"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1a1a1a"

    def show_screen(name: str):
        if hasattr(page, 'stop_current_screen'):
            page.stop_current_screen()
            del page.stop_current_screen
        page.clean()
        
        if name == "leafs":
            body = _build_leafs_home(page)
        elif name == "shop":
            body = _build_shop_home(page)
        elif name == "inventory":
            body = _build_inventory_home(page)
        elif name == "planet":
            body = _planet(page)
        else:
            body = _build_leafs_home(page)

        page.add(
            ft.Container(content=_build_navbar(show_screen), padding=8, bgcolor="#131313"),
            ft.Container(
                content=ft.Column(controls=body, expand=True),  # ← controls= explicite
                expand=True,
            )
        )

    show_screen("leafs")

if __name__ == "__main__":
    _seed_test_data()
    ft.run(main)
