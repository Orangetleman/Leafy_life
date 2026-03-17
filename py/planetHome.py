import flet as ft
from pynput import keyboard as pynput_keyboard
from datacenter import *
from style import *
import asyncio
import pyglet
import threading
import random

# Charge la musique
'''music = pyglet.media.load("assets/musics/frogmusic.wav", streaming=False)
music_player = pyglet.media.Player()
music_player.queue(music)
music_player.loop = True
music_player.play()

# Lance pyglet en arrière-plan
threading.Thread(target=pyglet.app.run, daemon=True).start()'''


def _planet(page: ft.Page, navigate) -> list:
    page.title = "Planet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    plaine = ft.Text("explore plaine", size=30,color='black')

    keys_pressed = {"right": False, "left": False, "space":False}
    dialogue_active = [False]
    running = [True]
    focused = [True]

    def on_press(key):
            if not focused[0]:
                return
            if dialogue_active[0]:  # ← bloquer toutes les touches pendant le dialogue
                return
            try:
                if key.char in ("d", "D"):
                    keys_pressed["right"] = True
                elif key.char in ("q", "Q"):
                    keys_pressed["left"] = True
            except AttributeError:
                if key == pynput_keyboard.Key.right:
                    keys_pressed["right"] = True
                elif key == pynput_keyboard.Key.left:
                    keys_pressed["left"] = True
                elif key == pynput_keyboard.Key.space:
                    keys_pressed["space"] = True

    def on_release(key):
        try:
            if key.char in ("d", "D"):
                keys_pressed["right"] = False
            elif key.char in ("q", "Q"):
                keys_pressed["left"] = False
        except AttributeError:
            if key == pynput_keyboard.Key.right:
                keys_pressed["right"] = False
            elif key == pynput_keyboard.Key.left:
                keys_pressed["left"] = False
            elif key == pynput_keyboard.Key.space: 
                keys_pressed["space"] = False

    
    def on_window_event(e):
        if e.type == ft.WindowEventType.FOCUS:
            focused[0] = True
        elif e.type == ft.WindowEventType.BLUR:
            focused[0] = False
            keys_pressed["right"] = False
            keys_pressed["left"] = False

    def dialogue(e, scene, dialogue_active):
        i_scene = [0]

        def next_dialogue(key):
            if key == pynput_keyboard.Key.space:
                if i_scene[0] < len(scene) - 1:  
                    i_scene[0] += 1
                    if i_scene[0]%2==0:
                        npc_msg.content.value = scene[i_scene[0]] 
                        chara_msg.visible = False
                        npc_msg.visible = True
                    else:
                        chara_msg.content.value = scene[i_scene[0]] 
                        chara_msg.visible = True
                        npc_msg.visible = False
                        page.update()
                else:
                    dialogue_box.visible = False  
                    dialogue_active[0] = False
                    page.update()
                    listener.stop()  


        msg=scene[i_scene[0]]
        
        chara_msg = ft.Container(
                content=ft.Text(msg,size= 30),
                bgcolor=ft.Colors.with_opacity(0.6, "green"),
                alignment=ft.Alignment.CENTER_RIGHT,
                height=200,
                visible=False
            )
        
        npc_msg = ft.Container(
                content=ft.Text(msg,size= 30),
                bgcolor=ft.Colors.with_opacity(0.6, "green"),
                alignment=ft.Alignment.CENTER_LEFT,
                height=200,
                visible=True
            )
        
        dialogue_box = ft.Container(content= ft.Stack([chara_msg, npc_msg]),
            alignment=ft.Alignment.BOTTOM_CENTER
        )
        
        listener = pynput_keyboard.Listener(on_press=next_dialogue)
        listener.start()

        return dialogue_box
    
    def tp(e):
        page.clean()
        running[0] = True
        event = random.choice(EVENTS["plain"])

        le_txt = ft.Text('planet', size=30)

        bouton_retour = ft.Container(
            content=ft.Row(
                [ft.Container(
                content=ft.Text("planète", size=20, color="white"),
                padding=10,
                border_radius=8,
                on_click=retourneur,  # ← on_click directement sur Container
            )],  
                alignment=ft.Alignment.TOP_LEFT,
            )
        )

        new_sprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180),
            animate_position=ft.Animation(50, ft.AnimationCurve.LINEAR),
        )

        preset = [
            ft.Container(
                content=ft.Image(src="assets/imgs/icons/arriere_plain.png", fit="cover"),
                expand=True,
            ),
        ]

        id = None
        emplacement = random.choice([ft.Alignment.CENTER_LEFT, ft.Alignment.CENTER_RIGHT])
        if event["type"] == "enemy":
            id = random.choice(ENEMIES)
            preset.append(ft.Container(
                content=ft.Image(src=id["visual"], width=80, height=60),
                alignment=emplacement,
            ))
        elif event["type"] == "npc":
            id = random.choice(NPCS)
            preset.append(ft.Container(
                content=ft.Image(src=id["visual"], width=80, height=60),
                alignment=emplacement,
            ))
        elif event["type"] == "empty":
            id = random.choice(OBJECTS)
            preset.append(ft.Container(
                content=ft.Image(src=id["visual"], width=180, height=160),
                alignment=emplacement,
            ))

        preset.append(new_sprite)
        preset.append(bouton_retour)
        

        new_listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
        new_listener.start()

        def stop_tp_screen(e=None):
            running[0] = False
            new_listener.stop()

        page.stop_current_screen = stop_tp_screen
        page.window.on_event = on_window_event

        async def tp_game_loop():
            biome_img_ratio = 1250 / 649
            new_sprite.left = page.width / 2  # ← init immédiate, pas après sleep
            while running[0]:
                if dialogue_active[0]:  # ← rien ne se passe pendant le dialogue
                    await asyncio.sleep(0.025)
                    continue
                if keys_pressed["right"]:
                    new_sprite.left = new_sprite.left + 15
                if keys_pressed["left"]:
                    new_sprite.left = new_sprite.left - 15

                biome_height = page.width / biome_img_ratio
                new_sprite.bottom = (biome_height / 4) + (page.height - biome_height)

                if new_sprite.left < 0:
                    print(f"sortie gauche: left={new_sprite.left}")
                    stop_tp_screen()
                    tp(e)
                    return
                if new_sprite.left > page.width - 150:
                    print(f"sortie droite: left={new_sprite.left}, width={page.width}")
                    stop_tp_screen()
                    tp(e)
                    return
                if event["type"] == "enemy" and ((new_sprite.left < 100 and emplacement == ft.Alignment.CENTER_LEFT) or (new_sprite.left > (page.width - 200) and emplacement == ft.Alignment.CENTER_RIGHT)):
                    stop_tp_screen()
                    combat(e,'plain',id)
                """if event["type"]=="npc" and ((new_sprite.left < 100 and emplacement == ft.Alignment.CENTER_LEFT) or (new_sprite.left > (page.width - 200) and emplacement == ft.Alignment.CENTER_RIGHT)):
                    wandering_shop()"""
                if event["type"] == "empty" and ((new_sprite.left < 100 and emplacement == ft.Alignment.CENTER_LEFT) or (new_sprite.left > (page.width - 200) and emplacement == ft.Alignment.CENTER_RIGHT)) and keys_pressed["space"]: 
                    print("eau recupérée")
                    keys_pressed["space"] = False

            

                page.update()
                await asyncio.sleep(0.025)
        
        event_scene = ft.Container(
            content=ft.Stack(preset),
            expand=True,
        )

        page.add(event_scene)
        page.run_task(tp_game_loop)

    def combat(e,biome,enemy):
        page.clean()
        #musique
        leafsprite = ft.Container(
            content=ft.Image(src="assets/imgs/leafs/Froggy.png", width=150, height=180), 
            bottom=page.height * 0.20,
            left=20,
            )
        enemysprite = ft.Container(
                content=ft.Image(src=enemy["visual"], width=150, height=180),
                bottom=page.height * 0.20,
                right=20,
            )
        menu = ft.Container(bottom=0, left=0, width=page.width, height=page.height * 0.20, bgcolor=ft.Colors.with_opacity(0.8, "green")) 
        """CHRIS A AJOUTER BOUTONS (atk,competence et boite_leaf) + BARRE PV ET INFOS LEAF STP"""
        
        preset = [
            ft.Container(
                content=ft.Image(src="assets/imgs/icons/arriere_plain.png", fit="cover"),
                expand=True,
            ),
            leafsprite,
            enemysprite,
            menu
        ]

        layout = ft.Container(content=ft.Stack(preset))
        page.add(layout)
        

    def atk(leaf,enemy):
        malus = "-" + leaf.atk
        dgts = ft.Container(ft.Text(malus,size=20),visible=True)
        leaf.left = page.width - 20
        page.update()
        page.add(dgts)
        #wait 0.2 sec
        dgts.visible=False
        leaf.left = 20
        page.update()
        enemy.pv -= leaf.atk

    def competence(leaf,enemy):
        if leaf.type == 'dps':
            leaf.atk *= 2
            atk(leaf,enemy)
            leaf.atk /= 2
            return None
        
        elif leaf.type == 'tank':
            bouclier = ft.Container(ft.Image(src='leaf_type_tank.png',width=100,height=100),visible=True)
            page.add(bouclier)
            enemy.atk /=2
            tour = 2
            return tour
        
        else:
            return None
        
    def boite_leaf():
        pass
    """CHRISSS FAIS ICI"""


    planet = ft.Stack([
        ft.Container(
            ft.Image(src="assets/imgs/icons/biome_plain.png"),
            alignment=ft.Alignment.CENTER,
            expand=True
        ),
        ft.Container(
            content=ft.Row(
                [ft.ElevatedButton(plaine, on_click=tp,bgcolor='green',)],
            ),
            alignment=ft.Alignment.BOTTOM_LEFT,
            padding=30,   
        ),
    ],expand=True)

    def retourneur(e):
        page.clean()
        navigate("planet")

    return planet