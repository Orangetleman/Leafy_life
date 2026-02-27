from datacenter import *
import flet as ft

def create_progress_bar(value, max_value, label, color="green"):
    """Crée une barre de progression stylisée."""
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    
    return ft.Column([
        ft.Row([
            ft.Text(label, weight=ft.FontWeight.W_500, size=14),
            ft.Text(f"{value}/{max_value}", size=12, color="gray"),
        ]),
        ft.Container(
            content=ft.Container(
                width=f'{percentage}%',
                height=20,
                bgcolor=color,
                border_radius=4,
            ),
            width=200,
            height=20,
            bgcolor="rgba(200, 200, 200, 0.3)",
            border_radius=4,
        )
    ], spacing=0)

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
    print("Ouverture du modal pour le leaf:", leaf_dict.name)
    """Ouvre le modal affichant les détails complets d'un leaf (comme en JavaScript)."""
    leaf = prepare_leaf_data(leaf_dict)
    
    def close_modal(e):
        bs.open = False
        page.update()
    
    # Récupérer les infos du biome et du type
    biome_name = BIOMES[leaf.biome - 1]['name']
    leaf_type_name = LEAFS_TYPE[leaf.type]['name']
    
    # Construire le contenu du modal
    modal_content = ft.Column(
        [
            ft.Text(leaf.name, size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Image(
                    src=leaf.img,
                    width=150,
                    height=150,
                    fit="contain",
                ),
                alignment=ft.Alignment.CENTER,
                margin=ft.margin.only(bottom=10),
            ),
            ft.Text(f"Biome: {biome_name}", size=14),
            ft.Text(f"Type: {leaf_type_name}", size=14),
            ft.Text(f"Rareté: {leaf.rarity}", size=14),
            ft.Text(f"Espèce: {leaf.species}", size=14),
            ft.Divider(),
            ft.Text("Statistiques", weight=ft.FontWeight.BOLD, size=14),
            ft.Text(f"Niveau: {leaf.competence_lvl}", weight=ft.FontWeight.W_500),
            create_progress_bar(leaf.hp, 10, "Points de Vie", color="red"),
            create_progress_bar(leaf.nutrients, 100, "Nourriture", color="orange"),
            create_progress_bar(leaf.hydration, 100, "Hydratation", color="blue"),
            create_progress_bar(leaf.atk, 10, "Attaque", color="purple"),
            ft.ElevatedButton("Fermer", on_click=close_modal),
        ],
        scroll="auto",
        spacing=10
    )
    
    bs = ft.BottomSheet(
        ft.Container(
            modal_content,
            padding=20,
        )
    )
    page.overlay.append(bs)
    bs.open = True
    page.update()
    print("Modal créé pour le leaf:", leaf.name)

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