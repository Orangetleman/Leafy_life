from datacenter import *
from style import *
import flet as ft

def _build_inventory_home(page: ft.Page) -> list:
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
        items       = inventory_manager.get_items()
        query       = state["search_query"].lower()
        active_type = state["active_type"]

        filtered = []
        for item in items:
            if is_search_mode():
                if query.startswith("#"):
                    tag = query[1:]
                    if any(tag in t.lower() for t in item.get("tags", [])):
                        filtered.append(item)
                else:
                    if query in item["name"].lower():
                        filtered.append(item)
            else:
                if active_type:
                    if item.get("category") == active_type["name"]:
                        filtered.append(item)
                else:
                    filtered.append(item)
        return filtered

    def refresh_item_list():
        item_list_container.controls.clear()
        items = filter_items()

        if not items:
            item_list_container.controls.append(
                ft.Text("Aucun résultat trouvé", size=16, color=INVENTORY_NO_RESULT_TEXT_COLOR)
            )
        else:
            for item in items:
                item_list_container.controls.append(create_inventory_item_button(item))
        page.update()

    def create_inventory_item_button(item):
        def on_tap(e, i=item):
            open_item_modal(i)

        item_container = ft.Container(
            content=ft.Stack([
                ft.Container(
                    content=ft.Image(
                        src=item.get("icon", ""),
                        width=80, height=80, fit="contain",
                        error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=40),
                    ),
                    padding=10,
                ),
                ft.Container(
                    content=ft.Text(str(item["amount"]), weight=ft.FontWeight.BOLD, size=12, color=INVENTORY_BUTTON_AMOUNT_BADGE_TEXT_COLOR),
                    bgcolor=ft.Colors.with_opacity(INVENTORY_BUTTON_AMOUNT_BADGE_BG_COLOR[0], INVENTORY_BUTTON_AMOUNT_BADGE_BG_COLOR[1]),
                    border=ft.border.all(2, INVENTORY_BUTTON_AMOUNT_BADGE_BORDER_COLOR),
                    border_radius=10,
                    padding=ft.padding.symmetric(horizontal=4, vertical=2),
                    right=-2, bottom=-2,
                ),
            ], width=80, height=80),
            width=90, height=90,
            border_radius=10,
            border=ft.border.all(2, INVENTORY_BUTTON_BORDER_COLOR),
            tooltip=item["name"],
            bgcolor=INVENTORY_BUTTON_BG_COLOR,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            on_click=on_tap,
        )

        def on_hover(e):
            item_container.bgcolor = INVENTORY_BUTTON_BG_COLOR_HOVER if e.data else INVENTORY_BUTTON_BG_COLOR
            item_container.update()

        item_container.on_hover = on_hover
        return item_container

    def open_item_modal(item):
        def close_modal(e):
            dialog.open = False
            page.update()

        effect = item.get("effect", {})
        effect_text = f"+{effect.get('amount', '?')} {effect.get('stat', '?')}" if effect else "—"

        dialog = ft.AlertDialog(
            modal=False,
            on_dismiss=lambda e: close_modal(e),
            title=ft.Text(item["name"], weight=ft.FontWeight.BOLD, color=INVENTORY_CARD_TITLE_TEXT_COLOR),
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Image(
                            src=item.get("icon", ""),
                            width=100, height=100, fit="contain",
                            error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=60),
                        ),
                        width=110, height=110,
                        bgcolor=INVENTORY_CARD_BG_COLOR, border_radius=10, padding=5,
                    ),
                    ft.Column([
                        ft.Text(f"Quantité : {item['amount']}", size=14, color=INVENTORY_CARD_INFO_TEXT_COLOR),
                        ft.Text(f"Catégorie : {item.get('category', '?')}", size=14, color=INVENTORY_CARD_INFO_TEXT_COLOR),
                        ft.Text(f"Effet : {effect_text}", size=14, color=INVENTORY_CARD_INFO_TEXT_COLOR),
                        ft.Text(f"Spécial : {'Oui' if item.get('is_special') else 'Non'}", size=14, color=INVENTORY_CARD_INFO_TEXT_COLOR),
                    ], spacing=5),
                ], spacing=10),
                ft.Divider(),
                ft.Text(item.get("description", "Pas de description"), size=13, color=INVENTORY_CARD_INFO_TEXT_COLOR),
            ], tight=True, width=300, spacing=10),
            actions=[ft.TextButton("Fermer", on_click=close_modal)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
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
                    src=type_obj.get("icon", ""),
                    width=50, height=50, fit="contain",
                    error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=40),
                ),
                ft.Text(type_obj["name"], size=11, text_align=ft.TextAlign.CENTER, color=INVENTORY_TYPE_TEXT_COLOR),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=80, height=85,
            border_radius=10,
            border=ft.border.all(2, INVENTORY_TYPE_BORDER_COLOR),
            padding=8,
            bgcolor=INVENTORY_TYPE_BG_COLOR,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        )

        def on_type_click(e):
            if state["active_type"] == type_obj:
                state["active_type"] = None
                button.border = ft.border.all(2, INVENTORY_TYPE_BORDER_COLOR)
                button.bgcolor = INVENTORY_TYPE_BG_COLOR
            else:
                for btn in type_buttons_container.controls:
                    btn.border  = ft.border.all(2, INVENTORY_TYPE_BORDER_COLOR)
                    btn.bgcolor = INVENTORY_TYPE_BG_COLOR
                    btn.update()
                state["active_type"] = type_obj
                button.border  = ft.border.all(2, INVENTORY_TYPE_BORDER_COLOR_ACTIVE)
                button.bgcolor = INVENTORY_TYPE_BG_COLOR_ACTIVE
            button.update()
            refresh_item_list()

        button.on_click = on_type_click
        return button

    for type_obj in TYPES:
        type_buttons_container.controls.append(create_type_button(type_obj))

    search_input = ft.TextField(
        label="🔍 Rechercher… (ex: #soin, bandage)",
        on_focus=on_search_focus,
        on_blur=on_search_blur,
        on_change=on_search_input,
        color=INVENTORY_SHEARCHBAR_INPUT_COLOR,
        hint_style=ft.TextStyle(color=INVENTORY_SHEARCHBAR_LABEL_COLOR),
        border_color=INVENTORY_SHEARCHBAR_BORDER_COLOR,
        bgcolor=INVENTORY_SHEARCHBAR_BG_COLOR,
        focused_border_color=INVENTORY_SHEARCHBAR_BORDER_COLOR_FOCUSED,
        focused_bgcolor=INVENTORY_SHEARCHBAR_BG_COLOR_FOCUSED,
    )

    refresh_item_list()

    return [ft.Container(ft.Column([
        ft.Container(
            content=ft.Container(
                content=ft.Text("Inventaire", size=24, weight=ft.FontWeight.BOLD, color=INVENTORY_TITLE_COLOR),
                padding=10,
                bgcolor=INVENTORY_TITLE_BG_COLOR,
                border=ft.border.all(INVENTORY_TITLE_BORDER_COLOR[0], INVENTORY_TITLE_BORDER_COLOR[1]),
                border_radius=10,
            ),
            alignment=ft.Alignment(0, 0),
        ),
        ft.Container(content=type_buttons_container, padding=ft.padding.symmetric(vertical=10)),
        ft.Container(content=search_input, padding=ft.padding.symmetric(horizontal=20)),
        ft.Container(content=item_list_container, padding=ft.padding.all(10), expand=True, alignment=ft.Alignment(-1, -1)),
    ], expand=True, spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER, margin=ft.margin.symmetric(vertical=10)), bgcolor=INVENTORY_BG_COLOR, expand=True)]