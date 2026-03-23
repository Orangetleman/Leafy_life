📄 Dossier de Présentation : Leafy Life (Version Complète)
🌿 1. Présentation globale
La genèse du projet :
Leafy Life n'est pas un simple exercice scolaire. Au sein de notre équipe, nous avons une politique immuable : transformer chaque projet en jeu vidéo. Pourquoi ? D'abord pour amuser l'évaluateur (le jury), mais surtout pour nous motiver à transformer des lignes de code en une expérience créative et concrète. Pour l'édition 2026, nous avons voulu adapter le thème "NATURE" en un univers vivant.

Problématique et Objectifs :
Comment faire comprendre la nature et ses enjeux à travers un moment agréable ? La réponse a été le jeu éducatif. Notre but : une "éducation subtile mais durable". Le joueur progresse, s'amuse, et sans s'en rendre compte, il assimile des connaissances sur la biodiversité et l'équilibre écologique (gestion de l'O2 et du CO2).

👥 2. L'équipe et l'organisation
Le cœur du projet est porté par un duo de meilleurs amis de la classe de NSI, habitués à entreprendre ensemble.

De ALMEIDA Christophe (Développeur) : Pilier technique. Il a programmé le main.py, LeafsHome.py, ShopHome.py, InventoryHome.py, Datacenter.py, Style.py, et a réalisé une grande partie de la première version en JavaScript. Il a une expertise particulière sur la structuration des données (dictionnaires, tableaux) et l'organisation du code.

PERLES Eva (Développeuse & Chef de projet) : Management, communication et rédaction des fichiers techniques. En programmation, elle a co-développé PlanetHome.py et le Datacenter.py. Elle s'est spécialisée sur l'utilisation des modules, l'implémentation des assets (images, sons), le scénario et la logique métier du jeu.

Contributeurs précieux : Louis Vandevoorde (Musique), Augustin Louis (Scénario et Graphisme), Emka (Graphisme).

Répartition des tâches :
Bien que Christophe ait été le moteur de la structure globale, Eva a géré toute la cohérence du projet et le lien avec le scénario. La répartition s'est faite naturellement selon les forces : Christophe sur l'algorithmique pure et Eva sur l'intégration logique et visuelle.

Temps passé (Estimation) :

Développeurs : 1 mois complet, avec des sessions quotidiennes allant de 2h à 7h de codage.

Artistes : Une semaine pour Emka, et environ 10h pour Augustin et Louis.

📅 3. Étapes du projet (Chronologie)
Décembre – Janvier : Pré-inscription et réflexion. Création du concept "Leafy Life". Développement d'une première version (l'épave) en JavaScript, HTML et CSS sur VS Code.

Février : Composition des musiques originales. Pivot majeur : Nous découvrons que les langages Web ne sont pas autorisés comme cœur de projet.

Fin Février : Transfert massif du code de JavaScript vers Python. Prise en main du module Flet en un temps record pour sauver le projet.

Mars : Poursuite de la programmation Python, production des assets graphiques finaux et implémentation du scénario.

Fin Mars : Tests complets (réalisés notamment par le petit frère pour traquer les bugs d'ergonomie), finitions et dépôt.

🛠️ 4. Validation et Choix Techniques
Le défi du transfert Web -> Python :
Pour passer du modèle Web au modèle Python sans tout perdre, nous avons conservé une structure modulaire :

Données : Le dossier "data" est devenu datacenter.py (gestion des palettes de données).

Design : Le fichier global.css est devenu style.py (centralisation des couleurs et des styles).

Affichage : Le dossier "screens" a été divisé en modules (leafsHome.py, shopHome.py, etc.).
Choix du module : Nous avons abandonné Pygame à cause de ses limitations pour créer des interfaces modernes. Nous avons choisi Flet car c'est la solution qui se rapprochait le plus d'un codage Web, nous permettant de ne pas perdre de temps dans l'apprentissage d'un support totalement différent.

Expertise Algorithmique :
Plutôt que d'utiliser du SQL, nous avons créé un système de gestion de données complexe en Python pur. Les dictionnaires imbriqués dans datacenter.py permettent de gérer les récompenses (reward), les types de biomes et les dialogues dynamiques. Le jeu gère également le placement adaptatif des objets pour s'assurer que l'expérience reste fluide peu importe la taille de la fenêtre.

🚀 5. Ouverture
Leafy Life s'inscrit dans une démarche durable de création. À l'avenir, nous pourrions :

Décliner ce moteur pour d'autres enjeux sociétaux (santé, social, etc).

Et pour leafy Life en lui même : Ajouter de nouveaux biomes, développer l'histoire et enrichir le contenu (nouveaux items, compétences et Leafs).