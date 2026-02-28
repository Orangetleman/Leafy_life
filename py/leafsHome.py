from datacenter import *
import flet as ft

def create_progress_bar(value, max_value, label, color="green"):
    """Crée une barre de progression stylisée."""
    ratio = value / max_value if max_value > 0 else 0
    
    return ft.Column([
        ft.Row([
            ft.Text(label, weight=ft.FontWeight.W_500, size=14),
            ft.Text(f"{value}/{max_value}", size=12, color="gray"),
        ]),
        ft.ProgressBar(
            value=ratio,
            color=color,
            bgcolor="#4C4C4C",
            width=300,
            bar_height=20,
            border_radius=8,
        )
    ], spacing=5)

def prepare_leaf_data(leaf):
    """Prépare les données d'un leaf - assure que tous les attributs existent."""
    # Ajouter les attributs manquants si elles n'existent pas
    if not hasattr(leaf, 'nutrients') or leaf.nutrients is None:
        leaf.nutrients = 100
        print(f"Attribut 'nutrients' manquant pour {leaf.name}, initialisé à 100.")
    if not hasattr(leaf, 'atk') or leaf.atk is None:
        leaf.atk = 0
        print(f"Attribut 'atk' manquant pour {leaf.name}, initialisé à 0.")
    if not hasattr(leaf, 'hydration') or leaf.hydration is None:
        leaf.hydration = 100
        print(f"Attribut 'hydration' manquant pour {leaf.name}, initialisé à 100.")
    if not hasattr(leaf, 'regime') or leaf.regime is None:
        leaf.regime = None
        print(f"Attribut 'regime' manquant pour {leaf.name}, initialisé à None.")
    
    return leaf

def open_leaf_modal(page: ft.Page, leaf_dict):
    leaf = prepare_leaf_data(leaf_dict)

    def close_modal(e):
        dialog.open = False
        page.update()

    biome_name = BIOMES[leaf.biome - 1]['name']
    leaf_type_name = LEAFS_TYPE[leaf.type]['name']

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(leaf.name, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                ft.Row(
                    controls=[
                        ft.Image(src=leaf.img, width=150, height=150, fit="contain"),
                        ft.Divider(),
                        ft.Column([
                            ft.Row([
                                ft.Text("Biome:", size=14, color="white", weight=ft.FontWeight.BOLD),
                                ft.Text(biome_name, size=14, color="white"),
                            ]),
                            ft.Row([
                                ft.Text("Type:", size=14, color="white", weight=ft.FontWeight.BOLD),
                                ft.Text(leaf_type_name, size=14, color="white"),
                            ]),
                            ft.Row([
                                ft.Text("Rareté:", size=14, color="white", weight=ft.FontWeight.BOLD),
                                ft.Text(leaf.rarity, size=14, color="white"),
                            ]),
                            ft.Row([
                                ft.Text("Espèce:", size=14, color="white", weight=ft.FontWeight.BOLD),
                                ft.Text(leaf.species, size=14, color="white"),
                            ]),
                        ])
                    ],
                ),
                ft.Divider(),
                ft.Text("Statistiques", weight=ft.FontWeight.BOLD),
                create_progress_bar(leaf.hp, 10, "Points de Vie", color="red"),
                create_progress_bar(leaf.nutrients, 100, "Nourriture", color="orange"),
                create_progress_bar(leaf.hydration, 100, "Hydratation", color="blue"),
                create_progress_bar(leaf.atk, 10, "Attaque", color="purple"),
            ],
            scroll="auto",
            tight=True,        # ← important pour que la Column ne prenne pas toute la hauteur
            width=300,
        ),
        actions=[
            ft.TextButton("Fermer", on_click=close_modal),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # ✅ La bonne façon : ajouter à overlay PUIS open=True PUIS update
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def _build_leafs_home(page: ft.Page) -> list:
    """Écran des leafs - affiche la collection avec recherche."""
    
    def on_leaf_click(leaf):
        open_leaf_modal(page, leaf)
    
    def populate_list(query=""):
        """Remplit la liste en fonction de la recherche."""
        items = []
        
        for leaf in leafmanager.owned:
            # Filtrer par recherche
            if query:
                search_lower = query.lower()
                # Recherche par nom, biome, type ou espèce
                biome_name = BIOMES[leaf.biome - 1]['name'].lower()
                leaf_type_name = LEAFS_TYPE[leaf.type]['name'].lower()
                
                if not (search_lower in leaf.name.lower() or 
                        search_lower in biome_name or 
                        search_lower in leaf_type_name or
                        search_lower in leaf.species.lower()):
                    continue
            
            # Créer un conteneur avec les infos du leaf
            leaf_row = ft.Container(
                content=ft.Row([
                    # Image miniature
                    ft.Container(
                        content=ft.Image(
                            src=leaf.img,
                            width=50,
                            height=50,
                            fit="contain",
                        ),
                        width=60,
                    ),
                    # Infos du leaf
                    ft.Column([
                        ft.Text(leaf.name, weight=ft.FontWeight.BOLD, size=14),
                        ft.Row([
                            ft.Text(f"Type: {LEAFS_TYPE[leaf.type]['name']}", size=11, color="#45691f"),
                            ft.Text(f"Biome: {BIOMES[leaf.biome - 1]['name']}", size=11, color="#59842a"),
                        ]),
                    ], expand=True),
                ], expand=True),
                padding=10,
                border_radius=8,
                bgcolor="#92b368",
                on_click=lambda e, l=leaf: on_leaf_click(l),
            )
            items.append(leaf_row)
        
        list_container.controls = items
        page.update()
    
    # Barre de recherche
    search = ft.TextField(
        hint_text="🔍 Rechercher par nom, type ou biome...",
        on_change=lambda e: populate_list(e.control.value.lower()),
        width=300,
    )
    
    # Conteneur de liste
    list_container = ft.Column(scroll="auto", spacing=5)
    
    # Remplir la liste au démarrage
    populate_list()
    
    return [
        ft.Column([
            ft.Text("Vos Leafs", size=22, weight=ft.FontWeight.BOLD),
            search,
            ft.Divider(),
            list_container,
        ], expand=True)
    ]