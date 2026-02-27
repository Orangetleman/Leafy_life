# -*- coding: utf-8 -*-
"""
Barre de navigation (équivalent de js/screens/navigation/navbar.js).
"""

import flet as ft

from js.css.styles import (
    COLOR_NAVBAR_BG,
    COLOR_NAVBAR_LINK_BG,
    COLOR_NAVBAR_LINK_TEXT,
)


def build_navbar(page: ft.Page) -> ft.Row:
    """Construit la barre de navigation avec les boutons Leafs, Shop, Inventory, Planet."""
    return ft.Row(
        [
            ft.ElevatedButton(
                "Leafs",
                on_click=lambda e: page.push_route("/leafs"),
                style=ft.ButtonStyle(bgcolor=COLOR_NAVBAR_LINK_BG, color=COLOR_NAVBAR_LINK_TEXT),
            ),
            ft.ElevatedButton(
                "Shop",
                on_click=lambda e: page.push_route("/shop"),
                style=ft.ButtonStyle(bgcolor=COLOR_NAVBAR_LINK_BG, color=COLOR_NAVBAR_LINK_TEXT),
            ),
            ft.ElevatedButton(
                "Inventory",
                on_click=lambda e: page.push_route("/inventory"),
                style=ft.ButtonStyle(bgcolor=COLOR_NAVBAR_LINK_BG, color=COLOR_NAVBAR_LINK_TEXT),
            ),
            ft.ElevatedButton(
                "Planet",
                on_click=lambda e: page.push_route("/planet"),
                style=ft.ButtonStyle(bgcolor=COLOR_NAVBAR_LINK_BG, color=COLOR_NAVBAR_LINK_TEXT),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
    )
