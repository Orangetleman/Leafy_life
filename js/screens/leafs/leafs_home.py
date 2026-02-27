# -*- coding: utf-8 -*-
"""
Écran « Vos leafs » (équivalent de js/screens/leafs/leafsHome.js).
Retourne la liste des contrôles du corps de la vue.
"""

import flet as ft

from js.css.styles import (
    BORDER_RADIUS_DEFAULT,
    BORDER_RADIUS_LARGE,
    COLOR_LEAFS_BG,
    COLOR_LEAFS_TITLE_BG,
    COLOR_LEAFS_TITLE_BORDER,
    COLOR_SEARCH_BAR_BG,
    COLOR_SEARCH_BAR_BORDER,
)
from js.gameplay.leafs.leaf_manager import leaf_manager


def build_leafs_home(page: ft.Page) -> list:
    """
    Construit le contenu de l'écran Leafs : titre, barre de recherche, liste des leafs.
    Retourne une liste de contrôles Flet à insérer dans la vue.
    """
    title_text = ft.Text(
        "Vos leafs",
        size=22,
        weight=ft.FontWeight.BOLD,
    )
    title_box = ft.Container(
        content=ft.Row([title_text], alignment=ft.MainAxisAlignment.CENTER),
        border=ft.border.all(2, COLOR_LEAFS_TITLE_BORDER),
        bgcolor=COLOR_LEAFS_TITLE_BG,
        border_radius=BORDER_RADIUS_LARGE,
        padding=8,
    )
    list_container = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=8,
    )

    def on_search_change(e):
        query = (e.control.value or "").strip().lower()
        list_container.controls.clear()
        for leaf in leaf_manager.owned:
            if not query or query in leaf.name.lower():
                list_container.controls.append(
                    ft.ListTile(
                        title=ft.Text(leaf.name),
                        leading=ft.Image(
                            src=leaf.img,
                            width=48,
                            height=48,
                            fit=ft.BoxFit.CONTAIN,
                        ),
                    )
                )
        page.update()

    search = ft.TextField(
        hint_text="🔍 Rechercher...",
        on_change=on_search_change,
        expand=True,
        bgcolor=COLOR_SEARCH_BAR_BG,
        border_color=COLOR_SEARCH_BAR_BORDER,
        border_radius=BORDER_RADIUS_DEFAULT,
    )

    for leaf in leaf_manager.owned:
        list_container.controls.append(
            ft.ListTile(
                title=ft.Text(leaf.name),
                leading=ft.Image(
                    src=leaf.img,
                    width=48,
                    height=48,
                    fit=ft.BoxFit.CONTAIN,
                ),
            )
        )

    return [
        ft.Container(
            content=ft.Column(
                [
                    ft.Row([title_box], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([search], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Container(content=list_container),
                ],
            ),
            padding=16,
            bgcolor=COLOR_LEAFS_BG,
            border_radius=BORDER_RADIUS_DEFAULT,
        )
    ]
