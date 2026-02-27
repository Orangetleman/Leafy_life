from os import name
# ------------------------------------------------------------------------
# ----------------------------- DATA PALETTE -----------------------------
# ------------------------------------------------------------------------

# Enemies palette
ENEMIES = [
    { "id": 1, "name": "Chardon", "type": "tank", "rarity": "common", "atk": 3, "hp": 10, "biome": ["plain"], "lvl": 2},
]

# Events palette
EVENTS = {
    "plain": [
        { "type": "enemy", "data": { "enemyId": 1 } },
        { "type": "npc", "data": { "npcId": 1 } },
        { "type": "lore", "data": { "leafId": 1 } },
    ]
}

# Items palette
ITEMS = {
    # Consomables Leafs Mobs (O2):
        # Normaux :
    3: { "id": 3, "name": "Meat", "use": "food", "price_O2": 64, "specialprice_O2": 32, "is_special": False, "icon": "assets/imgs/items/meat.png",
        "tags" : ["meat", "growth", "food"],
        "description": "Riche en protéines et en énergie, cette viande est essentielle au métabolisme des leafs carnivores. Elle soutient leur croissance et leur endurance." },
    4: { "id": 4, "name": "Grass", "use": "food", "price_O2": 32, "specialprice_O2": 16, "is_special": False, "icon": "assets/imgs/items/grass.png",
        "tags" : ["grass", "growth", "food"],
        "description": "Cette herbe fraîche fournit fibres et nutriments de base aux leafs herbivores. Un apport simple mais vital à leur équilibre digestif." },
    6: { "id": 6, "name": "Bandage", "use": "heal", "price_O2": 100, "specialprice_O2": 50, "is_special": False, "icon": "assets/imgs/items/bandage.png",
        "tags" : ["bandage", "heal", "regeneration"],
        "description": "Conçu pour stabiliser les tissus et limiter les pertes d’énergie, ce bandage favorise une cicatrisation rapide chez les leafs animaux." },

        # Spéciaux :
    8: { "id": 8, "name": "Milk 🌟", "use": "food", "price_O2": 64, "is_special": True, "rarity": 1, "icon": "assets/imgs/items/milk.png",
        "tags" : ["milk", "nutrients", "food", "special"],
        "description": "Riche en calcium et en nutriments essentiels, le lait renforce la structure et la vitalité des leafs animaux. Une ressource rare à forte valeur biologique." },

    # Consomables Leafs Plantes (CO2): */
        # Normaux :
    2: { "id": 2, "name": "Fertilizer", "use": "food", "price_CO2": 32, "specialprice_CO2": 16, "is_special": False, "icon": "assets/imgs/items/fertilizer.png",
        "tags" : ["fertilizer", "growth", "food"],
        "description": "Ce fertilisant enrichit le sol en éléments nutritifs et stimule la photosynthèse des leafs plantes. Indispensable à leur développement." },
    5: { "id": 5, "name": "Mineral Water", "use": "heal", "price_CO2": 100, "specialprice_CO2": 50, "is_special": False, "icon": "assets/imgs/items/mineral_water.png",
        "tags" : ["mineral_water", "heal", "regeneration"],
        "description": "Chargée en minéraux essentiels, cette eau restaure les tissus végétaux et aide les leafs plantes à se régénérer durablement." },

        # Spéciaux :
    9: { "id": 9, "name": "Bone Meal 🌟", "use": "food", "price_O2": 64, "is_special": True, "rarity": 1, "icon": "assets/imgs/items/bone_meal.png",
        "tags" : ["bone_meal", "growth", "food", "special"],
        "description": "Riche en phosphore et en calcium, cette poudre stimule fortement la croissance des leafs plantes. Un engrais puissant issu de matières anciennes." },

    # Consomables Leafs Plantes et Mobs (O2 + CO2): */
        # Normaux :
    1: { "id": 1, "name": "H2O", "use": "beverage", "price_O2": 4, "price_CO2": 4, "specialprice_O2": 2, "specialprice_CO2": 2, "is_special": False, "icon": "assets/imgs/items/water.png",
        "tags" : ["water", "hydration", "beverage"],
        "description": "Molécule indispensable à toute forme de vie, l’eau régule les échanges internes et maintient l’équilibre vital de tous les leafs." },
    7: { "id": 7, "name": "Ray of sunshine", "use": "resurrector", "price_O2": 200, "price_CO2": 200, "specialprice_O2": 100, "specialprice_CO2": 100, "is_special": False, "icon": "assets/imgs/items/sunshine.png",
        "tags" : ["sunshine", "resurrector"],
        "description": "Concentré d’énergie solaire, ce rayon relance les processus vitaux et peut ramener un leaf au seuil de la vie." },

        # Spéciaux :
    10: { "id": 10, "name": "Elixir of life 🌟", "use": "resurrector", "price_O2": 300, "price_CO2": 300, "is_special": True, "rarity": 1, "icon": "assets/imgs/items/elixir.png",
        "tags" : ["elixir_of_life", "resurrector", "special"],
        "description": "Composé d’essences rares et hautement énergétiques, cet élixir agit directement sur les mécanismes vitaux et défie le cycle naturel de la vie." },
    11: { "id": 11 , "name": "Attack boost potion 🌟", "use": "boost", "price_O2": 100, "price_CO2": 100, "is_special": True, "rarity": 1, "icon": "assets/imgs/items/attack_boost.png",
        "tags" : ["attack_boost", "boost", "special"],
        "description": "Cette potion spéciale augmente temporairement la puissance d’attaque des leafs, leur conférant un avantage stratégique en combat." },
    12: { "id": 12, "name": "Health boost potion 🌟", "use": "boost", "price_O2": 100, "price_CO2": 100, "is_special": True, "rarity": 1, "icon": "assets/imgs/items/health_boost.png",
        "tags" : ["health_boost", "boost", "special"],
        "description": "Cette potion spéciale augmente temporairement les points de vie des leafs, renforçant leur endurance face aux défis environnementaux." },
    13: {"id": 13, "name": "Book of knowledge 🌟", "use": "boost", "price_O2": 150, "price_CO2": 150, "is_special": True, "rarity": 1, "icon": "assets/imgs/items/book_of_knowledge.png",
        "tags" : ["book_of_knowledge", "boost", "special"],
        "description": "Ce livre ancien renferme des savoirs oubliés qui, une fois assimilés, augmentent les capacités et la sagesse des leafs." }
}
TYPES = [
    { 'id': 1, 'name': "food", 'icon': "assets/imgs/icons/type_food.png" },
    { 'id': 2, 'name': "heal", 'icon': "assets/imgs/icons/type_heal.png" },
    { 'id': 3, 'name': "beverage", 'icon': "assets/imgs/icons/type_beverage.png" },
    { 'id': 4, 'name': "resurrector", 'icon': "assets/imgs/icons/type_resurrector.png" }
]

# Leafs palette
LEAFS = {
    # id, name, type, rarity, atk, hp, species, regime (if animal), biome, competence_lvl, img

    # Animals
    0: { 'id': 0, 'name': "grenouille", 'type': 0, 'rarity': "default", 'atk': 4, 'hp': 5, 'species': "animal", 'regime': "carnivore", 'biome': 1, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_frog.png" },
    2: { 'id': 2, 'name': "mouton", 'type' : 2, 'rarity': "default", 'atk': 2, 'hp': 4, 'species': "animal", 'regime':"herbivore", 'biome': 1, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_sheep.png" },
    3: { 'id': 3, 'name': "abeille", 'type' : 2, 'rarity': "default", 'atk': 3, 'hp': 4, 'species': "animal", 'regime':"herbivore", 'biome': 1, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_bee.png" },
    5: { 'id': 5, 'name' :"loup", 'type' :1 , 'rarity':"default", 'atk': 6, 'hp': 2, 'species':"animal", 'regime':"carnivore", 'biome': 2, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_wolf.png"},
    8: { 'id': 8, 'name': "poisson", 'type' : 1, 'rarity': "default", 'atk': 5, 'hp': 4, 'species': "animal", 'regime':"herbivore", 'biome': 3, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_fish.png" },
    9: { 'id': 9, 'name': "chèvre", 'type' :3 , 'rarity': "default", 'atk': 2, 'hp': 10, 'species':"animal", 'regime':"herbivore", 'biome': 4, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_goat.png" },
    12: { 'id': 12, 'name': "aigle", 'type' : 1, 'rarity': "default", 'atk': 4, 'hp': 6, 'species': "animal", 'regime':"carnivore", 'biome':3 , 'competence_lvl':0 , 'img':"assets/imgs/leafs/Leaf_eagle.png" },
    13: { 'id': 13, 'name': "ours", 'type' :3 , 'rarity':"default" , 'atk':7 , 'hp':12 , 'species':"animal" , 'regime':"carnivore" , 'biome':4 , 'competence_lvl':0 , 'img':"assets/imgs/leafs/Leaf_bear.png" },
    # Plants
    1: { 'id': 1, 'name': "pissenlit", 'type' : 1, 'rarity': "default", 'atk': 5, 'hp': 4, 'species': "plant", 'biome': 1, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_dandelion.png" },
    4: { 'id': 4, 'name':"sapin", 'type' : 3 , 'rarity':"default", 'atk': 3, 'hp': 8, 'species':"plant", 'biome': 2, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_pine.png"},
    6: { 'id': 6, 'name': "fraisier", 'type' : 2, 'rarity': "default", 'atk': 3, 'hp': 6, 'species': "plant", 'biome': 2, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_strawberry.png" },
    7: { 'id': 7, 'name': "roseaux", 'type' : 3, 'rarity': "default", 'atk': 3, 'hp': 8, 'species': "plant", 'biome': 3, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_reeds.png" },
    10: { 'id': 10, 'name':"arbuste", 'type' :3 , 'rarity':"default", 'atk': 1, 'hp': 12, 'species':"plant", 'biome': 4, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_bush.png" },
    11: { 'id': 11, 'name': "nénuphare", 'type' : 2, 'rarity': "default", 'atk': 1, 'hp': 4, 'species': "plant", 'biome': 3, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_lilypad.png" },
}

LEAFS_TYPE = [
    { 'id': 0, 'name': "default", 'icon': "assets/imgs/icons/leaf_type_default.png" },
    { 'id': 1, 'name': "attacker", 'icon': "assets/imgs/icons/leaf_type_attacker.png" },
    { 'id': 2, 'name': "healer", 'icon': "assets/imgs/icons/leaf_type_healer.png" },
    { 'id': 3, 'name': "tank", 'icon': "assets/imgs/icons/leaf_type_tank.png" }
]

# Biomes palette
BIOMES = [
    {'id': 1, 'name': "plain", 'icon': "assets/imgs/icons/biome_plain.png"},
    {'id': 2, 'name': "forest", 'icon': "assets/imgs/icons/biome_forest.png"},
    {'id': 3, 'name': "lake", 'icon': "assets/imgs/icons/biome_lake.png"},
    {'id': 4, 'name': "mountain", 'icon': "assets/imgs/icons/biome_mountain.png"}
]
PLANETS = [
    { 'id': 1, 'name': "Earth", 'biomes': [BIOMES[0], BIOMES[1], BIOMES[2], BIOMES[3]] }
]

# ----------------------------------------------------------------------------------------
# ------------------------------------- DATA MANAGER -------------------------------------
# ----------------------------------------------------------------------------------------


class LeafManager:
    def __init__(self, owned = []):
        self.owned = owned

    def add_leaf(self,leaf):
        is_owned = False
        for leafs in self.owned:
            if leafs["id"] == leaf["id"]:
                print(leaf["name"] + " est déjà un de vos leafs.")
                is_owned = True
        if not is_owned:
            self.owned.append(leaf)
            print(leaf["name"] + " fais maintenant parti de vos leafs !")

leafmanager = LeafManager()

