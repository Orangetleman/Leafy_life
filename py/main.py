# -*- coding: utf-8 -*-
"""
Leafy Life - Point d'entrée Flet.
"""

import flet as ft

from datacenter import *
from leafsHome import _build_leafs_home
from planetHome import _planet
from inventoryHome import _build_inventory_home
from shopHome import _build_shop_home

# ---- Données de test ----
def _seed_test_data():
    inventory_manager.append_money("CO2", 1000)
    inventory_manager.append_money("O2",  1000)
    #for key in range(1, 14):
        #leafmanager.add_leaf(LEAFS[key])
    for item in range(1, 14):
        inventory_manager.append_item(ITEMS[item], amount=100)
    pass


def _build_navbar(navigate) -> ft.Row:
    return ft.Row(
        [
            ft.Button("Leafs",     on_click=lambda e: navigate("leafs")),
            ft.Button("Shop",      on_click=lambda e: navigate("shop")),
            ft.Button("Inventory", on_click=lambda e: navigate("inventory")),
            ft.Button("Planet",    on_click=lambda e: navigate("planet")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
    )


def main(page: ft.Page, page_name: str = "leafs") -> None:
    page.title      = "Leafy Life"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor    = "#1a1a1a"
    page.padding    = 0
    page.spacing    = 0

    def show_screen(name: str):
        if hasattr(page, "stop_current_screen"):
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
            body = _planet(page, show_screen)
        else:
            body = _build_leafs_home(page)

        page.add(
            ft.Container(content=_build_navbar(show_screen), padding=8, bgcolor="#131313"),
            ft.Container(
                content=ft.Column(controls=body, expand=True),
                expand=True,
                padding=0,
            )
        )

    # ── Démarrage du game clock ──────────────────────────────────────────────────────────
    # Le callback page.update() rafraîchit l'UI après chaque tick
    # (utile si le modal leaf est ouvert au moment du tick)
    game_clock.add_callback(lambda: page.update())
    game_clock.start(page)

    show_screen(page_name)


if __name__ == "__main__":
    _seed_test_data()
    ft.run(main)