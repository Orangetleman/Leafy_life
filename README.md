

# 🍃 Leafy Life : Echoes of the Pond

Leafy Life est un jeu vidéo éducatif original créé pour les Trophées NSI 2026. Explorez des biomes, gérez vos ressources et apprenez à protéger la biodiversité à travers une expérience ludique et immersive.

## 🚀 Démarrage Rapide

### Installation automatique (Recommandé)
Lancez simplement le fichier `dependencies.bat`. 
- Il vérifiera si Python est installé (et vous guidera vers le Store si besoin).
- Il installera les bibliothèques nécessaires (`flet`, `pyglet`, `pynput`).
- Il lancera le jeu automatiquement.

### Installation manuelle
Si vous préférez le faire à la main :
1. Installez les dépendances : `pip install -r requirements.txt`
2. Lancez le jeu : `python main.py`

## 🕹️ Commandes et Utilisation
- **Navigation :** Utilisez la barre de menu pour basculer entre la Planète, l'Inventaire et le Shop.
- **Interactions :** Utilisez la touche **[Espace]** pour interagir avec les PNJ et les objets sur la carte. Utiliser les touches **[d,flèche_droite]** pour aller à droite et **[a,q,flèche_gauche]** pour aller à gauche.
- **Objectif :** Collectez des ressources (O2/CO2), gérez vos "Leafs" et progressez dans l'histoire en affrontant des ennemis ou en commerçant dans le shop itinérant.
- **Système SEED :** La fonction _seed_test_data() permet d'obtenir des ressources illimitées normalement innaccessible à un vrai joueurs. La fonction permet de mettre de jeu en mode "développeur".

## 🛠️ Diagnostic et Résolutions (Bugs connus)
Bien que le projet soit opérationnel, deux comportements mineurs liés à l'interface Flet et à la gestion du rafraîchissement graphique sur certaines configurations peuvent survenir. Voici comment les résoudre :

### 🪳 Problème n°1 : Latence d'actualisation des dialogues (Lore)
Lors des séquences de narration, il peut arriver que l'interface visuelle ne se mette pas à jour immédiatement. Ce phénomène est dû à l'encapsulation profonde de certaines fonctions asynchrones qui peut parfois retarder le rafraîchissement de la page.

**✅ Solution :** Il suffit de provoquer un événement de redimensionnement manuel pour forcer Flet à recalculer le rendu. Pour cela, déplacez légèrement la fenêtre, changez sa taille ou passez en mode plein écran.

### 🪳 Problème n°2 : Blocage de l'affichage après la vidéo d'introduction
Sur certaines machines, la transition entre le lecteur vidéo et le lancement du moteur de jeu peut laisser l'écran noir ou figé sur un début de chargement.

**✅ Solution :** Ce bug est lié à l'initialisation du mode plein écran automatique. Pour débloquer l'affichage, activez manuellement le mode plein écran via le bouton standard situé en haut à droite de la fenêtre de l'application.


## 📂 Organisation du code
Le projet est structuré de manière modulaire pour faciliter la lecture et la maintenance :
- `main.py` : Point d'entrée gérant la navigation globale et l'initialisation de l'application.
- `datacenter.py` : Le "cerveau" technique. Il centralise toutes les données (stats des Leafs, items, dialogues) via des structures de dictionnaires imbriqués complexes.
- `style.py` : Design system centralisé (couleurs, polices, styles d'UI) fonctionnant comme une feuille de style CSS pour l'ensemble du projet.
- `planetHome.py` : Gestion du monde ouvert, du moteur de déplacement et du système d'interaction temps réel.
- `inventoryHome.py & leafsHome.py` : Modules gérant l'affichage dynamique de vos possessions et de vos créatures.
- `tuto.py` : Guide visuel et pédagogique pour accompagner les nouveaux joueurs.

## ⚖️ Licence
Ce projet est sous licence libre **GPL v3+**.