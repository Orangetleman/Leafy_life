import flet as ft
def _build_shop_home(page: ft.Page) -> list:
    """Écran de la boutique - affiche les items à acheter."""
    dialog = ft.AlertDialog(
        title=ft.Text("Boutique"),
        content=ft.Text("Contenu de la boutique à venir..."),
        actions=[
            ft.TextButton("Fermer", on_click=lambda e: dialog.close()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )