from datacenter import *
from style import *
import flet as ft

# ──────────────────────────────────────────────────────────────
#  Config d'affichage par label
#  (label -> stat_attr, couleur_base, couleur_boost|None)
# ──────────────────────────────────────────────────────────────
STAT_DISPLAY = {
    "Points de Vie": ("hp",        LEAF_CARD_PROGRESS_BAR_HP_COLOR,        LEAF_CARD_PROGRESS_BAR_BOOST_HP_COLOR),
    "Nourriture":    ("nutrients",  LEAF_CARD_PROGRESS_BAR_NUTRIENTS_COLOR, LEAF_CARD_PROGRESS_BAR_BOOST_NUTRIENTS_COLOR),
    "Hydratation":   ("hydration",  LEAF_CARD_PROGRESS_BAR_HYDRATION_COLOR, None),
    "Attaque":       ("atk",        LEAF_CARD_PROGRESS_BAR_ATK_COLOR,       LEAF_CARD_PROGRESS_BAR_BOOST_ATK_COLOR),
    "Level":         ("level",      LEAF_CARD_PROGRESS_BAR_LVL_COLOR,       None),
}

BAR_WIDTH = 200  # largeur fixe de toutes les barres (px)


# ──────────────────────────────────────────────────────────────
#  Item de base adapté au leaf et à la stat (toujours affiché)
# ──────────────────────────────────────────────────────────────
def base_item_for_stat(leaf, stat_attr):
    species = leaf.species
    regime  = getattr(leaf, "regime", None)
    hp      = getattr(leaf, "hp", 1)

    if stat_attr == "nutrients":
        if species == "plant":
            return ITEMS[2]                                          # Fertilisant
        return ITEMS[3] if regime == "carnivore" else ITEMS[4]      # Viande / Herbe

    elif stat_attr == "hydration":
        return ITEMS[1]                                              # Eau minérale

    elif stat_attr == "hp":
        if hp == 0:
            return ITEMS[7]                                          # Rayon de soleil (revive)
        return ITEMS[5] if species == "plant" else ITEMS[6]         # Sève / Bandage

    elif stat_attr == "level":
        return ITEMS[13]                                             # Livre de la connaissance

    return None


# ──────────────────────────────────────────────────────────────
#  Item boost adapté au leaf et à la stat (affiché si dispo)
# ──────────────────────────────────────────────────────────────
def boost_item_for_stat(leaf, stat_attr):
    """Retourne l'item boost seulement si le joueur le possède."""
    mapping = {
        "nutrients": ITEMS[9] if leaf.species == "plant" else ITEMS[8],  # Poudre d'os / Lait
        "hp":        ITEMS[12],   # Potion de vie
        "atk":       ITEMS[11],   # Potion d'attaque
    }
    item = mapping.get(stat_attr)
    if item is None:
        return None
    owned = next((i for i in inventory_manager.get_items() if i["id"] == item["id"]), None)
    return item if owned else None


# ──────────────────────────────────────────────────────────────
#  Barre de stats avec overlay boost
# ──────────────────────────────────────────────────────────────
def create_stat_bar(value, base_max, boost_value, boost_max, color, boost_color):
    base_ratio  = value / base_max if base_max > 0 else 0
    boost_ratio = boost_value / base_max if base_max > 0 else 0

    if boost_max > 0 and boost_color is not None:
        return ft.Container(
            content=ft.Stack([
                # Barre de base
                ft.ProgressBar(
                    value=base_ratio,
                    color=color,
                    bgcolor=LEAF_CARD_PROGRESS_BAR_BG_COLOR,
                    width=BAR_WIDTH,
                    bar_height=20,
                    border_radius=8,
                ),
                # Barre boost superposée (transparente si boost = 0)
                ft.ProgressBar(
                    value=boost_ratio,
                    color=ft.Colors.with_opacity(0.6, boost_color) if boost_value > 0 else ft.Colors.with_opacity(0, "white"),
                    bgcolor=ft.Colors.with_opacity(0, "white"),
                    width=BAR_WIDTH,
                    bar_height=20,
                    border_radius=8,
                ),
            ], width=BAR_WIDTH, height=20),
            width=BAR_WIDTH,
            height=20,
            border_radius=8,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
    else:
        return ft.ProgressBar(
            value=base_ratio,
            color=color,
            bgcolor=LEAF_CARD_PROGRESS_BAR_BG_COLOR,
            width=BAR_WIDTH,
            bar_height=20,
            border_radius=8,
        )


# ──────────────────────────────────────────────────────────────
#  Badge cliquable (base ou boost)
# ──────────────────────────────────────────────────────────────
def create_badge_button(leaf, current_value, max_value, item, is_boost=False, on_used=None):
    """
    is_boost=False -> item de base : toujours affiché, warning si absent de l'inventaire.
    is_boost=True  -> item boost   : affiché seulement si en inventaire (vérifié par l'appelant).
    """
    if item is None:
        return ft.Container(width=0, height=0, visible=False)

    in_inventory = next((i for i in inventory_manager.get_items() if i["id"] == item["id"]), None)
    at_max       = current_value >= max_value
    warning      = not in_inventory and not is_boost   # item de base manquant

    # Boost items : ne jamais afficher si pas en inventaire (l'appelant vérifie déjà, sécurité)
    if is_boost and not in_inventory:
        return ft.Container(width=0, height=0, visible=False)

    disabled     = at_max or warning
    border_color = (LEAF_CARD_BADGE_WARNING_BORDER_COLOR if warning
                    else (LEAF_CARD_BADGE_BOOST_BORDER_COLOR if is_boost
                        else LEAF_CARD_BADGE_BORDER_COLOR))

    item_name = item["name"].replace(" 🌟", "")

    def on_over(e):
        if not disabled:
            e.control.bgcolor = LEAF_CARD_BADGE_BG_HOVER_COLOR if e.data else LEAF_CARD_BADGE_BG_COLOR
            e.control.update()

    def on_click(e):
        owned = next((i for i in inventory_manager.get_items() if i["id"] == item["id"]), None)
        if not owned or owned["amount"] < 1:
            print(f"Pas de {item_name} en inventaire.")
            return
        if at_max:
            print(f"Stat au maximum pour {leaf.name}.")
            return
        leaf.apply_item(item)
        inventory_manager.remove_item(item["id"], 1)
        if on_used:
            on_used()

    tooltip = (
        f"⚠️ {item_name} non disponible" if warning
        else ("Max boost atteint"        if at_max and is_boost
            else ("Déjà au maximum"      if at_max
                else f"{'[BOOST] ' if is_boost else ''}Utiliser : {item['name']} "
                    f"(+{item['effect']['amount']} {item['effect']['stat']})"))
    )

    return ft.Container(
        content=ft.Image(src=item["icon"], width=18, height=18, fit="contain"),
        padding=5,
        bgcolor=LEAF_CARD_BADGE_BG_COLOR,
        border=ft.border.all(1, border_color),
        border_radius=8,
        width=32,
        height=32,
        alignment=ft.Alignment.CENTER,
        on_click=on_click if not (at_max and not warning) else None,
        on_hover=on_over,
        tooltip=tooltip,
        opacity=0.4 if disabled else 1.0,
    )


# ──────────────────────────────────────────────────────────────
#  Barre de progression + badges (base + boost)
# ──────────────────────────────────────────────────────────────
def create_progress_bar(leaf, label, on_used=None):
    stat_attr, color, boost_color = STAT_DISPLAY[label]
    base_max    = leaf.STAT_MAX.get(stat_attr, 100)
    value       = getattr(leaf, stat_attr, 0)
    boost_value = getattr(leaf, f"{stat_attr}_boost", 0)
    boost_max   = getattr(leaf, f"{stat_attr.upper()}_BOOST_MAX", 0)

    # Couleurs d'alerte sur les stats vitales
    if label == "Nourriture"  and value <= 20: color = LEAF_CARD_PROGRESS_BAR_NUTRIENTS_ALERT_COLOR
    if label == "Hydratation" and value <= 20: color = LEAF_CARD_PROGRESS_BAR_HYDRATION_ALERT_COLOR

    base_item  = base_item_for_stat(leaf, stat_attr)
    boost_item = boost_item_for_stat(leaf, stat_attr)   # None si absent de l'inventaire

    # Texte valeur
    val_text = f"{value}/{base_max}"
    if boost_value > 0:
        val_text += f"  +{boost_value}"

    # Badges
    badges = []
    if base_item:
        badges.append(create_badge_button(leaf, value, base_max, base_item,
                                        is_boost=False, on_used=on_used))
    if boost_item:
        badges.append(create_badge_button(leaf, boost_value, boost_max, boost_item,
                                        is_boost=True, on_used=on_used))

    return ft.Column([
        ft.Row([
            ft.Text(label, weight=ft.FontWeight.W_500, size=14, color=LEAF_CARD_TITLE_TEXT_COLOR),
            ft.Text(val_text, size=12, color=LEAF_CARD_INFO_TEXT_COLOR),
        ]),
        ft.Row(
            [create_stat_bar(value, base_max, boost_value, boost_max, color, boost_color)] + badges,
            spacing=6,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    ], spacing=4)


# ──────────────────────────────────────────────────────────────
#  Bouton de récolte individuel (dans le modal leaf)
# ──────────────────────────────────────────────────────────────
def create_harvest_button(leaf, on_harvested=None):
    pending  = int(leaf.pending_currency)
    currency = LeafStat.CURRENCY_PRODUCED[leaf.species]
    has_prod = pending > 0

    def on_hover(e):
        if has_prod:
            btn.bgcolor = LEAF_CARD_HARVEST_BUTTON_BG_HOVER_COLOR if e.data else LEAF_CARD_HARVEST_BUTTON_BG_COLOR
            btn.update()

    def on_click(e):
        c, amt = leaf.harvest()
        if amt > 0 and on_harvested:
            on_harvested()

    btn = ft.Container(
        content=ft.Row([
            ft.Text("🌾 Récolter", size=14, color=LEAF_CARD_HARVEST_BUTTON_TEXT_COLOR,
                    weight=ft.FontWeight.W_500),
            ft.Container(
                content=ft.Text(
                    f"{pending} {currency}" if has_prod else "rien à récolter",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=LEAF_CARD_HARVEST_BUTTON_TEXT_COLOR,
                ),
                bgcolor=LEAF_CARD_HARVEST_BADGE_BG_COLOR if has_prod else LEAF_CARD_PROGRESS_BAR_BG_COLOR,
                border_radius=6,
                padding=ft.padding.symmetric(horizontal=8, vertical=2),
            ),
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=LEAF_CARD_HARVEST_BUTTON_BG_COLOR if has_prod else LEAF_CARD_HARVEST_BUTTON_BG_EMPTY_COLOR,
        border=ft.border.all(1, LEAF_CARD_HARVEST_BUTTON_BORDER_COLOR),
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        alignment=ft.Alignment(0, 0),
        on_click=on_click if has_prod else None,
        on_hover=on_hover,
        opacity=1.0 if has_prod else 0.5,
        animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        tooltip=f"Récolter {pending} {currency}" if has_prod else "Pas encore de production accumulée",
    )
    return btn


# ──────────────────────────────────────────────────────────────
#  Modal leaf
# ──────────────────────────────────────────────────────────────
def open_leaf_modal(page: ft.Page, leaf, on_harvested_global=None):

    def close_modal(e):
        # Retire l'overlay de page.overlay — évite l'accumulation d'overlays invisibles
        # qui alourdit chaque page.update() après plusieurs ouvertures de modals.
        if overlay in page.overlay:
            page.overlay.remove(overlay)
        if tick_refresh in game_clock.callbacks:
            game_clock.callbacks.remove(tick_refresh)
        page.update()

    def on_stat_used():
        modal_content.content = build_content()
        if on_harvested_global:
            on_harvested_global()
        page.update()

    def build_content():
        biome_name     = BIOMES[leaf.biome - 1]["name"]
        leaf_type_name = LEAFS_TYPE[leaf.type]["name"]
        return ft.Column(
            [
                # ── Infos générales ──────────────────────────────
                ft.Row([
                    ft.Image(src=leaf.img, width=100, height=100, fit="contain"),
                    ft.Column([
                        ft.Row([ft.Text("Biome :",  size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_TITLE_TEXT_COLOR),
                                ft.Text(biome_name,     size=13, color=LEAF_CARD_INFO_TEXT_COLOR)]),
                        ft.Row([ft.Text("Type :",   size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_TITLE_TEXT_COLOR),
                                ft.Text(leaf_type_name, size=13, color=LEAF_CARD_INFO_TEXT_COLOR)]),
                        ft.Row([ft.Text("Rareté :", size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_TITLE_TEXT_COLOR),
                                ft.Text(leaf.rarity,    size=13, color=LEAF_CARD_INFO_TEXT_COLOR)]),
                        ft.Row([ft.Text("Espèce :", size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_TITLE_TEXT_COLOR),
                                ft.Text(leaf.species,   size=13, color=LEAF_CARD_INFO_TEXT_COLOR)]),
                    ], spacing=4),
                ], spacing=12),
                ft.Divider(color="#444"),
                # ── Statistiques ─────────────────────────────────
                ft.Text("Statistiques", weight=ft.FontWeight.BOLD, size=15, color=LEAF_CARD_TITLE_TEXT_COLOR),
                create_progress_bar(leaf, "Points de Vie", on_used=on_stat_used),
                create_progress_bar(leaf, "Nourriture",    on_used=on_stat_used),
                create_progress_bar(leaf, "Hydratation",   on_used=on_stat_used),
                create_progress_bar(leaf, "Attaque",       on_used=on_stat_used),
                create_progress_bar(leaf, "Level",         on_used=on_stat_used),
                ft.Divider(color="#444"),
                # ── Bouton récolte individuel ─────────────────────
                create_harvest_button(leaf, on_harvested=on_stat_used),
            ],
            scroll="auto",
            tight=True,
            width=350,
            spacing=8,
        )

    modal_content = ft.Container(content=build_content())

    overlay = ft.Container(
        visible=True,
        expand=True,
        bgcolor=ft.Colors.with_opacity(LEAF_CARD_SHADOW_COLOR[0], LEAF_CARD_SHADOW_COLOR[1]),
        alignment=ft.Alignment(0, 0),
        content=ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.BASIC,
            on_tap=close_modal,
            content=ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(leaf.name, weight=ft.FontWeight.BOLD, size=18,
                                color=LEAF_CARD_TITLE_TEXT_COLOR),
                        ft.Divider(color="#444"),
                        modal_content,
                        ft.Row([
                            ft.TextButton("Fermer", on_click=close_modal)
                        ], alignment=ft.MainAxisAlignment.END),
                    ], tight=True, spacing=8),
                    bgcolor=LEAF_CARD_BG_COLOR,
                    border=ft.border.all(2, LEAF_CARD_BORDER_COLOR),
                    border_radius=12,
                    padding=20,
                    width=400,
                    on_click=lambda e: None,
                )
            )
        )
    )

    def tick_refresh():
        """Rafraîchit le modal à chaque tick du game_clock (toutes les 30s)."""
        if overlay.visible:
            modal_content.content = build_content()
            page.update()

    game_clock.add_callback(tick_refresh)
    page.overlay.append(overlay)
    page.update()


# ──────────────────────────────────────────────────────────────
#  Écran principal Leafs
# ──────────────────────────────────────────────────────────────
def _build_leafs_home(page: ft.Page) -> list:
    import asyncio

    async def on_leaf_click(e, leaf_row, leaf):
        leaf_row.bgcolor = LEAF_BUTTON_BG_COLOR_CLICKED
        leaf_row.update()
        await asyncio.sleep(0.05)
        open_leaf_modal(page, leaf, on_harvested_global=refresh_harvest_btns)
        await asyncio.sleep(0.2)
        leaf_row.bgcolor = LEAF_BUTTON_BG_COLOR
        leaf_row.update()

    def on_leaf_hover(e, leaf_row):
        # ── IMPORTANT : appeler leaf_row.update() pour que le changement de bgcolor
        # soit envoyé immédiatement au frontend. Sans cela, le changement est bufferisé
        # et n'apparaît que lors du prochain page.update() global — ce qui causait
        # un délai pouvant aller jusqu'à 30 secondes sur l'effet hover. ──────────────
        leaf_row.bgcolor = LEAF_BUTTON_BG_COLOR_HOVER if e.data else LEAF_BUTTON_BG_COLOR
        leaf_row.update()

    # ── Helpers pour les boutons de récolte globale ───────────────────────────────────
    def get_pending_total(specie: str) -> int:
        return sum(int(l.pending_currency) for l in leafmanager.owned if l.species == specie)

    # Textes de montant référencés pour mise à jour dynamique sans rebuild complet
    o2_amount_text  = ft.Text("0", size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_HARVEST_BUTTON_TEXT_COLOR)
    co2_amount_text = ft.Text("0", size=13, weight=ft.FontWeight.BOLD, color=LEAF_CARD_HARVEST_BUTTON_TEXT_COLOR)

    def refresh_harvest_btns():
        pending_o2  = get_pending_total("plant")
        pending_co2 = get_pending_total("animal")

        o2_amount_text.value  = str(pending_o2)
        co2_amount_text.value = str(pending_co2)

        harvest_O2_btn.opacity  = 1.0 if pending_o2  > 0 else 0.4
        harvest_CO2_btn.opacity = 1.0 if pending_co2 > 0 else 0.4

        harvest_O2_btn.bgcolor  = LEAF_CARD_HARVEST_BUTTON_BG_COLOR if pending_o2  > 0 else LEAF_CARD_HARVEST_BUTTON_BG_EMPTY_COLOR
        harvest_CO2_btn.bgcolor = LEAF_CARD_HARVEST_BUTTON_BG_COLOR if pending_co2 > 0 else LEAF_CARD_HARVEST_BUTTON_BG_EMPTY_COLOR

        harvest_O2_btn.on_click  = (lambda e: (leafmanager.harvest_all("plant"),  refresh_harvest_btns())) if pending_o2  > 0 else None
        harvest_CO2_btn.on_click = (lambda e: (leafmanager.harvest_all("animal"), refresh_harvest_btns())) if pending_co2 > 0 else None

        harvest_O2_btn.tooltip  = f"Récolter tout ({pending_o2} O2)"   if pending_o2  > 0 else "Rien à récolter"
        harvest_CO2_btn.tooltip = f"Récolter tout ({pending_co2} CO2)" if pending_co2 > 0 else "Rien à récolter"

        # Ne mettre à jour que si les contrôles sont déjà montés sur la page —
        # evite le RuntimeError lors du premier appel dans populate_list() au chargement.
        try:
            harvest_O2_btn.update()
            harvest_CO2_btn.update()
        except RuntimeError:
            pass

    game_clock.add_callback(refresh_harvest_btns)

    def make_harvest_btn(amount_text_widget: ft.Text, currency: str):
        """Construit un bouton de récolte globale pour une espèce donnée."""
        btn = ft.Container(
            content=ft.Column([
                ft.Text("🌾", size=22),
                ft.Text(currency, size=11, weight=ft.FontWeight.BOLD,
                        color=LEAF_CARD_HARVEST_BUTTON_TEXT_COLOR),
                amount_text_widget,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER, spacing=2),
            width=140, height=90,
            border_radius=10,
            bgcolor=LEAF_CARD_HARVEST_BUTTON_BG_EMPTY_COLOR,
            border=ft.border.all(1, LEAF_CARD_HARVEST_BUTTON_BORDER_COLOR),
            alignment=ft.Alignment(0, 0),
            opacity=0.4,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        )

        def on_hover(e, b=btn, currency=currency):
            # Ne réagit au hover que si le bouton est actif (opacity == 1)
            if b.opacity == 1.0:
                b.bgcolor = LEAF_CARD_HARVEST_BUTTON_BG_HOVER_COLOR if e.data else LEAF_CARD_HARVEST_BUTTON_BG_COLOR
                b.update()

        btn.on_hover = on_hover
        return btn

    harvest_O2_btn  = make_harvest_btn(o2_amount_text,  "O2")
    harvest_CO2_btn = make_harvest_btn(co2_amount_text, "CO2")

    def populate_list(query=""):
        items = []
        for leaf in leafmanager.owned:
            if query:
                q              = query.lower()
                biome_name     = BIOMES[leaf.biome - 1]["name"].lower()
                leaf_type_name = LEAFS_TYPE[leaf.type]["name"].lower()
                if not (q in leaf.name.lower() or q in biome_name
                        or q in leaf_type_name   or q in leaf.species.lower()):
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
                            ft.Text(f"Type: {LEAFS_TYPE[leaf.type]['name']}",    size=11, color=LEAF_BUTTON_TYPE_COLOR),
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

        leaf_column.controls = items
        refresh_harvest_btns()
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
            width=400,
        ),
        alignment=ft.Alignment.CENTER,
        padding=4,
    )

    leaf_column    = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=5, expand=True)
    list_container = ft.Container(leaf_column, expand=True, padding=ft.padding.symmetric(horizontal=10))
    populate_list()

    return [ft.Container(
        content=ft.Column([
            ft.Container(
                ft.Row(
                    controls=[
                        harvest_O2_btn,
                        ft.Container(
                            ft.Column([
                                ft.Container(
                                    content=ft.Text("Vos Leafs", size=22, weight=ft.FontWeight.BOLD,
                                                    color=LEAF_TITLE_COLOR, text_align=ft.TextAlign.CENTER),
                                    padding=5,
                                    alignment=ft.Alignment.CENTER,
                                ),
                                search,
                            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True,
                            alignment=ft.Alignment.CENTER,
                        ),
                        harvest_CO2_btn,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.symmetric(horizontal=20),
            ),
            ft.Divider(),
            list_container,
        ], expand=True),
        bgcolor=LEAF_BG_COLOR,
        expand=True,
    )]