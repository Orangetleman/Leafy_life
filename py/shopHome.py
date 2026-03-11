import flet as ft
from datacenter import inventory_manager, classic_shop_manager, WANDERINGSHOPS
from style import *


def open_error_modal(page: ft.Page, message: str):
    def close(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Erreur", color=SHOP_CARD_ALERT_TEXT_COLOR, weight=ft.FontWeight.BOLD),
        content=ft.Text(message, color=SHOP_CARD_ALERT_TEXT_COLOR),
        bgcolor=SHOP_CARD_ALERT_BG_COLOR,
        actions=[ft.TextButton("Fermer", on_click=close)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def open_buy_modal(page: ft.Page, item: dict, shop, on_confirm):
    stock_entry = next((i for i in shop.stock if i["id"] == item["id"]), None)
    max_amount  = stock_entry["amount"] if stock_entry else 0

    price_O2  = item.get("price_O2",  0) or 0
    price_CO2 = item.get("price_CO2", 0) or 0

    max_affordable_O2  = (inventory_manager.money["O2"]  // price_O2)  if price_O2  > 0 else float("inf")
    max_affordable_CO2 = (inventory_manager.money["CO2"] // price_CO2) if price_CO2 > 0 else float("inf")
    max_buyable = min(max_amount, max_affordable_O2, max_affordable_CO2)
    if max_buyable == float("inf"):
        max_buyable = max_amount

    state = {"amount": 1}

    amount_text    = ft.Text(str(state["amount"]), size=20, weight=ft.FontWeight.BOLD, color=SHOP_CARD_ITEM_AMOUNT_SELECTED_BADGE_TEXT_COLOR)
    price_o2_text  = ft.Text(f"{price_O2} O2",   size=14, color=SHOP_CARD_ITEM_PRICE_O2_TEXT_COLOR) if price_O2  > 0 else None
    price_co2_text = ft.Text(f"{price_CO2} CO2", size=14, color=SHOP_CARD_ITEM_PRICE_CO2_TEXT_COLOR) if price_CO2 > 0 else None

    effect = item.get("effect", {})
    effect_label = f"+{effect.get('amount','?')} {effect.get('stat','?')}" if effect else "—"

    def refresh_prices():
        if price_o2_text:  price_o2_text.value  = f"{price_O2  * state['amount']} O2"
        if price_co2_text: price_co2_text.value = f"{price_CO2 * state['amount']} CO2"
        amount_text.value = str(state["amount"])
        page.update()

    def remove(e):
        if state["amount"] > 1:
            state["amount"] -= 1
            refresh_prices()

    def add(e):
        if state["amount"] < max_buyable:
            state["amount"] += 1
            refresh_prices()

    def confirm(e):
        dialog.open = False
        page.update()
        on_confirm(item, state["amount"])

    def cancel(e):
        dialog.open = False
        page.update()

    price_row = ft.Row([
        ft.Container(price_o2_text,  bgcolor=SHOP_CARD_ITEM_PRICE_O2_BG_COLOR, border_radius=6,
                    padding=ft.padding.symmetric(horizontal=8, vertical=4)) if price_o2_text  else ft.Container(),
        ft.Container(price_co2_text, bgcolor=SHOP_CARD_ITEM_PRICE_CO2_BG_COLOR, border_radius=6,
                    padding=ft.padding.symmetric(horizontal=8, vertical=4)) if price_co2_text else ft.Container(),
    ], spacing=8)
    remove_badge = ft.Container(content=ft.Text("-",weight=ft.FontWeight.BOLD, color=SHOP_CARD_ITEM_AMOUNT_SELECTOR_REMOVE_TEXT_COLOR), bgcolor=SHOP_CARD_ITEM_AMOUNT_SELECTOR_REMOVE_BG_COLOR,
                        on_click=remove,
                        border=ft.border.all(SHOP_CARD_ITEM_AMOUNT_SELECTOR_REMOVE_BORDER_COLOR[0], SHOP_CARD_ITEM_AMOUNT_SELECTOR_REMOVE_BORDER_COLOR[1]), 
                        border_radius=8,
                        padding=ft.padding.symmetric(horizontal=10, vertical=8),
                        alignment=ft.Alignment(0,0))

    add_badge = ft.Container(content=ft.Text("+",weight=ft.FontWeight.BOLD, color=SHOP_CARD_ITEM_AMOUNT_SELECTOR_ADD_TEXT_COLOR), bgcolor=SHOP_CARD_ITEM_AMOUNT_SELECTOR_ADD_BG_COLOR,
                        on_click=add,
                        border=ft.border.all(SHOP_CARD_ITEM_AMOUNT_SELECTOR_ADD_BORDER_COLOR[0], SHOP_CARD_ITEM_AMOUNT_SELECTOR_ADD_BORDER_COLOR[1]), 
                        border_radius=8,
                        padding=ft.padding.symmetric(horizontal=10, vertical=8),
                        alignment=ft.Alignment(0,0))
    
    def remove_hover(e):
        remove_badge.bgcolor = SHOP_CARD_ITEM_AMOUNT_SELECTOR_REMOVE_BG_HOVER_COLOR if e.data else SHOP_CARD_ITEM_AMOUNT_SELECTOR_REMOVE_BG_COLOR
        remove_badge.update()

    def add_hover(e):
        add_badge.bgcolor = SHOP_CARD_ITEM_AMOUNT_SELECTOR_ADD_BG_HOVER_COLOR if e.data else SHOP_CARD_ITEM_AMOUNT_SELECTOR_ADD_BG_COLOR
        add_badge.update()

    remove_badge.on_hover = remove_hover
    add_badge.on_hover = add_hover
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmer l'achat", weight=ft.FontWeight.BOLD, color=SHOP_CARD_TITLE_TEXT_COLOR),
        bgcolor=SHOP_BUTTON_BG_COLOR,
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Image(src=item.get("icon", ""), width=50, height=50, fit="contain",
                                    error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=30, color="white")),
                    bgcolor="#2a2a3e", border_radius=8, padding=8,
                ),
                ft.Column([
                    ft.Text(item["name"], size=16, weight=ft.FontWeight.BOLD, color=SHOP_CARD_ITEM_NAME_COLOR),
                    ft.Text(f"Effet : {effect_label}", size=13, color=SHOP_CARD_ITEM_EFFECT_COLOR),
                    ft.Text(f"En stock : {max_amount}", size=13, color=SHOP_CARD_ITEM_STOCK_COLOR),
                ], spacing=4),
            ], spacing=12),
            ft.Divider(color="#444"),
            ft.Text("Quantité :", size=14, color=SHOP_CARD_ITEM_AMOUNT_SELECTED_TEXT_COLOR),
            ft.Row([
                remove_badge,
                ft.Container(content=amount_text, bgcolor=SHOP_CARD_ITEM_AMOUNT_SELECTED_BADGE_BG_COLOR,
                            border=ft.border.all(SHOP_CARD_ITEM_AMOUNT_SELECTED_BADGE_BORDER[0], SHOP_CARD_ITEM_AMOUNT_SELECTED_BADGE_BORDER[1]), border_radius=8,
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            alignment=ft.Alignment(0,0)),
                add_badge,
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            price_row,
        ], tight=True, spacing=12, width=280),
        actions=[
            ft.TextButton("Annuler", on_click=cancel, style=ft.ButtonStyle(color="gray")),
            ft.ElevatedButton("Acheter", on_click=confirm, bgcolor=SHOP_CARD_CONFIRM_BUTTON_BG_COLOR, color=SHOP_CARD_CONFIRM_BUTTON_TEXT_COLOR),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def _build_shop_home(page: ft.Page, shop_type: str = "classic", biome: str = "plain") -> list:
    if shop_type == "classic":
        shop = classic_shop_manager
    else:
        entry = next((s for s in WANDERINGSHOPS if s["biome"] == biome), None)
        shop  = entry["shop"] if entry else classic_shop_manager
        shop.reload_wandering_shop_items()

    state = {"search_query": ""}

    o2_badge = ft.Container(
        content=ft.Text(f"{inventory_manager.money['O2']} O2",  size=13, color=SHOP_BUTTON_BADGE_TXT_COLOR),
        bgcolor=SHOP_BUTTON_BADGE_BG_O2_COLOR, border=ft.border.all(1, SHOP_BUTTON_BADGE_BORDER_O2_COLOR),
        border_radius=6, padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )
    co2_badge = ft.Container(
        content=ft.Text(f"{inventory_manager.money['CO2']} CO2", size=13, color=SHOP_BUTTON_BADGE_TXT_COLOR),
        bgcolor=SHOP_BUTTON_BADGE_BG_CO2_COLOR, border=ft.border.all(1, SHOP_BUTTON_BADGE_BORDER_CO2_COLOR),
        border_radius=6, padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )

    def refresh_badges():
        o2_badge.content.value  = f"{inventory_manager.money['O2']} O2"
        co2_badge.content.value = f"{inventory_manager.money['CO2']} CO2"
        o2_badge.update()
        co2_badge.update()

    shop_list = ft.Column(scroll="auto", spacing=8, expand=True)

    def filter_items():
        query  = state["search_query"].lower()
        is_tag = query.startswith("#")
        tag    = query[1:] if is_tag else query
        result = []
        for item in shop.stock:
            if is_tag:
                if any(tag in t.lower() for t in item.get("tags", [])):
                    result.append(item)
            else:
                if tag in item["name"].lower():
                    result.append(item)
        return result

    def refresh_list():
        shop_list.controls.clear()
        items = filter_items()
        if not items:
            shop_list.controls.append(ft.Text("Aucun article trouvé.", color="gray", size=14))
        else:
            for item in items:
                shop_list.controls.append(create_item_row(item))
        page.update()

    def create_item_row(item):
        stock_entry = next((i for i in shop.stock if i["id"] == item["id"]), None)
        stock_qty   = stock_entry["amount"] if stock_entry else 0

        effect = item.get("effect", {})
        effect_text = f"+{effect.get('amount','?')} {effect.get('stat','?')}" if effect else ""

        price_badges = []
        if item.get("price_O2",  0):
            price_badges.append(ft.Container(
                ft.Text(f"{item['price_O2']} O2",  size=12, color=SHOP_BUTTON_BADGE_TXT_COLOR),
                bgcolor=SHOP_BUTTON_BADGE_BG_O2_COLOR, border=ft.border.all(1, SHOP_BUTTON_BADGE_BORDER_O2_COLOR),
                border_radius=6, padding=ft.padding.symmetric(horizontal=6, vertical=3),
            ))
        if item.get("price_CO2", 0):
            price_badges.append(ft.Container(
                ft.Text(f"{item['price_CO2']} CO2", size=12, color=SHOP_BUTTON_BADGE_TXT_COLOR),
                bgcolor=SHOP_BUTTON_BADGE_BG_CO2_COLOR, border=ft.border.all(1, SHOP_BUTTON_BADGE_BORDER_CO2_COLOR),
                border_radius=6, padding=ft.padding.symmetric(horizontal=6, vertical=3),
            ))
        if stock_qty != float("inf") and stock_qty < 9999:
            price_badges.append(ft.Container(
                ft.Text(f"Stock: {stock_qty}", size=12, color=SHOP_BUTTON_BADGE_TXT_COLOR),
                bgcolor=SHOP_BUTTON_BADGE_BG_STOCK_COLOR, border=ft.border.all(1, SHOP_BUTTON_BADGE_BORDER_STOCK_COLOR),
                border_radius=6, padding=ft.padding.symmetric(horizontal=6, vertical=3),
            ))

        row_container = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        ft.Image(src=item.get("icon", ""), width=40, height=40, fit="contain",
                                error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=24, color=SHOP_BUTTON_IMG_ERROR_TXT_COLOR)),
                        bgcolor=SHOP_BUTTON_IMG_BG_COLOR, 
                        border_radius=8, border=ft.border.all(1, SHOP_BUTTON_IMG_BORDER_COLOR),
                        padding=5,
                    ),
                    ft.Column([
                        ft.Text(item["name"], size=14, color=SHOP_BUTTON_NAME_COLOR, weight=ft.FontWeight.W_500),
                        ft.Text(effect_text,  size=11, color=SHOP_BUTTON_EFFECT_COLOR),
                    ], spacing=2),
                ], spacing=10),
                ft.Row(price_badges, spacing=6),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            border_radius=10,
            border=ft.border.all(2, SHOP_BUTTON_BORDER_COLOR),
            bgcolor=SHOP_BUTTON_BG_COLOR,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        )

        def on_hover(e):
            row_container.bgcolor = SHOP_BUTTON_BG_COLOR_HOVER if e.data else SHOP_BUTTON_BG_COLOR
            row_container.update()

        def on_click(e, i=item):
            row_container.bgcolor = SHOP_BUTTON_BG_COLOR_CLICKED if e.data else SHOP_BUTTON_BG_COLOR
            row_container.update()
            open_buy_modal(page, i, shop, on_purchase)

        row_container.on_hover = on_hover
        row_container.on_click = on_click
        return row_container

    def on_purchase(item, amount):
        result = shop.buy_item(item, amount)
        if result["success"]:
            refresh_badges()
            refresh_list()
        else:
            messages = {
                "insufficient_funds": f"Fonds insuffisants pour acheter {item['name']}.",
                "out_of_stock":       f"{item['name']} n'est pas en stock.",
                "payment_failed":     "Erreur lors du paiement. Veuillez réessayer.",
            }
            open_error_modal(page, messages.get(result["error"], "Erreur inconnue."))

    def on_search_change(e):
        state["search_query"] = e.control.value
        refresh_list()

    refresh_list()

    return [ft.Container(
                    ft.Column([
                            ft.Container(
                                content=ft.Row([
                                    ft.TextField(
                                        label="🔍 Rechercher… (ex: #soin, bandage)",
                                        on_change=on_search_change,
                                        expand=True,
                                        border_color=SHOP_SHEARCHBAR_BORDER_COLOR, 
                                        color=SHOP_SHEARCHBAR_INPUT_COLOR, 
                                        hint_style=ft.TextStyle(color=SHOP_SHEARCHBAR_LABEL_COLOR),
                                        bgcolor=SHOP_SHEARCHBAR_BG_COLOR,
                                        focused_bgcolor=SHOP_SHEARCHBAR_COLOR_FOCUSED,
                                        focused_border_color=SHOP_SHEARCHBAR_BORDER_COLOR_FOCUSED,
                                    ),
                                    ft.Row([o2_badge, co2_badge], spacing=6),
                                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                            ),
                            ft.Container(
                                content=ft.Text("Shop itinérant" if shop_type == "wandering" else "Shop",
                                                size=20, weight=ft.FontWeight.BOLD,
                                                text_align=ft.TextAlign.CENTER, color=SHOP_TITLE_COLOR),
                                alignment=ft.Alignment.CENTER,
                                bgcolor=SHOP_TITLE_BG_COLOR, border=ft.border.all(2, SHOP_TITLE_BORDER_COLOR),
                                border_radius=8, padding=ft.padding.symmetric(vertical=8),
                                margin=ft.margin.symmetric(horizontal=12),
                            ),
                            ft.Container(content=shop_list, expand=True,
                                        padding=ft.padding.symmetric(horizontal=12, vertical=4)),
                        ], expand=True, spacing=0),
                    expand=True, bgcolor=SHOP_BG_COLOR, padding=0,
                    )]