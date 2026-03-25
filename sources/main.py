# -*- coding: utf-8 -*-
"""
Leafy Life - Point d'entrée Flet.
"""

import flet as ft
import os
import time
import subprocess

from datacenter import *
from leafsHome import _build_leafs_home
from planetHome import _planet
from planetHome import scene_actu
from inventoryHome import _build_inventory_home
from shopHome import _build_shop_home
from tuto import _tuto


# la video
def find_player(base_dir: str) -> tuple[str, list] | tuple[None, None]:
    """
    Cherche un lecteur vidéo disponible.
    Retourne (exe, args_prefix) ou (None, None).
    """
    candidates = [
        # mpv portable dans PROJET/tools/mpv/
        (
            os.path.join(base_dir, "source", "tools", "mpv", "mpv.exe"),
            ["--fs", "--no-terminal", "--really-quiet", "--no-border"],
        ),
        # VLC si installé en standard
        (
            r"C:\Program Files\VideoLAN\VLC\vlc.exe",
            ["--fullscreen", "--play-and-exit", "--no-video-title-show", "--no-osd"],
        ),
        (
            r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
            ["--fullscreen", "--play-and-exit", "--no-video-title-show", "--no-osd"],
        ),
    ]

    for exe, args in candidates:
        if os.path.isfile(exe):
            print(f" Lecteur trouvé : {exe}")
            return exe, args

    return None, None


# ─────────────────────────────────────────────────────────────────────────────
# Lecture vidéo — bloque jusqu'à la fin
# ─────────────────────────────────────────────────────────────────────────────

def play_intro_video(video_path: str, base_dir: str) -> None:
    if not os.path.isfile(video_path):
        print(f" !  Vidéo introuvable : {video_path}")
        return

    exe, args = find_player(base_dir)

    if exe is None:
        print(" !  Aucun lecteur trouvé. Installe mpv dans PROJET/tools/mpv/")
        print("    Téléchargement : https://mpv.io/installation/")
        return

    subprocess.run([exe] + args + [video_path])






# ---- Données de test ----
def _seed_test_data():
    inventory_manager.append_money("CO2", 1000)
    inventory_manager.append_money("O2",  1000)
    for key in range(1, 14):
        leafmanager.add_leaf(LEAFS[key])
    for item in range(1, 14):
        inventory_manager.append_item(ITEMS[item], amount=100)

NAVBAR_HEIGHT = 60

def _build_navbar(navigate) -> ft.Row:
    return ft.Row(
        [
            ft.Button("Leafs",     on_click=lambda e: navigate("leafs")),
            ft.Button("Shop",      on_click=lambda e: navigate("shop")),
            ft.Button("Inventory", on_click=lambda e: navigate("inventory")),
            ft.Button("Planet",    on_click=lambda e: navigate("planet")),
            ft.Button("Tuto",    on_click=lambda e: navigate("tuto")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
    )


def main(page: ft.Page, page_name: str = "tuto") -> None:
    page.window.maximized = True
    page.window.focused   = True
    page.title      = "Leafy Life"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor    = "#1a1a1a"
    page.padding    = 0
    page.spacing    = 0

    def show_screen(name: str):
        if hasattr(page, "stop_current_screen"):
            page.stop_current_screen()
            del page.stop_current_screen

        # ── Nettoyage avant changement d'écran ────────────────────────────────────────
        page.on_resize         = None
        page.window.on_event   = None  # évite que le handler planet reste actif ailleurs

        # Vide les callbacks du game_clock pour éviter l'accumulation de tick_refresh
        # des modals leaf ouverts sans être explicitement fermés avant navigation.
        # Chaque écran qui en a besoin (ex : modal leaf) les re-enregistre lui-même.
        game_clock.callbacks.clear()

        page.clean()

        if name == "leafs":
            body = _build_leafs_home(page)
        elif name == "shop":
            body = _build_shop_home(page)
        elif name == "inventory":
            body = _build_inventory_home(page)
        elif name == "planet":
            body = _planet(page, show_screen)
        else:
            body = _tuto(page)

        body_container = ft.Container(
            content=ft.Column(controls=body, expand=True),
            expand=True,
            padding=0,
        )
        page.body_container = body_container
        page.navbar_height   = NAVBAR_HEIGHT

        page.add(
            ft.Container(content=_build_navbar(show_screen), padding=8, bgcolor="#131313"),
            body_container,
        )

    # ── Démarrage du game clock ───────────────────────────────────────────────────────
    # On N'ajoute PAS de callback page.update() global ici.
    # Chaque écran gère ses propres mises à jour via control.update() ou
    # des callbacks ciblés (ex : tick_refresh dans open_leaf_modal).
    # Un page.update() global toutes les 30s forçait un re-rendu complet de la page
    # et vidait le buffer Flet, ce qui causait des délais sur les effets hover.
    game_clock.start(page)

    show_screen(page_name)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    VIDEO_PATH = os.path.join(BASE_DIR, "assets", "musics", "test.mp4")
    music.play("assets/musics/frogmusic.wav")
    play_intro_video(VIDEO_PATH, BASE_DIR)
    time.sleep(0.8)

    _seed_test_data()
    music.play("assets/musics/lobby.wav", loop=True)
    ft.run(main)
    music.stop()

    if scene_actu[0] >= len(LORE):
        music.play("assets/musics/frogmusic.wav", loop=True)
        play_intro_video(VIDEO_PATH, BASE_DIR)
        time.sleep(0.8)
        music.stop()