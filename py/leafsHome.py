from datacenter import *
from style import *
import flet as ft

# ──────────────────────────────────────────────────────────────
#  Config d'affichage par label
#  (label → stat_attr, max_value, couleur_barre)
# ──────────────────────────────────────────────────────────────
STAT_DISPLAY = {
    "Points de Vie": ("hp",        10,  LEAF_CARD_PROGRESS_BAR_HP_COLOR),
    "Nourriture":    ("nutrients", 100, LEAF_CARD_PROGRESS_BAR_NUTRIENTS_COLOR),
    "Hydratation":   ("hydration", 100, LEAF_CARD_PROGRESS_BAR_HYDRATION_COLOR),
    "Attaque":       ("atk",       10,  LEAF_CARD_PROGRESS_BAR_ATK_COLOR),
    "Level":         ("level",     100, LEAF_CARD_PROGRESS_BAR_LVL_COLOR),
}

# ──────────────────────────────────────────────────────────────
#  Sélection de l'item à afficher sur le badge selon le leaf
#  et la stat concernée — on se base sur effect["stat"]
# ──────────────────────────────────────────────────────────────
def item_for_stat(leaf, stat_attr):
    """
    Retourne l'item de l'inventaire (ou du catalogue) le plus
    adapté pour agir sur `stat_attr` pour ce leaf.
    Priorité : item possédé > item catalogue.
    """
    species = leaf.species
    regime  = getattr(leaf, "regime", None)
    hp      = getattr(leaf, "hp", 1)

    # Candidats selon la stat
    if stat_attr == "nutrients":
        if species == "plant":
            candidates = [ITEMS[2], ITEMS[9]]          # Fertilisant, Poudre d'os
        elif regime == "carnivore":
            candidates = [ITEMS[3], ITEMS[8]]          # Viande, Lait
        else:
            candidates = [ITEMS[4], ITEMS[8]]          # Herbe, Lait

    elif stat_attr == "hydration":
        candidates = [ITEMS[1]]                        # Eau minérale

    elif stat_attr == "hp":
        if hp == 0:
            candidates = [ITEMS[7], ITEMS[10]]         # Rayon de soleil, Elixir
        elif species == "plant":
            candidates = [ITEMS[5]]                    # Sève
        else:
            candidates = [ITEMS[6], ITEMS[12]]         # Bandage, Potion de vie

    elif stat_attr == "atk":
        candidates = [ITEMS[11]]                       # Potion d'attaque

    elif stat_attr == "level":
        candidates = [ITEMS[13]]                       # Livre de la connaissance

    else:
        return None

    # Préférer un item que le joueur possède déjà
    owned_ids = {i["id"] for i in inventory_manager.get_items()}
    for item in candidates:
        if item["id"] in owned_ids:
            return item
    return candidates[0] if candidates else None


# ──────────────────────────────────────────────────────────────
#  Badge cliquable
# ──────────────────────────────────────────────────────────────
def create_badge_button(leaf, item, on_used=None):
    item_name = item["name"] if item and not item["name"].endswith(" 🌟") else item["name"][:len(item["name"]) - 2]
    if item is None:
        return ft.Container(width=32, height=32)

    def on_click(e):
        # Vérifier que le joueur possède l'item
        owned = next((i for i in inventory_manager.get_items() if i["id"] == item["id"]), None)
        if not owned or owned["amount"] < 1:
            print(f"Pas de {item_name} en inventaire.")
            return
        # Appliquer l'effet
        stat   = item["effect"]["stat"]
        amount = item["effect"]["amount"]
        leaf.stat_update(stat, amount)
        # Consommer l'item
        inventory_manager.remove_item(item["id"], 1)
        print(f"{item_name} utilisé sur {leaf.name} (+{amount} {stat})")
        if on_used:
            on_used()

    return ft.Container(
        content=ft.Image(src=item["icon"], width=18, height=18, fit="contain"),
        padding=5,
        bgcolor="#2a2a3e",
        border=ft.border.all(1, "#555"),
        border_radius=8,
        width=32,
        height=32,
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        tooltip=f"Utiliser : {item['name']}  (+{item['effect']['amount']} {item['effect']['stat']})",
    )


# ──────────────────────────────────────────────────────────────
#  Barre de progression + badge
# ──────────────────────────────────────────────────────────────
def create_progress_bar(leaf, label, on_used=None):
    stat_attr, _, color = STAT_DISPLAY[label]
    max_value = leaf.STAT_MAX.get(stat_attr, 100)
    value = getattr(leaf, stat_attr, 0)

    # Couleurs d'alerte
    if label == "Nourriture"  and value <= 20: color = LEAF_CARD_PROGRESS_BAR_NUTRIENTS_ALERT_COLOR
    if label == "Hydratation" and value <= 20: color = LEAF_CARD_PROGRESS_BAR_HYDRATION_ALERT_COLOR

    ratio = value / max_value if max_value > 0 else 0
    item  = item_for_stat(leaf, stat_attr)

    return ft.Column([
        ft.Row([
            ft.Text(label, weight=ft.FontWeight.W_500, size=14),
            ft.Text(f"{value}/{max_value}", size=12, color=LEAF_CARD_INFO_TEXT_COLOR),
        ]),
        ft.Row([
            ft.ProgressBar(
                value=ratio,
                color=color,
                bgcolor=LEAF_CARD_PROGRESS_BAR_BG_COLOR,
                width=260,
                bar_height=20,
                border_radius=8,
            ),
            create_badge_button(leaf, item, on_used=on_used),
        ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ], spacing=4)


# ──────────────────────────────────────────────────────────────
#  Modal leaf
# ──────────────────────────────────────────────────────────────
def open_leaf_modal(page: ft.Page, leaf):
    def close_modal(e):
        dialog.open = False
        page.update()

    def on_stat_used():
        # Reconstruire le contenu pour rafraîchir les barres
        dialog.content = build_content()
        page.update()

    def build_content():
        biome_name     = BIOMES[leaf.biome - 1]["name"]
        leaf_type_name = LEAFS_TYPE[leaf.type]["name"]
        return ft.Column(
            [
                ft.Row([
                    ft.Image(src=leaf.img, width=110, height=110, fit="contain"),
                    ft.Column([
                        ft.Row([ft.Text("Biome :",  size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_TITLE_TEXT_COLOR), ft.Text(biome_name,     size=13, color=LEAF_CARD_INFO_TEXT_COLOR)]),
                        ft.Row([ft.Text("Type :",   size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_TITLE_TEXT_COLOR), ft.Text(leaf_type_name, size=13, color=LEAF_CARD_INFO_TEXT_COLOR)]),
                        ft.Row([ft.Text("Rareté :", size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_TITLE_TEXT_COLOR), ft.Text(leaf.rarity,    size=13, color=LEAF_CARD_INFO_TEXT_COLOR)]),
                        ft.Row([ft.Text("Espèce :", size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_TITLE_TEXT_COLOR), ft.Text(leaf.species,   size=13, color=LEAF_CARD_INFO_TEXT_COLOR)]),
                    ], spacing=4),
                ], spacing=12),
                ft.Divider(),
                ft.Text("Statistiques", weight=ft.FontWeight.BOLD, size=15, color=LEAF_CARD_TITLE_TEXT_COLOR),
                create_progress_bar(leaf, "Points de Vie", on_used=on_stat_used),
                create_progress_bar(leaf, "Nourriture",    on_used=on_stat_used),
                create_progress_bar(leaf, "Hydratation",   on_used=on_stat_used),
                create_progress_bar(leaf, "Attaque",       on_used=on_stat_used),
                create_progress_bar(leaf, "Level",         on_used=on_stat_used),
            ],
            scroll="auto",
            tight=True,
            width=330,
            spacing=8,
        )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(leaf.name, weight=ft.FontWeight.BOLD, size=18, color=LEAF_CARD_TITLE_TEXT_COLOR),
        bgcolor= LEAF_CARD_BG_COLOR,
        content=build_content(),
        actions=[ft.TextButton("Fermer", on_click=close_modal)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()


# ──────────────────────────────────────────────────────────────
#  Écran principal
# ──────────────────────────────────────────────────────────────

def _build_leafs_home(page: ft.Page) -> list:
    import asyncio

    async def on_leaf_click(e, leaf_row, leaf):
        leaf_row.bgcolor = LEAF_BUTTON_BG_COLOR_CLICKED
        leaf_row.update()
        await asyncio.sleep(0.2)
        leaf_row.bgcolor = LEAF_BUTTON_BG_COLOR
        leaf_row.update()
        open_leaf_modal(page, leaf)

    def on_leaf_hover(e, leaf_row):
        leaf_row.bgcolor = LEAF_BUTTON_BG_COLOR_HOVER if e.data else LEAF_BUTTON_BG_COLOR
        leaf_row.update()

    def populate_list(query=""):
        items = []
        for leaf in leafmanager.owned:
            if query:
                q = query.lower()
                biome_name     = BIOMES[leaf.biome - 1]["name"].lower()
                leaf_type_name = LEAFS_TYPE[leaf.type]["name"].lower()
                if not (q in leaf.name.lower() or q in biome_name
                        or q in leaf_type_name or q in leaf.species.lower()):
                    continue

            leaf_row = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Image(src=leaf.img, width=50, height=50, fit="contain"),
                        width=60,
                        border=ft.border.all(2, LEAF_BUTTON_IMG_BORDER_COLOR),
                        bgcolor=LEAF_BUTTON_IMG_BG_COLOR,
                        padding=4,
                        border_radius=8,
                    ),
                    ft.Column([
                        ft.Text(leaf.name, weight=ft.FontWeight.BOLD, size=14, color=LEAF_BUTTON_NAME_COLOR),
                        ft.Row([
                            ft.Text(f"Type: {LEAFS_TYPE[leaf.type]['name']}", size=11, color=LEAF_BUTTON_TYPE_COLOR),
                            ft.Text(f"Biome: {BIOMES[leaf.biome - 1]['name']}", size=11, color=LEAF_BUTTON_BIOME_COLOR),
                        ]),
                    ], expand=True),
                ], expand=True),
                padding=10,
                border_radius=8,
                border=ft.border.all(2, LEAF_BUTTON_BORDER_COLOR),
                bgcolor=LEAF_BUTTON_BG_COLOR,
                animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            )

            leaf_row.on_hover = lambda e, r=leaf_row: on_leaf_hover(e, r)

            async def handle_click(e, r=leaf_row, l=leaf):
                await on_leaf_click(e, r, l)

            leaf_row.on_click = handle_click
            items.append(leaf_row)

        list_container.controls = items
        page.update()

    search = ft.Container(
                    ft.TextField(
                        label="🔍 Rechercher par nom, type ou biome...",
                        on_change=lambda e: populate_list(e.control.value.lower()),
                        text_style=ft.TextStyle(color=LEAF_SHEARCHBAR_INPUT_COLOR),
                        label_style=ft.TextStyle(color=LEAF_SHEARCHBAR_LABEL_COLOR),
                        hint_style=ft.TextStyle(color=LEAF_SHEARCHBAR_HINT_COLOR),
                        bgcolor=LEAF_SHEARCHBAR_BG_COLOR,
                        border_color=LEAF_SHEARCHBAR_BORDER_COLOR,
                        focused_border_color=LEAF_SHEARCHBAR_BORDER_COLOR_FOCUSED,
                        width=300,
                    ),
                    alignment=ft.Alignment.CENTER,
                    padding=4,
    )

    list_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=5, expand=True)
    populate_list()

    return [ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("Vos Leafs", size=22, weight=ft.FontWeight.BOLD, color=LEAF_TITLE_COLOR, text_align=ft.TextAlign.CENTER),
                        padding=5,
                        alignment=ft.Alignment.CENTER,
                    ),
                    search,
                    ft.Divider(),
                    list_container,
                    ],
                    expand=True,),
                bgcolor= LEAF_BG_COLOR,
                expand=True,
            )]  