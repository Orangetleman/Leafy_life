import flet as ft
from datacenter import *

def _build_inventory_home(page: ft.Page) -> list:
    """Écran de l'inventaire - affiche les items possédés."""
    
    state = {
        "search_query": "",
        "active_type": None,
        "temp_type": None,
    }
    
    item_list_container = ft.Row(spacing=10, wrap=True, scroll="auto")
    type_buttons_container = ft.Row(
        spacing=10,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        expand=True,
    )
    
    def is_search_mode():
        return state["search_query"] != ""
    
    def filter_items():
        items = inventory_manager.get_items()
        search_query = state["search_query"].lower()
        active_type = state["active_type"]
        
        filtered = []
        for item in items:
            if is_search_mode():
                if search_query.startswith("#"):
                    tag = search_query[1:]
                    if "tags" in item and any(tag in t.lower() for t in item["tags"]):
                        filtered.append(item)
                else:
                    if search_query in item["name"].lower():
                        filtered.append(item)
            else:
                if active_type:
                    if "use" in item and item["use"] == active_type["name"]:
                        filtered.append(item)
                else:
                    filtered.append(item)
        
        return filtered
    
    def refresh_item_list():
        item_list_container.controls.clear()
        items = filter_items()
        
        if is_search_mode() and not items:
            item_list_container.controls.append(
                ft.Text("Aucun résultat trouvé", size=16, color="#f77c5dab")
            )
        elif not items:
            item_list_container.controls.append(
                ft.Text("Inventaire vide", size=16, color="#f77c5dab")
            )
        else:
            for item in items:
                item_list_container.controls.append(create_inventory_item_button(item))
        
        page.update()
    
    def create_inventory_item_button(item):
        def on_tap(e, i=item):
            open_item_modal(i)
        
        # Créer le container une fois
        item_container = ft.Container(
            content=ft.Stack([
                ft.Container(
                    content=ft.Image(
                        src=item["icon"] if "icon" in item else "",
                        width=80,
                        height=80,
                        fit="contain",
                        error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=40),
                    ),
                    padding=10,
                ),
                ft.Container(
                    content=ft.Text(str(item["amount"]), weight=ft.FontWeight.BOLD, size=12, color="white"),
                    bgcolor=ft.Colors.with_opacity(0.7, "black"),
                    border=ft.border.all(2, "#444444"),
                    border_radius=10,
                    padding=ft.padding.symmetric(horizontal=4, vertical=2),
                    right=-2,
                    bottom=-2,
                ),
            ], width=80, height=80),
            width=90,
            height=90,
            border_radius=10,
            border=ft.border.all(2, "#444444"),
            tooltip=item["name"],
            bgcolor="#2a2a2a",
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            on_click=on_tap,
        )

        def on_hover(e):
            item_container.bgcolor = "#3c3c3c" if e.data else "#2a2a2a"
            item_container.update()

        item_container.on_hover = on_hover
        return item_container
    
    def open_item_modal(item):
        # Créer la dialog d'abord
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(item["name"], weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Image(
                            src=item["icon"] if "icon" in item else "",
                            width=100,
                            height=100,
                            fit="contain",
                            error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=60),
                        ),
                        width=110,
                        height=110,
                        bgcolor="#2a2a2a",
                        border_radius=10,
                        padding=5,
                    ),
                    ft.Column([
                        ft.Text(f"Quantité : {item['amount']}", size=14),
                        ft.Text(f"Type : {item.get('use', 'inconnu')}", size=14),
                        ft.Text(f"Spécial : {'Oui' if item.get('is_special') else 'Non'}", size=14),
                    ], spacing=5),
                ], spacing=10),
                ft.Divider(),
                ft.Text(item.get("description", "Pas de description"), size=13, color="gray"),
            ], tight=True, width=300, spacing=10),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        def close_modal(e):
            dialog.open = False
            page.update()
        
        dialog.actions = [ft.TextButton("Fermer", on_click=close_modal)]
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    def on_search_focus(e):
        state["temp_type"] = state["active_type"]
        state["active_type"] = None
        refresh_item_list()
    
    def on_search_blur(e):
        state["active_type"] = state["temp_type"]
        refresh_item_list()
    
    def on_search_input(e):
        state["search_query"] = e.control.value
        refresh_item_list()
    
    def create_type_button(type_obj):
        button = ft.Container(
            content=ft.Column([
                ft.Image(
                    src=type_obj["icon"] if "icon" in type_obj else "",
                    width=50,
                    height=50,
                    fit="contain",
                    error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=40),
                ),
                ft.Text(type_obj["name"], size=11, text_align=ft.TextAlign.CENTER, color="white"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=80,
            height=85,
            border_radius=10,
            border=ft.border.all(2, "#555555"),
            padding=8,
            bgcolor="#2a2a2a",
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        def on_type_click(e):
            if state["active_type"] is not None:
                if state["active_type"] == type_obj:
                    state["active_type"] = None
                    button.border = ft.border.all(2, "#555555")
                    button.bgcolor = "#2a2a2a"
                else:
                    # modifier le précédent bouton actif pour le désactiver
                    for btn in type_buttons_container.controls:
                        if btn.content.controls[1].value == state["active_type"]["name"]:
                            state["active_type"] = type_obj
                            button.border = ft.border.all(2, "#4a9eff")
                            button.bgcolor = "#1a3a5c"
                            btn.border = ft.border.all(2, "#555555")
                            btn.bgcolor = "#2a2a2a"
                            btn.update()
                            break
            else:
                state["active_type"] = type_obj
                button.border = ft.border.all(2, "#4a9eff")
                button.bgcolor = "#1a3a5c"
            button.update()
            refresh_item_list()
        
        button.on_click = on_type_click
        return button
    
    for type_obj in TYPES:
        type_buttons_container.controls.append(create_type_button(type_obj))
    
    search_input = ft.TextField(
        hint_text="Rechercher... (ex: #food, bandage)",
        on_focus=on_search_focus,
        on_blur=on_search_blur,
        on_change=on_search_input,
        border_color="#555555",
        focused_border_color="#4a9eff",
    )
    
    refresh_item_list()
    
    return [ft.Column([
        ft.Container(
            content=ft.Text("Inventaire", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            alignment=ft.Alignment.CENTER,
            padding=ft.padding.symmetric(vertical=10),
        ),
        ft.Container(
            content=type_buttons_container,
            padding=ft.padding.symmetric(vertical=10),
        ),
        ft.Container(
            content=search_input,
            alignment=ft.Alignment.CENTER,
            padding=ft.padding.symmetric(horizontal=20),
        ),
        ft.Container(
            content=item_list_container,
            padding=ft.padding.all(10),
            expand=True,
        ),
    ], expand=True, spacing=5)]