import flet as ft
from datacenter import (
    inventory_manager,
    classic_shop_manager,
    WANDERINGSHOPS,
)


# ──────────────────────────────────────────────────────────────
#  Modale d'erreur (équivalent openErrorModal)
# ──────────────────────────────────────────────────────────────
def open_error_modal(page: ft.Page, message: str):
    def close(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Erreur", color="white", weight=ft.FontWeight.BOLD),
        content=ft.Text(message, color="white"),
        bgcolor="#cc3333",
        actions=[ft.TextButton("Fermer", on_click=close)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


# ──────────────────────────────────────────────────────────────
#  Modale d'achat (équivalent openBuyModal)
# ──────────────────────────────────────────────────────────────
def open_buy_modal(page: ft.Page, item: dict, shop, on_confirm):
    stock_entry = next((i for i in shop.stock if i["id"] == item["id"]), None)
    max_amount = stock_entry["amount"] if stock_entry else 0

    price_O2  = item.get("price_O2",  0) or 0
    price_CO2 = item.get("price_CO2", 0) or 0

    max_affordable_O2  = (inventory_manager.money["O2"]  // price_O2)  if price_O2  > 0 else float("inf")
    max_affordable_CO2 = (inventory_manager.money["CO2"] // price_CO2) if price_CO2 > 0 else float("inf")
    max_buyable = min(max_amount, max_affordable_O2, max_affordable_CO2)
    if max_buyable == float("inf"):
        max_buyable = max_amount

    state = {
        "amount": 1
        }

    # --- widgets dynamiques ---
    amount_text = ft.Text(
        str(state["amount"]),
        size=20,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    price_o2_text  = ft.Text(f"{price_O2}  O2",  size=14, color="#4da6ff") if price_O2  > 0 else None
    price_co2_text = ft.Text(f"{price_CO2} CO2", size=14, color="#6ecf7a") if price_CO2 > 0 else None

    def refresh_prices():
        if price_o2_text:
            price_o2_text.value  = f"{price_O2  * state['amount']} O2"
        if price_co2_text:
            price_co2_text.value = f"{price_CO2 * state['amount']} CO2"
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

    price_row_controls = []
    if price_o2_text:
        price_row_controls.append(
            ft.Container(price_o2_text,  bgcolor="#1a3a5c", border_radius=6, padding=ft.padding.symmetric(horizontal=8, vertical=4))
        )
    if price_co2_text:
        price_row_controls.append(
            ft.Container(price_co2_text, bgcolor="#1a3a5c", border_radius=6, padding=ft.padding.symmetric(horizontal=8, vertical=4))
        )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmer l'achat", weight=ft.FontWeight.BOLD, color="white"),
        bgcolor="#1e1e2e",
        content=ft.Column([
            # Icône + infos item
            ft.Row([
                ft.Container(
                    content=ft.Image(src=item.get("icon", ""), width=50, height=50, fit="contain",
                                    error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=30, color="white")),
                    bgcolor="#2a2a3e", border_radius=8, padding=8,
                ),
                ft.Column([
                    ft.Text(item["name"], size=16, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text(f"En stock : {max_amount}", size=13, color="gray"),
                ], spacing=4),
            ], spacing=12),

            ft.Divider(color="#444"),

            # Sélection de quantité
            ft.Text("Quantité :", size=14, color="white"),
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.REMOVE,
                    icon_color="white",
                    bgcolor="#c0392b",
                    on_click=remove,
                    style=ft.ButtonStyle(shape=ft.CircleBorder()),
                ),
                ft.Container(
                    content=amount_text,
                    bgcolor="#2a2a3e",
                    border=ft.border.all(1, "#555"),
                    border_radius=8,
                    padding=ft.padding.symmetric(horizontal=16, vertical=6),
                ),
                ft.IconButton(
                    icon=ft.Icons.ADD,
                    icon_color="white",
                    bgcolor="#27ae60",
                    on_click=add,
                    style=ft.ButtonStyle(shape=ft.CircleBorder()),
                ),
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),

            # Prix
            ft.Row(price_row_controls, spacing=8) if price_row_controls else ft.Text("Gratuit", color="gray"),
        ], tight=True, spacing=12, width=280),
        actions=[
            ft.TextButton("Annuler", on_click=cancel, style=ft.ButtonStyle(color="gray")),
            ft.ElevatedButton("Acheter", on_click=confirm,
                            bgcolor="#27ae60", color="white"),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


# ──────────────────────────────────────────────────────────────
#  Écran principal du shop
# ──────────────────────────────────────────────────────────────
def _build_shop_home(page: ft.Page, shop_type: str = "classic", biome: str = "plain") -> list:

    # Choisir le bon shop
    if shop_type == "classic":
        shop = classic_shop_manager
    else:
        entry = next((s for s in WANDERINGSHOPS if s["biome"] == biome), None)
        shop  = entry["shop"] if entry else classic_shop_manager
        shop.reload_wandering_shop_items()

    state = {"search_query": ""}

    # --- affichage monnaies ---
    o2_badge  = ft.Container(
        content=ft.Text(f"{inventory_manager.money['O2']} O2",  size=13, color="white"),
        bgcolor="#1a3a7c", border=ft.border.all(1, "#006bb3"),
        border_radius=6, padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )
    co2_badge = ft.Container(
        content=ft.Text(f"{inventory_manager.money['CO2']} CO2", size=13, color="white"),
        bgcolor="#1a4a2a", border=ft.Border.all(1, "#2e8b39"),
        border_radius=6, padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )

    def refresh_badges():
        o2_badge.content.value  = f"{inventory_manager.money['O2']} O2"
        co2_badge.content.value = f"{inventory_manager.money['CO2']} CO2"
        o2_badge.update()
        co2_badge.update()

    # --- liste des items ---
    shop_list = ft.Column(scroll="auto", spacing=8, expand=True)

    def filter_items():
        query = state["search_query"].lower()
        is_tag = query.startswith("#")
        tag    = query[1:] if is_tag else query

        result = []
        for item in shop.stock:
            if is_tag:
                tags = item.get("tags", [])
                if any(tag in t.lower() for t in tags):
                    result.append(item)
            else:
                if tag in item["name"].lower():
                    result.append(item)
        return result

    def refresh_list():
        shop_list.controls.clear()
        items = filter_items()

        if not items:
            shop_list.controls.append(
                ft.Text("Aucun article trouvé.", color="#f77c5dab", size=14)
            )
        else:
            for item in items:
                shop_list.controls.append(create_item_row(item))

        page.update()

    def create_item_row(item):
        stock_entry = next((i for i in shop.stock if i["id"] == item["id"]), None)
        stock_qty   = stock_entry["amount"] if stock_entry else 0

        # badges de prix
        price_badges = []
        if item.get("price_O2",  0):
            price_badges.append(ft.Container(
                ft.Text(f"{item['price_O2']} O2",  size=12, color="white"),
                bgcolor="#1a3a7c", border=ft.Border.all(1, "#006bb3"),
                border_radius=6, padding=ft.padding.symmetric(horizontal=6, vertical=3),
            ))
        if item.get("price_CO2", 0):
            price_badges.append(ft.Container(
                ft.Text(f"{item['price_CO2']} CO2", size=12, color="white"),
                bgcolor="#1a4a2a", border=ft.Border.all(1, "#2e8b39"),
                border_radius=6, padding=ft.padding.symmetric(horizontal=6, vertical=3),
            ))
        if stock_qty != float("inf") and stock_qty < 99999:
            price_badges.append(ft.Container(
                ft.Text(f"Stock: {stock_qty}", size=12, color="white"),
                bgcolor="#7a6a00", border=ft.Border.all(1, "#bfa500"),
                border_radius=6, padding=ft.padding.symmetric(horizontal=6, vertical=3),
            ))

        row_container = ft.Container(
            content=ft.Row([
                # Gauche : icône + nom
                ft.Row([
                    ft.Container(
                        ft.Image(src=item.get("icon", ""), width=40, height=40, fit="contain",
                                error_content=ft.Icon(ft.Icons.HELP_OUTLINE, size=24, color="white")),
                        bgcolor="#2a2a3e", border_radius=8, padding=5,
                    ),
                    ft.Text(item["name"], size=14, color="white", weight=ft.FontWeight.W_500),
                ], spacing=10),
                # Droite : prix
                ft.Row(price_badges, spacing=6),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            border_radius=10,
            border=ft.Border.all(1, "#444"),
            bgcolor="#2a2a3e",
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        )

        def on_hover(e):
            row_container.bgcolor = "#3a3a5e" if e.data else "#2a2a3e"
            row_container.update()

        def on_click(e, i=item):
            open_buy_modal(page, i, shop, on_purchase)

        row_container.on_hover  = on_hover
        row_container.on_click  = on_click
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

    # Remplissage initial
    refresh_list()

    shop_title = "Shop itinérant" if shop_type == "wandering" else "Shop"

    return [ft.Column([
        # Header : recherche + monnaies
        ft.Container(
            content=ft.Row([
                ft.TextField(
                    label="🔍 Rechercher… (ex: #food, bandage)",
                    on_change=on_search_change,
                    expand=True,
                    border_color="#555",
                    focused_border_color="#4a9eff",
                    color="white",
                    hint_style=ft.TextStyle(color="#888"),
                ),
                ft.Row([o2_badge, co2_badge], spacing=6),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
        ),

        # Titre
        ft.Container(
            content=ft.Text(shop_title, size=20, weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER, color="white"),
            alignment=ft.Alignment.CENTER,
            bgcolor="#7a3a7a",
            border=ft.Border.all(2, "#5a1a5a"),
            border_radius=8,
            padding=ft.padding.symmetric(vertical=8),
            margin=ft.Margin.symmetric(horizontal=12),
        ),

        # Liste scrollable
        ft.Container(
            content=shop_list,
            expand=True,
            padding=ft.padding.symmetric(horizontal=12, vertical=4),
        ),
    ], expand=True, spacing=0)]