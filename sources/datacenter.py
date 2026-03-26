import random
import asyncio
import math

# ————————————————————————————————————————————————————————————————————————————————————————
# ————————————————————————————————————— DATA PALETTE —————————————————————————————————————
# ————————————————————————————————————————————————————————————————————————————————————————

# ------------------------------------ Enemies palette -----------------------------------
# reward : { "currency": "O2"|"CO2", "amount": int }
# lvl    : niveau approximatif de l'ennemi (indicateur de difficulté)
ENEMIES = [
    {
        "id": 1, "name": "Crabe", "rarity": "common",
        "atk": 35, "hp": 80,
        "biome": ["lake"], "lvl": 1,
        "visual": "assets/imgs/npc/crab.png",
        "met": False, "prez": "Le crabe chinois (Eriocheir sinensis) est un crabe fouisseur de la famille des varunidae. Il se nourrit essentiellement d’algues et de petits crustacés. Il est la proie de mammifères, d’oiseaux, et de poissons. Il possède deux pinces pour se défendre.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 2, "name": "Ours", "rarity": "common",
        "atk": 25, "hp": 100,
        "biome": ["mountain"], "lvl": 1,
        "visual": "assets/imgs/npc/bear.png",
        "met": False, "prez": " L’ours brun (Ursus arctos) est un mammifère omnivore de la famille des ursidés. Il utilise l’intimidation pour se défendre, et possède de grandes griffes. Il se nourrit de tout, des poissons jusqu’aux élans, mais surtout des végétaux. Etant un superprédateur, seuls certains grands carnivores osent l’attaquer.",
        "reward": {"currency": "CO2", "amount": 50},
    },
    {
        "id": 3, "name": "Serpent", "rarity": "rare",
        "atk": 20, "hp": 80,
        "biome": ["mountain"], "lvl": 3,
        "visual": "assets/imgs/npc/snake.png",
        "met": False, "prez": "La vipère aspic (Vipera aspis) est un serpent de la famille des viperidae, endémique d’Europe. Elle utilise du venin pour se défendre. Elle est la proie de certains oiseaux, de sangliers, de blaireaux, de renards et de mustélidés. Elle chasse des micromammifères et plus rarement des lézards et petits oiseaux.",
        "reward": {"currency": "O2", "amount": 18},
    },
    {
        "id": 4, "name": "rien", "rarity": "common",
        "atk": 5, "hp": 20,
        "biome": ["plain"], "lvl": 1,
        "visual": "assets/imgs/items/rien.png",
        "met": False, "prez": "Un crabe minuscule, mais ses pinces font mal.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 5, "name": "rien", "rarity": "common",
        "atk": 12, "hp": 40,
        "biome": ["forest"], "lvl": 1,
        "visual": "assets/imgs/items/rien.png",
        "met": False, "prez": "Un crabe minuscule, mais ses pinces font mal.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 6, "name": "rien", "rarity": "common",
        "atk": 3, "hp": 10,
        "biome": ["mountain"], "lvl": 1,
        "visual": "assets/imgs/items/rien.png",
        "met": False, "prez": "Un crabe minuscule, mais ses pinces font mal.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 7, "name": "rien", "rarity": "common",
        "atk": 3, "hp": 10,
        "biome": ["lake"], "lvl": 1,
        "visual": "assets/imgs/items/rien.png",
        "met": False, "prez": "Un crabe minuscule, mais ses pinces font mal.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 8, "name": "Champignon", "rarity": "common",
        "atk": 12, "hp": 40,
        "biome": ["forest"], "lvl": 1,
        "visual": "assets/imgs/npc/mushroom.png",
        "met": False, "prez": " L’amanite tue-mouche (Amanita muscaria) est un champignon mortel et psychotrope. Il produit des toxines violentes pour se protéger de ses prédateurs, généralement des cervidés.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 9, "name": "Mante religieuse", "rarity": "common",
        "atk": 6, "hp": 25,
        "biome": ["plain"], "lvl": 1,
        "visual": "assets/imgs/npc/mantis.png",
        "met": False, "prez": "La mante religieuse (Mantis religiosa) est un insecte de la famille des mantidae originaire du bassin méditerranéen. Si son intimidation ne fonctionne pas, elle peut mordre pour se défendre des oiseaux et reptiles. Elle se nourrit de petits insectes vivants, en mouvement, qu’elle chasse.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 10, "name": "Guepe", "rarity": "common",
        "atk": 8, "hp": 18,
        "biome": ["plain"], "lvl": 1,
        "visual": "assets/imgs/npc/wasp.png",
        "met": False, "prez": "La guêpe commune (Vespula vulgaris) est un insecte de la famille des vespinae originaire d’Eurasie. Elle dispose d’un dard pour se défendre contre les oiseaux, les chauves-souris, les amphibiens et insectes carnivores. Elle se nourrit de substances sucrées, et attaque les abeilles pour leur territoire.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 11, "name": "Ronces", "rarity": "common",
        "atk": 15, "hp": 50,
        "biome": ["forest"], "lvl": 1,
        "visual": "assets/imgs/npc/thorns.png",
        "met": False, "prez": "La ronce commune (Rubus fruticosus) est une plante à fleur de la famille des rosacées. Elle possède des aiguillons pour se protéger des chèvres et cervidés, et produit des fruits appelés mûres pour se multiplier très rapidement. Elle est considérée comme de la mauvaise-herbe.",
        "reward": {"currency": "O2", "amount": 8},
    },


    #LORE ENEMIES
    {
        "id": 12, "name": "Crabefaible", "rarity": "common",
        "atk": 3, "hp": 10,
        "biome": ["plain"], "lvl": 1,
        "visual": "assets/imgs/npc/crabfaible.png",
        "met": False, "prez": "Un crabe minuscule, mais ses pinces font mal.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 13, "name": "Heron", "rarity": "common",
        "atk": 50, "hp": 1000,
        "biome": ["lake"], "lvl": 1,
        "visual": "assets/imgs/npc/BigBadHeron.png",
        "met": False, "prez": "tie finito chef",
        "reward": {"currency": "O2", "amount": 1000},
    },
    {
        "id": 14, "name": "OursGrand", "rarity": "common",
        "atk": 20, "hp": 500,
        "biome": ["mountain"], "lvl": 1,
        "visual": "assets/imgs/npc/bigbear.png",
        "met": True, "prez": "Un ours.",
        "reward": {"currency": "CO2", "amount": 50},
    },
]

# ------------------------------------ Npcs palette --------------------------------------
NPCS = [
    { "id": 1, "name": "Heron", "biome": "lake", "visual": "assets/imgs/npc/heron.png","met": False, "prez": "Le héron cendré (Ardea cinerea) est un oiseau échassier de la famille des ardeidae. Il vit en colonie et sa taille est son meilleur atout. Il se nourrit essentiellement de poissons mais peu s’adapter au besoin. Il n’a pas de vrai prédateur, bien qu’il soit la victime de certains grands rapaces."},
    { "id": 2, "name": "Cat", "biome": "plain", "visual": "assets/imgs/npc/cat.png","met": False, "prez": " Le chat domestiqué (Felis catus) est un mammifère ccarnivore de l’ordre des félins. Il possède une excellente vision nocturne, des griffes et des dents pointues. Il se nourrit de viande, venant d’oiseaux, de petits rongeurs et de poissons. Ses prédateurs sont les rapaces, et les grands mustélidés tels que les blaireaux."},
    { "id": 7, "name": "chamois", "biome": "mountain", "visual": "assets/imgs/npc/chamois.png","met": False, "prez": "Le chamois (Rupicapra rupicapra) est un bovidé vivant dans les zones rocheuses, forêts et pâturages de montagne. Ils possèdent de petites cornes noires leur permettant de se défendre ainsi qu’une très bonne vision pour repérer ses prédateurs. Il est la proie des loups, lynx, ours, aigles royaux et parfois des grands corbeaux et se nourri exclusivement d’herbes et de graines."},
    { "id": 9, "name": "spider", "biome": "forest", "visual": "assets/imgs/npc/spider.png","met": False, "prez": "La saltique chevronné (Salticus scenicus) ou araignée sauteuse, est un insecte de la famille des salticidae. Pour attaquer ses proies, généralement de petits insectes vivants, elle approche discrètement et leur saute dessus pour les immobiliser avec son venin. Elle est chassée par les oiseaux et d’autres insectes."},

    { "id": 3, "name": "rien", "biome": "plain", "visual": "assets/imgs/items/rien.png"},
    { "id": 4, "name": "rien", "biome": "forest", "visual": "assets/imgs/items/rien.png"},
    { "id": 5, "name": "rien", "biome": "mountain", "visual": "assets/imgs/items/rien.png"},
    { "id": 6, "name": "rien", "biome": "lake", "visual": "assets/imgs/items/rien.png"},
    
    { "id": 8, "name": "criquet", "biome": "plain", "visual": "assets/imgs/npc/criquet.png","met": False, "prez": " Le criquet migrateur (Locusta migratoria) est un insecte orthoptère de la famille des acrididae. C’est un insecte ravageur dans de nombreuses régions tropicales. Il se nourri principalement de graines, il est chassé par des oiseaux comme les rapaces ou la volaille, des insectes comme les mantes religieuses, ou encore des reptiles et amphibiens. Il utilise généralement le camouflage pour se défendre."},
]

# ------------------------------------ Objects palette -----------------------------------
OBJECTS = [
    { "id": 1, "name": "flaque", "visual": "assets/imgs/icons/flaque.png",    "gives": "Eau minérale"},
    { "id": 2, "name": "herbe",   "visual": "assets/imgs/items/grass.png", "gives": "Herbe"},
    { "id": 3, "name": "rien", "visual": "assets/imgs/items/rien.png", "gives": "rien"},
]

# ------------------------------------ Events palette ------------------------------------
# EVENTS_WEIGHTS : probabilités relatives (normalisées automatiquement)
# "lore" est retiré de la liste dès que tous les lore ont été vus
EVENTS = [
    "enemy",
    "npc",
    "empty",
    "lore",
]

EVENTS_WEIGHTS = {
    "enemy": 0.40,   # 40 % de chance de tomber sur un ennemi
    "npc":   0.15,   # 15 % de chance de tomber sur un marchand
    "empty": 0.35,   # 35 % de chance de tomber sur un objet
    "lore":  0.10,   # 10 % pour un événement lore (retiré quand terminé)
}


def choose_event():
    """Tirage pondéré parmi les événements disponibles."""
    available = EVENTS[:]
    weights   = [EVENTS_WEIGHTS.get(e, 0.1) for e in available]
    return random.choices(available, weights=weights, k=1)[0]


# ------------------------------------ Items palette ------------------------------------
ITEMS = {
    # ── Animaux (O2) ────────────────────────────────────────────────────────────────────
    3: {
        "id": 3, "name": "Viande", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 40},
        "price_O2": 45, "specialprice_O2": 22, "is_special": False,
        "icon": "assets/imgs/items/meat.png",
        "tags": ["meat", "growth", "nouriture"],
        "description": "Riche en protéines et en énergie, cette viande est essentielle au métabolisme des leafs carnivores.",
        "species": ["animal"], "regime": ["carnivore"],
    },
    4: {
        "id": 4, "name": "Herbe", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 35},
        "price_O2": 25, "specialprice_O2": 12, "is_special": False,
        "icon": "assets/imgs/items/grass.png",
        "tags": ["grass", "growth", "nouriture"],
        "description": "Cette herbe fraîche fournit fibres et nutriments de base aux leafs herbivores.",
        "species": ["animal"], "regime": ["herbivore"],
    },
    6: {
        "id": 6, "name": "Bandage", "category": "soin",
        "effect": {"stat": "hp", "amount": 12},
        "price_O2": 35, "specialprice_O2": 18, "is_special": False,
        "icon": "assets/imgs/items/bandage.png",
        "tags": ["bandage", "soin", "regeneration"],
        "description": "Conçu pour stabiliser les tissus, ce bandage favorise une cicatrisation rapide chez les leafs animaux.",
        "species": ["animal"],
    },
    8: {
        "id": 8, "name": "Lait 🌟", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 50},
        "price_O2": 55, "is_special": True, "rarity": 0.4,
        "icon": "assets/imgs/items/milk.png",
        "tags": ["milk", "nutrients", "nouriture", "special"],
        "description": "Riche en calcium, le lait booste durablement les nutriments des leafs animaux.",
        "species": ["animal"],
    },
    # ── Plantes (CO2) ────────────────────────────────────────────────────────────────────
    2: {
        "id": 2, "name": "Fertilisant", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 35},
        "price_CO2": 25, "specialprice_CO2": 12, "is_special": False,
        "icon": "assets/imgs/items/fertilizer.png",
        "tags": ["fertilizer", "growth", "nouriture"],
        "description": "Ce fertilisant enrichit le sol et stimule la photosynthèse des leafs plantes.",
        "species": ["plant"],
    },
    5: {
        "id": 5, "name": "Sève", "category": "soin",
        "effect": {"stat": "hp", "amount": 12},
        "price_CO2": 35, "specialprice_CO2": 18, "is_special": False,
        "icon": "assets/imgs/items/seve.png",
        "tags": ["seve", "soin", "regeneration"],
        "description": "Cette sève régénératrice restaure les tissus végétaux.",
        "species": ["plant"],
    },
    9: {
        "id": 9, "name": "Poudre d'os 🌟", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 50},
        "price_CO2": 55, "is_special": True, "rarity": 0.4,
        "icon": "assets/imgs/items/bone_meal.png",
        "tags": ["bone_meal", "growth", "nouriture", "special"],
        "description": "Riche en phosphore, cette poudre booste durablement les nutriments des leafs plantes.",
        "species": ["plant"],
    },
    # ── Universels (O2 + CO2) ────────────────────────────────────────────────────────────
    1: {
        "id": 1, "name": "Eau minérale", "category": "boisson",
        "effect": {"stat": "hydration", "amount": 30},
        "price_O2": 3, "price_CO2": 3, "specialprice_O2": 1, "specialprice_CO2": 1, "is_special": False,
        "icon": "assets/imgs/items/water.png",
        "tags": ["water", "hydration", "boisson"],
        "description": "Indispensable à toute forme de vie, l'eau minérale maintient l'équilibre vital de tous les leafs.",
    },
    7: {
        "id": 7, "name": "Rayon de soleil", "category": "revitaliseur",
        "effect": {"stat": "hp", "amount": 8},
        "price_O2": 80, "price_CO2": 80, "specialprice_O2": 40, "specialprice_CO2": 40, "is_special": False,
        "icon": "assets/imgs/items/sunshine.png",
        "tags": ["sunshine", "revitaliseur"],
        "description": "Concentré d'énergie solaire, ce rayon peut ramener un leaf au seuil de la vie.",
    },
    10: {
        "id": 10, "name": "Elixir de vie 🌟", "category": "revitaliseur",
        "effect": {"stat": "hp", "amount": 30},
        "price_O2": 180, "price_CO2": 180, "is_special": True, "rarity": 0.3,
        "icon": "assets/imgs/items/elixir.png",
        "tags": ["elixir_of_life", "revitaliseur", "special"],
        "description": "Cet élixir agit directement sur les mécanismes vitaux et défie le cycle naturel de la vie.",
    },
    11: {
        "id": 11, "name": "Potion d'attaque 🌟", "category": "boost",
        "effect": {"stat": "atk", "amount": 5},
        "price_O2": 85, "price_CO2": 85, "is_special": True, "rarity": 0.35,
        "icon": "assets/imgs/items/attack_boost.png",
        "tags": ["attack_boost", "boost", "special"],
        "description": "Booste temporairement l'attaque pour toute la durée d'un combat.",
    },
    12: {
        "id": 12, "name": "Potion de vie 🌟", "category": "boost",
        "effect": {"stat": "hp", "amount": 15},
        "price_O2": 80, "price_CO2": 80, "is_special": True, "rarity": 0.35,
        "icon": "assets/imgs/items/health_boost.png",
        "tags": ["health_boost", "boost", "special"],
        "description": "Augmente durablement le maximum de points de vie d'un leaf.",
    },
    13: {
        "id": 13, "name": "Livre de la connaissance 🌟", "category": "boost",
        "effect": {"stat": "level", "amount": 5},
        "price_O2": 150, "price_CO2": 150, "is_special": True, "rarity": 0.3,
        "icon": "assets/imgs/items/book_of_knowledge.png",
        "tags": ["book_of_knowledge", "boost", "special"],
        "description": "Ce livre ancien augmente les capacités et la sagesse des leafs.",
    },
}

TYPES = [
    { "id": 1, "name": "nouriture",    "icon": "assets/imgs/icons/type_food.png" },
    { "id": 2, "name": "soin",         "icon": "assets/imgs/icons/type_heal.png" },
    { "id": 3, "name": "boisson",      "icon": "assets/imgs/icons/type_beverage.png" },
    { "id": 4, "name": "revitaliseur", "icon": "assets/imgs/icons/type_resurrector.png" },
]

# ------------------------------------ Leafs palette ------------------------------------
LEAFS = {
    2:  { "id": 2,  "name": "mouton",    "type": 2, "rarity": "default", "atk": 2, "hp": 40,  "species": "animal", "regime": "herbivore", "biome": 1, "level": 0, "img": "assets/imgs/leafs/Leaf_sheep.png",      "xp": 0, "met": False, "prez":"Le mouton (Ovis aries) est un mammifère herbivore ruminant des caprinés bovidés. Chassé par les canidés et notamment le loup gris, il vit en troupeau et préfère la fuite bien qu’il puisse charger pour se défendre. Son régime alimentaire est essentiellement composé d’herbe et de graines." },
    3:  { "id": 3,  "name": "abeille",   "type": 2, "rarity": "default", "atk": 3, "hp": 40,  "species": "animal", "regime": "herbivore", "biome": 1, "level": 0, "img": "assets/imgs/leafs/Leaf_bee.png",        "xp": 0, "met": False, "prez":"L’abeille européennee (Apis mellifera) est connu pour sa capacité à produire du miel. Organisée en colonie dans une ruche, la reine est la seule à pouvoir pondre des œufs. Les abeilles se défendent en utilisant un dard. Elles se nourrissent de fleurs, et sont chassées par les guêpes et frelons ainsi que de nombreux oiseaux insectivores et certains batraciens. Les abeilles communiquent entre elles par des mouvements !" },
    5:  { "id": 5,  "name": "loup",      "type": 1, "rarity": "default", "atk": 6, "hp": 20,  "species": "animal", "regime": "carnivore", "biome": 2, "level": 0, "img": "assets/imgs/leafs/Leaf_wolf.png",       "xp": 0, "met": False, "prez":"Le loup gris (Canis Lupus) fait parti de la famille des canidés, et est un carnivore. Il se nourrit de grands herbivores comme les cerfs, de rongeurs, d’oiseaux et parfois de carcasses. Le loup est un superprédateur et est en haut de la chaîne alimentaire et n’a donc aucun prédateur naturel. Il a une morsure puissante, peut courir et nager, et a une ouïe très développée. C’est un animal territorial et social vivant en meute." },
    8:  { "id": 8,  "name": "poisson",   "type": 1, "rarity": "default", "atk": 5, "hp": 40,  "species": "animal", "regime": "herbivore", "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_fish.png",       "xp": 0, "met": False, "prez":"Le poisson rouge ou carassin doré (Carassius auratus) est un poisson d’eau douce vivant en banc. Il est omnivore à tendance insectivore et détritivore, et est la proie des poissons-pêcheurs, des serpents aquatiques ainsi que de certains batraciens. Les femelles fécondées pondent des œufs pour se reproduire." },
    9:  { "id": 9,  "name": "chèvre",    "type": 3, "rarity": "default", "atk": 2, "hp": 100, "species": "animal", "regime": "herbivore", "biome": 4, "level": 0, "img": "assets/imgs/leafs/Leaf_goat.png",       "xp": 0, "met": False, "prez":"La chèvre domestique (Capra hircus) est un mammifère herbivore ruminant de la famille des bovidés. Elle se nourrit essentiellement de mauvaise-herbe, et a pour prédateurs les renards, les chiens errants ainsi que les loups. Pour se défendre, elles peuvent utiliser leurs cornes, ou bien leur agilité pour grimper dans les arbres hors de la portée de leurs prédateurs." },
    12: { "id": 12, "name": "aigle",     "type": 1, "rarity": "default", "atk": 4, "hp": 60,  "species": "animal", "regime": "carnivore", "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_eagle.png",      "xp": 0, "met": False, "prez":" L’aigle royal (Aquila chrysaetos) est un rapace de la famille des accipitridae. Il utilise sa grande vitesse, son agilité et ses puissantes serres pour attraper ses proies, telles que des lapins, des marmottes, des écureuils et même des renards ainsi que des chèvres. Il pond des œufs et protège son vaste territoire. Considéré comme un superprédateur, seul le grand corbeau s’attaque à ses petits." },
    13: { "id": 13, "name": "trefle",    "type": 3, "rarity": "default", "atk": 7, "hp": 120, "species": "plant", "biome": 4, "level": 0, "img": "assets/imgs/leafs/Leaf_clover.png",       "xp": 0, "met": False, "prez":" Le trèfle rampant (Trifolium repens) est souvent considéré comme de la mauvaise-herbe, et sert de nourriture pour les ovins, bovins et certains cervidés. C’est une plante vivace dont les tiges peuvent atteindre 40 cm. Le trèfle produit des fleurs et des fruits et se développe très rapidement. Il peut être utilisé dans la médecine et n’est dangereux ni pour les humains ni pour les animaux domestiques." },
    1:  { "id": 1,  "name": "pissenlit", "type": 1, "rarity": "default", "atk": 5, "hp": 40,  "species": "plant",  "biome": 1, "level": 0, "img": "assets/imgs/leafs/Leaf_dandelion.png",   "xp": 0, "met": False, "prez":"Le pissenlit commun (Taraxacum rubicuncum) est une plante à fleur de la famille des asteraceae. Il se multiplie très rapidement et est considéré comme de la mauvaise herbe. Il sert de nourriture aux insectes pollinisateurs comme les abeilles, et aux mammifères herbivores ainsi qu’à certains oiseaux granivores." },
    4:  { "id": 4,  "name": "sapin",     "type": 3, "rarity": "default", "atk": 3, "hp": 80,  "species": "plant",  "biome": 2, "level": 0, "img": "assets/imgs/leafs/Leaf_pine.png",        "xp": 0, "met": False, "prez":" Le sapin commun (Abies alba) est une espèce de conifère de la famille des pinacées, et est originaire d’Europe. Il produit des cônes appelés pomme de pin dans le but que les animaux puissent les disperser, semant ainsi leurs graines pour se dupliquer. Il peut être la cible de coléoptères, qui creusent des galeries dans son tronc, entrainant la mort de l’arbre." },
    6:  { "id": 6,  "name": "fraisier",  "type": 2, "rarity": "default", "atk": 3, "hp": 60,  "species": "plant",  "biome": 2, "level": 0, "img": "assets/imgs/leafs/Leaf_strawberry.png",  "xp": 0, "met": False, "prez":" Le framboisier (Rubus idaeus) est une plante à fleur de la famille des rosacées. C’est une plante dressée produisant des fruits, les framboises, qui sont consommées par de nombreux insectes, tels que par exemple les papillons, les chenilles et les pucerons. Cela lui permet de disperser ses graines et donc de se multiplier." },
    7:  { "id": 7,  "name": "roseaux",   "type": 3, "rarity": "default", "atk": 3, "hp": 80,  "species": "plant",  "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_reeds.png",       "xp": 0, "met": False, "prez":" La massette à feuilles étroites (Typha angustifolia) plus connue sous le nom de roseau est une plante herbacée de la famille des typhaceae. Il se développe généralement proche de l’eau, et produit jusqu’à 300 000 graines par macettes, lui permettant ainsi de se multiplier très rapidement. Il n’a pas de réel prédateur, bien que certains insectes l’attaque et que les humains se servent de lui dans l’industrie du textile." },
    10: { "id": 10, "name": "arbuste",   "type": 3, "rarity": "default", "atk": 1, "hp": 120, "species": "plant",  "biome": 4, "level": 0, "img": "assets/imgs/leafs/Leaf_bush.png",        "xp": 0, "met": False, "prez":"Le genévrier commun (Juniperus communis) est un arbuste de la famille des cupressacés. Il se protège grâce à ses feuilles qui ont une forme d’aiguille. Il est utilisé par les humains dans la cuisine et la médecine, et n’a pas de prédateurs directs même si certains insectes se servent de lui pour survivre." },
    11: { "id": 11, "name": "lotus", "type": 2, "rarity": "default", "atk": 1, "hp": 40,  "species": "plant",  "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_lilypad.png",     "xp": 0, "met": False, "prez":"Le lotus sacré (Nelumbo nucifera) est une plante aquatique d’eau douce à fleurs de la famille des Nélumbonacées, et est originaire d’Eurasie. Sa fleur immergée est récoltée depuis plusieurs milliers d’années dans un but médical, alimentaire ou ornemental. Certains rongeurs se nourrissent de ses racines ou tiges, provoquant ainsi la mort de la plante." },
}

LEAFS_TYPE = [
    { "id": 0, "name": "default",  "icon": "assets/imgs/icons/leaf_type_default.png"  },
    { "id": 1, "name": "attacker", "icon": "assets/imgs/icons/leaf_type_attacker.png" },
    { "id": 2, "name": "healer",   "icon": "assets/imgs/icons/leaf_type_healer.png"   },
    { "id": 3, "name": "tank",     "icon": "assets/imgs/icons/leaf_type_tank.png"     },
]

BIOMES = [
    { "id": 1, "name": "plain",    "icon": "assets/imgs/biomes/arriere_plain.png"    },
    { "id": 2, "name": "forest",   "icon": "assets/imgs/biomes/arriere_forest.png"   },
    { "id": 3, "name": "lake",     "icon": "assets/imgs/biomes/arriere_lake.png"     },
    { "id": 4, "name": "mountain", "icon": "assets/imgs/biomes/arriere_mountain.png" },
]

PLANETS = [
    { "id": 1, "name": "Earth", "biomes": [BIOMES[0], BIOMES[1], BIOMES[2], BIOMES[3]] }
]

# ————————————————————————————————————————————————————————————————————————————————————————
# ————————————————————————————————————— DATA MANAGER —————————————————————————————————————
# ————————————————————————————————————————————————————————————————————————————————————————

class LeafStat:
    # ── Constantes de classe ──────────────────────────────────────────────────────────────
    CURRENCY_PRODUCED = {"animal": "CO2", "plant": "O2"}
    # Consommation par tick : nutrients -1, hydration -2 (rapport 1:2)
    TICK_CONSUMPTION  = {"nutrients": 1, "hydration": 2}

    def __init__(self, leaf):
        self.id        = leaf["id"]
        self.name      = leaf["name"]
        self.type      = leaf["type"]
        self.rarity    = leaf["rarity"]
        self.atk       = leaf["atk"]
        self.hp        = leaf["hp"]
        self.species   = leaf["species"]
        self.biome     = leaf["biome"]
        self.level     = leaf["level"]
        self.img       = leaf["img"]
        self.nutrients = 100
        self.hydration = 100
        self.regime    = leaf.get("regime", None)
        self.xp        = leaf["xp"]
        self.hp_max    = leaf["hp"]
        self.atk_max   = leaf["atk"]
        # Valeurs de base immuables — toujours utilisées comme référence pour le scaling.
        # Ne jamais modifier atk_base/hp_base après __init__.
        self.atk_base  = leaf["atk"]
        self.hp_base   = leaf["hp"]

        # ── Boosts ───────────────────────────────────────────────────────────────────────
        self.atk_boost       = 0   # temporaire (reset après combat)
        self.hp_boost        = 0   # permanent  (max hp supplémentaire)
        self.nutrients_boost = 0   # permanent  (nutriments bonus)

        # Plafonds des boosts : moitié du max de base
        self.HP_BOOST_MAX        = max(1, self.hp_max // 2)
        self.NUTRIENTS_BOOST_MAX = 50
        self.ATK_BOOST_MAX       = max(1, self.atk_max // 2)

        # ── Production en attente ────────────────────────────────────────────────────────
        self.pending_currency = 0.0

        # ── Limites max par stat ──────────────────────────────────────────────────────────
        self.STAT_MAX = {
            "hp":        self.hp_max,
            "nutrients": 100,
            "hydration": 100,
            "atk":       self.atk_max,
            "level":     100,
        }

    # ── Mise à jour classique (clampée) ──────────────────────────────────────────────────
    def stat_update(self, stat: str, amount: int):
        if not hasattr(self, stat):
            print(f"Stat '{stat}' inexistante pour {self.name}.")
            return
        current = getattr(self, stat)
        max_val = self.STAT_MAX.get(stat, 9999)
        new_val = max(0, min(current + amount, max_val))
        setattr(self, stat, new_val)
        print(f"{self.name} - {stat} : {current} -> {new_val}")

    # ── Scaling de niveau via ln(x+1)/sqrt(x+1) ────────────────────────────────────────────
    def calculate_atk_from_level(self):
        if self.level <= 0:
            return self.atk_base
        total = self.atk_base
        for lvl in range(1, self.level + 1):
            total += self.atk_base * (math.log(lvl + 1) / math.sqrt(lvl + 1)) * 0.12
        return int(total)

    def calculate_hp_from_level(self):
        if self.level <= 0:
            return self.hp_base
        total = self.hp_base
        for lvl in range(1, self.level + 1):
            total += self.hp_base * (math.log(lvl + 1) / math.sqrt(lvl + 1)) * 0.20
        return int(total)

    # ── Application d'un item ─────────────────────────────────────────────────────────────
    def apply_item(self, item: dict):
        """
        - Items spéciaux nutrients/hp : remplit la base d'abord, puis le boost (capped).
        - Items spéciaux atk           : boost temporaire (capped à ATK_BOOST_MAX).
        - Autres items                 : stat_update classique.
        """
        stat     = item["effect"]["stat"]
        amount   = item["effect"]["amount"]
        special  = item.get("is_special", False)

        if special and stat in ("nutrients", "hp"):
            base_max   = self.STAT_MAX[stat]
            current    = getattr(self, stat)
            boost_attr = f"{stat}_boost"
            boost_max  = getattr(self, f"{stat.upper()}_BOOST_MAX", 0)
            
            # 1. Remplir la base d'abord
            fill      = min(amount, max(0, base_max - current))
            setattr(self, stat, current + fill)
            remaining = amount - fill
            
            # 2. Le surplus va dans le boost
            if remaining > 0:
                cur_boost = getattr(self, boost_attr, 0)
                setattr(self, boost_attr, min(cur_boost + remaining, boost_max))
            print(f"{self.name} - {stat} boost : +{amount} (base +{fill}, boost +{remaining})")

        elif special and stat == "atk":
            old = self.atk_boost
            self.atk_boost = min(self.atk_boost + amount, self.ATK_BOOST_MAX)
            print(f"{self.name} - atk_boost : {old} -> {self.atk_boost}")

        elif special and stat == "level":
            self.stat_update(stat, amount)
            new_atk = self.calculate_atk_from_level()
            new_hp  = self.calculate_hp_from_level()
            self.atk     = new_atk
            self.atk_max = new_atk
            self.hp_max  = new_hp
            self.STAT_MAX["atk"] = new_atk
            self.STAT_MAX["hp"]  = new_hp
            self.HP_BOOST_MAX    = max(1, new_hp  // 2)
            self.ATK_BOOST_MAX   = max(1, new_atk // 2)
            print(f"{self.name} - atk : {self.atk} | hp_max : {self.hp_max}")

        else:
            self.stat_update(stat, amount)

    # ── Reset des boosts temporaires (fin de combat) ─────────────────────────────────────
    def reset_combat_boosts(self):
        self.atk_boost = 0

    # ── Tick de gestion ───────────────────────────────────────────────────────────────────
    def tick(self):
        if self.hp <= 0:
            return
        for stat, need in self.TICK_CONSUMPTION.items():
            boost_attr = f"{stat}_boost"
            cur_boost  = getattr(self, boost_attr, 0)
            if cur_boost >= need:
                setattr(self, boost_attr, cur_boost - need)
            else:
                remaining = need - cur_boost
                setattr(self, boost_attr, 0)
                cur_base = getattr(self, stat)
                setattr(self, stat, max(0, cur_base - remaining))

        # Production
        nut_base_ratio  = self.nutrients / 100.0
        nut_boost_ratio = self.nutrients_boost / self.NUTRIENTS_BOOST_MAX
        hyd_ratio       = self.hydration / 100.0
        ratio = ((nut_base_ratio + hyd_ratio) / 2.0 + (nut_boost_ratio * 0.5))*2.5
        self.pending_currency += ratio

    # ── Récolte ───────────────────────────────────────────────────────────────────────────
    def harvest(self):
        amount = int(self.pending_currency)
        if amount <= 0:
            return None, 0
        self.pending_currency -= amount
        currency = self.CURRENCY_PRODUCED[self.species]
        inventory_manager.append_money(currency, amount)
        print(f"{self.name} - récolte : {amount} {currency}")
        return currency, amount


class LeafManager:
    def __init__(self):
        self.owned = []

    def add_leaf(self, leaf):
        if any(l.id == leaf["id"] for l in self.owned):
            print(f"{leaf['name']} est déjà dans votre collection.")
            return
        self.owned.append(LeafStat(leaf))
        print(f"{leaf['name']} ajouté à votre collection !")
    
    def harvest_all(self, specie:str="plant"):
        for leaf in self.owned:
            if leaf.species == specie:
                leaf.harvest()


class InventoryManager:
    def __init__(self):
        self.items = []
        self.money = {"O2": 0, "CO2": 0}

    def append_item(self, item, amount=1):
        existing = next((i for i in self.items if i["id"] == item["id"]), None)
        if existing:
            existing["amount"] += amount
        else:
            self.items.append({**item, "amount": amount})

    def append_money(self, currency, amount):
        if currency in self.money:
            self.money[currency] += amount

    def remove_item(self, item_id, amount=1):
        for i, item in enumerate(self.items):
            if item["id"] == item_id:
                item["amount"] -= amount
                if item["amount"] <= 0:
                    return self.items.pop(i)
        return None

    def remove_money(self, currency, amount):
        if currency not in self.money:
            return False
        if self.money[currency] >= amount:
            self.money[currency] -= amount
            return True
        return False

    def is_item_in_inventory(self, item_id):
        return any(i["id"] == item_id for i in self.items)

    def is_enough_money(self, item):
        needs_O2  = (item.get("price_O2")  or 0) > 0
        needs_CO2 = (item.get("price_CO2") or 0) > 0
        if needs_O2 and needs_CO2:
            return self.money["O2"] >= item["price_O2"] and self.money["CO2"] >= item["price_CO2"]
        if needs_O2:
            return self.money["O2"]  >= item["price_O2"]
        if needs_CO2:
            return self.money["CO2"] >= item["price_CO2"]
        return True

    def get_items(self): return self.items
    def get_money(self): return self.money


class ShopManager:
    def __init__(self, biome=None, type_str=None):
        self.type  = type_str or "classic"
        self.biome = biome or BIOMES[0]
        self.stock = get_classic_shop_items() if self.type == "classic" else get_wandering_shop_items(self.biome)

    def reload_wandering_shop_items(self):
        if self.type == "wandering":
            self.stock = get_wandering_shop_items(self.biome)

    def is_item_in_stock(self, item_id, amount=1):
        return any(i["id"] == item_id and i["amount"] >= amount for i in self.stock)

    def remove_item_from_stock(self, item_id, amount=1):
        for item in self.stock:
            if item["id"] == item_id:
                if item["amount"] >= amount:
                    item["amount"] -= amount
                    return True
                return False
        return False

    def buy_item(self, item, amount=1):
        if not inventory_manager.is_enough_money(item):
            return {"success": False, "error": "insufficient_funds"}
        if not self.is_item_in_stock(item["id"], amount):
            return {"success": False, "error": "out_of_stock"}
        if item.get("price_O2", 0) > 0:
            if not inventory_manager.remove_money("O2", item["price_O2"] * amount):
                return {"success": False, "error": "payment_failed"}
        if item.get("price_CO2", 0) > 0:
            if not inventory_manager.remove_money("CO2", item["price_CO2"] * amount):
                if item.get("price_O2", 0) > 0:
                    inventory_manager.append_money("O2", item["price_O2"] * amount)
                return {"success": False, "error": "insufficient_funds"}
        inventory_manager.append_item(item, amount)
        self.remove_item_from_stock(item["id"], amount)
        return {"success": True}


def get_classic_shop_items():
    return [{**item, "amount": float("inf")} for item in ITEMS.values() if not item["is_special"]]

def get_wandering_shop_items(biome):
    specials    = [{**i, "amount": 50} for i in ITEMS.values() if i["is_special"] and roll(i["rarity"])]
    non_special = [i for i in ITEMS.values() if not i["is_special"]]
    random.shuffle(non_special)
    discounted = [
        {**i,
        # Priorité au prix soldé, sinon prix normal, sinon 0.
        # Le `or` natif échoue si specialprice vaut None (item sans ce champ)
        # car None or None retourne None au lieu de 0, ce qui casse buy_item.
        "price_O2":  i.get("specialprice_O2") or i.get("price_O2")  or 0,
        "price_CO2": i.get("specialprice_CO2") or i.get("price_CO2") or 0,
        "amount": 50}
        for i in non_special[:2]
    ]
    return specials + discounted

def roll(chance):
    return random.random() < chance


# ── Instances globales ───────────────────────────────────────────────────────────────────
leafmanager       = LeafManager()
inventory_manager = InventoryManager()
classic_shop_manager = ShopManager()

wandering_shop_manager_plain    = ShopManager(PLANETS[0]["biomes"][0], "wandering")
wandering_shop_manager_forest   = ShopManager(PLANETS[0]["biomes"][1], "wandering")
wandering_shop_manager_lake     = ShopManager(PLANETS[0]["biomes"][2], "wandering")
wandering_shop_manager_mountain = ShopManager(PLANETS[0]["biomes"][3], "wandering")

WANDERINGSHOPS = [
    {"id": 0, "shop": wandering_shop_manager_plain,    "biome": "plain"},
    {"id": 1, "shop": wandering_shop_manager_forest,   "biome": "forest"},
    {"id": 2, "shop": wandering_shop_manager_lake,     "biome": "lake"},
    {"id": 3, "shop": wandering_shop_manager_mountain, "biome": "mountain"},
]


# ————————————————————————————————————————————————————————————————————————————————————————
# ———————————————————————————————————— GAME CLOCK ————————————————————————————————————————
# ————————————————————————————————————————————————————————————————————————————————————————

class GameClock:
    TICK_INTERVAL = 30.0

    def __init__(self):
        self.running   = False
        self.callbacks = []

    def add_callback(self, fn):
        self.callbacks.append(fn)

    async def _loop(self):
        while self.running:
            await asyncio.sleep(self.TICK_INTERVAL)
            for leaf in leafmanager.owned:
                leaf.tick()
            for cb in self.callbacks:
                try:
                    cb()
                except Exception as e:
                    print(f"GameClock callback error: {e}")

    def start(self, page):
        self.running = True
        page.run_task(self._loop)
        print(f"GameClock démarrée (tick toutes les {self.TICK_INTERVAL}s)")

    def stop(self):
        self.running = False
        print("GameClock arrêtée")


game_clock = GameClock()


from pygame import mixer

class MusicManager:
    def __init__(self):
        mixer.init()

    def play(self, path: str, loop: bool = True):
        mixer.music.load(path)
        mixer.music.set_volume(0.5)
        mixer.music.play(-1 if loop else 0)

    def stop(self):
        mixer.music.stop()

music = MusicManager()


# ── Dialogues ────────────────────────────────────────────────────────────────────────────
victoire = ["bravo! vous avez vaicu l'ennemi!"]

s1 = ["Tiens, un pissenlit...", 
        "Bonsoir! Je ne t'ai encore jamais vu dans ces plaines, tu es nouveau?", 
        "Bonjour, oui, je m'appelle Froggy", 
        "Un voyageur ! C'est rare par ici! Quelle est ta destination ?", 
        "Je voyage pour trouver un point d'eau pour mes oeufs, tu sais où je peux en trouver un ?", 
        "Il n'y en a pas d'appropriés par ici, mais tu en trouveras peut etre un dans la forêt!", 
        "Où est elle?",
        "Pas très loin, je pense.",
        "Tu penses?",
        "Je ne me suis jamais aventuré très loin, à cause de tous les voisins aggressifs... Je peux peut être t'accompagner!",
        "Si soudainement?",
        "Je vais te protéger des locaux, et je souhaite voir le monde au delà de ma motte de terre!",
        "Eh bien, si t'insistes, je ne suis pas contre un peu de compagnie pour la route.",
        ]
s2 = ["Que fais un crabe ici, loin de son habitat naturel?",
        "Qui va là?","Bonjour, je ne suis qu'un simple voyageur, savez vous où -", 
        "Pas un pas de plus! Revenez d'où vous venez, je n'ai pas d'affaires à faire avec ceux qui ralentissent ma mission.", 
        "Vous ne semblais pas en très bonne santé.", 
        "Cela ne vous regarde pas!",
        "Un crabe sans eau ne survivra pas longtemps.",
        "Partez !",
        "Une mission, vous dites? Dans cet état? Prenez cette gourde d'eau au moins -", 
        "ASSEZ!"
        ]
s3 = ["[Un criquet est coincé sous une touffe d'herbe aplatie par le vent.]",
        "Hé. Hé ! Là-dessous !",
        "Qui est là?",
        "Je suis bloqué depuis ce matin. Tu peux soulever ça ?",
        "[soulève]",
        "Ah. Merci.",
        "[pars]",
        "Tu vas à la forêt ?",
        "Oui.",
        "Moi j'essaie d'y aller depuis trois jours mais j'arrive pas à traverser le terrain sec au milieu. Je me dessèche...Je peux venir avec toi ?",
        "[aquiese]",
        "Merci beaucoup! Je te guiderais jusqu'aux bois, promis !",
        ]
s4 = ["(Un nuage dans l'herbe...)",
        "Oh. Une grenouille. On voit pas souvent ça par ici.",
        "(C'est la première fois que je vois un mouton...)",
        "T'as l'air de chercher quelque chose.",
        "La forêt.",
        "[regarde vers le nord] La forêt? C'est par là. Les herbes deviennent plus sombres, tu peux pas rater.",
        "[suis le regard]",
        "Moi j'y vais jamais. Trop de racines sous les pattes. Mais bon, Charlie m'a répété pleins de fois que si je voulais que les femelles me regardent un jour, il fallait que je me salisse les sabots."
        ]
s5 = ["(quel est ce bourdonnement ?)",
      "Halte ! Que faites vous si près de la reine?",
      "Je ne fais que passer",
      "Comment etes vous arrivés si près? Mes frères ont dû vous arrêter avant.",
      "Non, vous êtes la première abeille que je vois.",
      "Etrange. Si vous ne voulez vraiment aucun mal, il n'y a pas d'inconvénient à ce que je vous surveille quelques temps, n'est-ce pas?",
      "(Le pissenlit sera content, je suppose)"
      ]
s6 = ["(Un trèfle à quatres feuilles... Il parait que ça porte chance. J'en aurai surement besoin.)"]
s7 = ["Nous y sommes.",
      "C'est... grand. Je savais pas que c'était aussi grand.",
      "Ca te fais peur?",
      "...je vais rester là un petit instant, avance sans moi",
      "Tu es sûr?",
      "Oui, merci d'avoir voyagé avec moi jusqu'ici, je ne t'oublierai jamais, promis!",
      "Alors, c'est ici qu'on se dit au-revoir, Criquet... Tu vas me manquer...",
      "Bonne chance pour la suite !",
      "(Moi aussi je ne t'oublierai jamais, ami.)"
      ]
s8 = ["(La forêt, enfin... mais je ne vois pas de point d'eau. Il y a t'il quelqu'un à qui demander?)",
      "Besoin d'aide?",
      "(C'est vraiment calme ici, comparé à la plaine)",
      "Bonjouuuuur !!!",
      "(Hmm, je trouverai peut-être quelqu'un si je m'avance un peu...)",
      "EH OH NE ME MARCHEZ PAS DESSUS !!",
      "[sursaute]",
      "Vous pourriez faire attention où vous marchez au moins ?",
      "Escusez moi.",
      "Ce n'est pas grave. Je suis Saltique, la manageuse en chef de toute la communication web de la forêt.",
      "(La mana- quoi?) Je suis Froggy, enchanté.",
      "Mince, on m'appelle. Je dois filer.",
      "(Je crois que je commence à comprendre.)",
      "N'hésite pas à venir me voir si tu as besoin de quoi que ce soit. Moi et mes soeurs feront tout notre possible pour que tu passes un merveilleux séjour dans le Bois de l'Ombre Verte!",
      "Attendez, je voulais vous demand...er. Elle est partie. En bondissant. Très bien, ce bois promet d'être intéressant."
      ]
s9 = ["(Une fraise parfaitement mûre. Le rouge éclatant fait le charme des forêts.)"]
s10 = ["[Mouton tremble]",
       "[ignore]",
       "Bonjour, toi.",
       "Tu n'as pas peur de moi?",
       "Pourquoi un louveteau s'attaquerait à une grenouille?",
       "Je ne sais pas, ma meute dit que tous les animeaux de cette forêt nous craignent, et que c'est pour cela qu'on n'en vois pas beaucoup sur notre territoire",
       "Ca doit être pour ça que je ne croise personne...",
       "Je dois retourner vers ma meute, mais ne t'inquetes pas, je leur dirait que tu es un ami qui ne fait que passer!"
       ]
s11 = ["(Plus je m'avance, plus les arbres sont immenses...)","[vent soufle]","[saute sur une branche et admire le paysage]","Je peux t'emmener regarder la canopée, si tu le souhaite."]
s12 = ["(Ce n'est pas le louveteau de tout à l'heure? Il a l'air triste...)",
       "La grenouille ! Ca me fait plaisir de te voir à nouveau.",
       "Quelque chose ne va pas?",
       "[sanglote] Mon frère a ramené une immense proie qu'il a chassé avec son groupe d'amis, et mes parents et l'alpha ne parlent que de lui depuis...",
       "Tu te sens délaissé?",
       "Oui...",
       "J'ai rencontré quelques ennemis redoutables pendant mon voyage. Si on en térasse un ensemble, tu pourras le ramener à ta meute et tu sera couvert de bien plus de gloire que ton frère et sa proie.",
       "Oui ! Tu as raison ! Vous aussi, vous êtes mon proupe d'amis après tout!"
       ]
s13 = ["[peine à avancer dans les broussailles]",
       "[s'accroche à son menteau]",
       "[continue d'avancer, arrachant une des branches]"]
s14 = ["Vas y petit loup, c'est ta chance de briller !",
       "QUI OSE ENTRER SUR MON TERRITOIRE?"]
s15 = ["Bonjour, savez vous où je peux trouver un point d'eau?",
       "Il  y a un grand lac après cette montagne.",
       "Merci beauc- [glisse]",
       "Vous allez bien?",
       "[se relève] Oui, oui, merci, j'ai juste glissé un peu rien de grave.",
       "Une grenouille qui gravit une montagne, on en voit pas tous les jours.",
       "J'en gravirai cent si c'est pour que mes enfants grandissent dans les meilleures conditions!",
       "J'ai de la peine pour vous, laissez moi au moins vous porter jusqu'au lac, j'y allais également de toute façon"]
s16 = ["[marche]",
       "[fais des cercles au-dessus, dans le ciel]",
       "[se sent mal à l'aise]",
       "[plonge]",
       "(c'est la fin...)",
       "Aie ! Pourquoi le protèges tu, Chèvre?",
       "[lève la tête, apperçoit la chèvre au dessus de lui, bloquant l'attaque de l'aigle]",
       "Depuis quand une grenouille a une armée pour traverser la montagne?",
       "(il s'est blessé en heurtant la chèvre...), je peux soigner cette plaie si tu promets de ne plus m'attaquer.",
       "[confus] Si t'y tiens tant, je n'ai aucune raison de refuser..."]
s17 = ["[époustoufflé]",
       "Nous y sommes, Froggy, le grand lac des Eaux Tranquilles!",
       "Enfin... c'est tellement beau...",
       "Hehe, un choc, pas vrai? Ca m'a fait le même effet la première fois que je l'ai vu aussi.",
       "Ne perdons pas de temps, et allons y tout de suite !"]
s18 = ["Chercheons un endroit tranquille et abrité d'abord.",
       "On peut longer la rive, juqu'à trouver le parfait endroit.",
       "Oui, bonne idée.",
       "[observe le sac de Froggy] Les oeufs ont l'air de vouloir éclore d'ici peu.",
       "[souris]"
       ]
s19 = ["[saute sur un nénuphar près de la rive]",
       "Pour qui vous prenez vous, monsieur la grenouille ?!",
       "[bondis de nouveau, surpris]",
       "C'est sur la princesse lotus que vous venez de poser vos pattes vertes!",
       "Excuseez moi, majesté, je suis nouveau ici.",
       "Cela explique la présence d'une grenouille ici, à découvert",
       "Que voulez vous dire par là?",
       "[attentive] restez près de moi, j'entends quelque chose arriver."]
s20 = ["[attentif]",
       "C'est moi ! Ne vous inquetez pas !",
       "[soulagement général]",
       "Mais je n'apporte pas de bonnes nouvelles. Le Héron est revenu de sa promenade !",
       "[tressaille]",
       "Suivez moi, je vais vous cacher pas loin."]
s21 = ["L'Héron, droit devant !",
       "[se retourne]",
       "[tout le monde se fige]",
       "[s'envole]",
       "(Quoi?)"]
s22 = ["(Pourquoi continuons nous de courir? Le héron ne vient il pas de s'envoler?)",
       "C'est son cousin. Il a honte de sa tyrannie, mais a trop peur pour s'y opposer. Il nous vends des babioles pour nous aider en secret"]
s23 = ["[cours]",
       "Par ici! Je vais vous cacher!"]
s24 = ["On y est presqu-",
       "[se pose devant tout le monde] Presque, où?",
       "(C'est lui. C'est lui qui a dévoré ma femme sous mes yeux. Jamais je n'oublierai cet oiseau. Il va me payer pour tout ce qu'il a fait, ce tyran !)"]

LORE = [{'dialogue':s1, 'visual':"assets/imgs/leafs/Leaf_dandelion.png", 'combat':False, "add":1,    "entity":"leaf", "biome":"plain"},
        {'dialogue':s2, 'visual':"assets/imgs/npc/crabfaible.png",       'combat':True,  "add":None, "entity":"nmi",  "biome":"plain"},
        {'dialogue':s3, 'visual':"assets/imgs/npc/criquet.png",          'combat':False, "add":None, "entity":"npc",  "biome":"plain"},
        {'dialogue':s4, 'visual':"assets/imgs/leafs/Leaf_sheep.png",     'combat':False, "add":2,    "entity":"leaf", "biome":"plain"},
        {'dialogue':s5, 'visual':"assets/imgs/leafs/Leaf_bee.png",       'combat':False, "add":3,    "entity":"leaf", "biome":"plain"},
        {'dialogue':s6, 'visual':"assets/imgs/leafs/Leaf_clover.png",    'combat':False, "add":13,   "entity":"leaf", "biome":"plain"},
        {'dialogue':s7, 'visual':"assets/imgs/npc/criquet.png",          'combat':False, "add":None, "entity":"npc",  "biome":"plain"},

        # foret

        {'dialogue':s8, 'visual':"assets/imgs/npc/spider.png",          'combat':False, "add":None, "entity":"npc",  "biome":"forest"},
        {'dialogue':s9, 'visual':"assets/imgs/leafs/Leaf_strawberry.png",    'combat':False, "add":6,   "entity":"leaf", "biome":"forest"},
        {'dialogue':s10, 'visual':"assets/imgs/leafs/Leaf_wolf.png",    'combat':False, "add":None,   "entity":"leaf", "biome":"forest"},
        {'dialogue':s11, 'visual':"assets/imgs/leafs/Leaf_pine.png",    'combat':False, "add":4,   "entity":"leaf", "biome":"forest"},
        {'dialogue':s12, 'visual':"assets/imgs/leafs/Leaf_wolf.png",    'combat':False, "add":5,   "entity":"leaf", "biome":"forest"},

        # montagne

        {'dialogue':s13, 'visual':"assets/imgs/leafs/Leaf_bush.png",    'combat':False, "add":10,   "entity":"leaf", "biome":"mountain"},
        {'dialogue':s14, 'visual':"assets/imgs/npc/bigbear.png",       'combat':True,  "add":None, "entity":"nmi", "biome":"mountain"},
        {'dialogue':s15, 'visual':"assets/imgs/leafs/Leaf_goat.png",    'combat':False, "add":9,   "entity":"leaf", "biome":"mountain"},
        {'dialogue':s16, 'visual':"assets/imgs/leafs/Leaf_eagle.png",    'combat':False, "add":12,   "entity":"leaf", "biome":"mountain"},
        {'dialogue':s17, 'visual':"assets/imgs/leafs/Leaf_goat.png",    'combat':False, "add":None,   "entity":"leaf", "biome":"mountain"},

        # lac

        {'dialogue':s18, 'visual':"assets/imgs/leafs/Leaf_dandelion.png", 'combat':False, "add":None,    "entity":"leaf", "biome":"lake"},
        {'dialogue':s19, 'visual':"assets/imgs/leafs/Leaf_lilypad.png", 'combat':False, "add":11,    "entity":"leaf", "biome":"lake"},
        {'dialogue':s20, 'visual':"assets/imgs/leafs/Leaf_fish.png", 'combat':False, "add":8,    "entity":"leaf", "biome":"lake"},
        {'dialogue':s21, 'visual':"assets/imgs/npc/heron.png",          'combat':False, "add":None, "entity":"npc",  "biome":"lake"},
        {'dialogue':s22, 'visual':"assets/imgs/leafs/Leaf_fish.png", 'combat':False, "add":None,    "entity":"leaf", "biome":"lake"},
        {'dialogue':s23, 'visual':"assets/imgs/leafs/Leaf_reeds.png", 'combat':False, "add":7,    "entity":"leaf", "biome":"lake"},
        {'dialogue':s24, 'visual':"assets/imgs/leafs/BigBadHeron.png", 'combat':True, "add":None,    "entity":"leaf", "biome":"lake"},
        ]






