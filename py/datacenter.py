import random
from os import name
# ————————————————————————————————————————————————————————————————————————————————————————
# ————————————————————————————————————— DATA PALETTE —————————————————————————————————————
# ————————————————————————————————————————————————————————————————————————————————————————

# ------------------------------------ Enemies palette -----------------------------------
ENEMIES = [
    { "id": 1, "name": "Chardon", "type": "tank", "rarity": "common", "atk": 3, "hp": 10, "biome": ["plain"], "lvl": 2, "visual" : "23112025-IMG_0402.jpg"},
]

# ------------------------------------ Events palette ------------------------------------
EVENTS = {
    "plain": [
        { "type": "enemy", "data": { "enemyId": 1 } },
        { "type": "npc", "data": { "npcId": 1 } },
        { "type": "lore", "data": { "leafId": 1 } },
    ]
}

# ------------------------------------ Items palette ------------------------------------
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

# ------------------------------------ Leafs palette ------------------------------------
LEAFS = {
    # id, name, type, rarity, atk, hp, species, regime (if animal), biome, competence_lvl, img

    # Animals
    0: { 'id': 0, 'name': "grenouille", 'type': 0, 'rarity': "default", 'atk': 4, 'hp': 5, 'species': "animal", 'regime': "carnivore", 'biome': 1, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_frog.png", 'xp': 10},
    2: { 'id': 2, 'name': "mouton", 'type' : 2, 'rarity': "default", 'atk': 2, 'hp': 4, 'species': "animal", 'regime':"herbivore", 'biome': 1, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_sheep.png", 'xp': 0 },
    3: { 'id': 3, 'name': "abeille", 'type' : 2, 'rarity': "default", 'atk': 3, 'hp': 4, 'species': "animal", 'regime':"herbivore", 'biome': 1, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_bee.png", 'xp': 0 },
    5: { 'id': 5, 'name' :"loup", 'type' :1 , 'rarity':"default", 'atk': 6, 'hp': 2, 'species':"animal", 'regime':"carnivore", 'biome': 2, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_wolf.png", 'xp': 0},
    8: { 'id': 8, 'name': "poisson", 'type' : 1, 'rarity': "default", 'atk': 5, 'hp': 4, 'species': "animal", 'regime':"herbivore", 'biome': 3, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_fish.png", 'xp': 0 },
    9: { 'id': 9, 'name': "chèvre", 'type' :3 , 'rarity': "default", 'atk': 2, 'hp': 10, 'species':"animal", 'regime':"herbivore", 'biome': 4, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_goat.png", 'xp': 0 },
    12: { 'id': 12, 'name': "aigle", 'type' : 1, 'rarity': "default", 'atk': 4, 'hp': 6, 'species': "animal", 'regime':"carnivore", 'biome':3 , 'competence_lvl':0 , 'img':"assets/imgs/leafs/Leaf_eagle.png", 'xp': 0 },
    13: { 'id': 13, 'name': "ours", 'type' :3 , 'rarity':"default" , 'atk':7 , 'hp':12 , 'species':"animal" , 'regime':"carnivore" , 'biome':4 , 'competence_lvl':0 , 'img':"assets/imgs/leafs/Leaf_bear.png", 'xp': 0 },
    # Plants
    1: { 'id': 1, 'name': "pissenlit", 'type' : 1, 'rarity': "default", 'atk': 5, 'hp': 4, 'species': "plant", 'biome': 1, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_dandelion.png", 'xp': 0 },
    4: { 'id': 4, 'name':"sapin", 'type' : 3 , 'rarity':"default", 'atk': 3, 'hp': 8, 'species':"plant", 'biome': 2, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_pine.png", 'xp': 0},
    6: { 'id': 6, 'name': "fraisier", 'type' : 2, 'rarity': "default", 'atk': 3, 'hp': 6, 'species': "plant", 'biome': 2, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_strawberry.png", 'xp': 0 },
    7: { 'id': 7, 'name': "roseaux", 'type' : 3, 'rarity': "default", 'atk': 3, 'hp': 8, 'species': "plant", 'biome': 3, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_reeds.png", 'xp': 0 },
    10: { 'id': 10, 'name':"arbuste", 'type' :3 , 'rarity':"default", 'atk': 1, 'hp': 12, 'species':"plant", 'biome': 4, 'competence_lvl': 0, 'img':"assets/imgs/leafs/Leaf_bush.png", 'xp': 0 },
    11: { 'id': 11, 'name': "nénuphare", 'type' : 2, 'rarity': "default", 'atk': 1, 'hp': 4, 'species': "plant", 'biome': 3, 'competence_lvl': 0, 'img': "assets/imgs/leafs/Leaf_lilypad.png", 'xp': 0 },
}

LEAFS_TYPE = [
    { 'id': 0, 'name': "default", 'icon': "assets/imgs/icons/leaf_type_default.png" },
    { 'id': 1, 'name': "attacker", 'icon': "assets/imgs/icons/leaf_type_attacker.png" },
    { 'id': 2, 'name': "healer", 'icon': "assets/imgs/icons/leaf_type_healer.png" },
    { 'id': 3, 'name': "tank", 'icon': "assets/imgs/icons/leaf_type_tank.png" }
]

# ------------------------------------ Biomes palette ------------------------------------
BIOMES = [
    {'id': 1, 'name': "plain", 'icon': "assets/imgs/icons/biome_plain.png"},
    {'id': 2, 'name': "forest", 'icon': "assets/imgs/icons/biome_forest.png"},
    {'id': 3, 'name': "lake", 'icon': "assets/imgs/icons/biome_lake.png"},
    {'id': 4, 'name': "mountain", 'icon': "assets/imgs/icons/biome_mountain.png"}
]
PLANETS = [
    { 'id': 1, 'name': "Earth", 'biomes': [BIOMES[0], BIOMES[1], BIOMES[2], BIOMES[3]] }
]

# ————————————————————————————————————————————————————————————————————————————————————————
# ————————————————————————————————————— DATA MANAGER —————————————————————————————————————
# ————————————————————————————————————————————————————————————————————————————————————————

# ------------------------------------- LeafManager --------------------------------------
# Gère les leafs possédés par le joueur, leur ajout et leurs statistiques.
class LeafManager:
    def __init__(self, owned = []):
        self.owned = owned

    def add_leaf(self,leaf):
        is_owned = False
        new_leaf = LeafStat(leaf)
        for leafs in self.owned:
            if leafs.id == new_leaf.id:
                print(new_leaf.name + " est déjà un de vos leafs.")
                is_owned = True
        if not is_owned:
            self.owned.append(new_leaf)
            print(new_leaf.name + " fais maintenant parti de vos leafs !")

class LeafStat:
    def __init__(self, leaf):
        self.id = leaf["id"]
        self.name = leaf["name"]
        self.type = leaf["type"]
        self.rarity = leaf["rarity"]
        self.atk = leaf["atk"]
        self.hp = leaf["hp"]
        self.species = leaf["species"]
        self.biome = leaf["biome"]
        self.competence_lvl = leaf["competence_lvl"]
        self.img = leaf["img"]
        self.nutrients = 20
        self.hydration = 20
        self.regime = leaf["regime"] if "regime" in leaf else None
        self.xp = leaf["xp"]

leafmanager = LeafManager()

# ------------------------------------- InventoryManager -------------------------------------
# Gère les items et l'argent possédés par le joueur, leur ajout et leurs quantités.
class InventoryManager:
    def __init__(self):
        self.items = []
        self.money = {"O2": 0, "CO2": 0}
    
    def append_item(self, item, amount=1):
        existing_item = None
        for i in self.items:
            if i["id"] == item["id"]:
                existing_item = i
                break
        
        if existing_item:
            existing_item["amount"] += amount
        else:
            new_item = item.copy()
            new_item["amount"] = amount
            self.items.append(new_item)
    
    def append_money(self, currency, amount):
        if currency in self.money:
            self.money[currency] += amount
        else:
            print(f"Currency {currency} not recognized.")
    
    def remove_item(self, item_id, amount=1):
        item_index = -1
        for i, item in enumerate(self.items):
            if item["id"] == item_id:
                item_index = i
                break
        
        if item_index != -1:
            self.items[item_index]["amount"] -= amount
            if self.items[item_index]["amount"] <= 0:
                deleted_item = self.items.pop(item_index)
                return deleted_item
        return None
    
    def remove_money(self, currency, amount):
        if currency not in self.money:
            print(f"Currency {currency} not recognized.")
            return False
        
        if self.money[currency] >= amount:
            self.money[currency] -= amount
            print(f"{currency}: {self.money[currency]} (removed {amount})")
            return True
        else:
            print(f"Not enough {currency}. Required: {amount}, Available: {self.money[currency]}")
            return False
    
    def is_item_in_inventory(self, item_id):
        return any(i["id"] == item_id for i in self.items)
    
    def is_enough_money(self, item):
        needs_O2 = "price_O2" in item and item["price_O2"] > 0
        needs_CO2 = "price_CO2" in item and item["price_CO2"] > 0
        
        # Si l'item nécessite les deux devises
        if needs_O2 and needs_CO2:
            return self.money["O2"] >= item["price_O2"] and self.money["CO2"] >= item["price_CO2"]
        # Si l'item nécessite uniquement O2
        elif needs_O2:
            return self.money["O2"] >= item["price_O2"]
        # Si l'item nécessite uniquement CO2
        elif needs_CO2:
            return self.money["CO2"] >= item["price_CO2"]
        # Si aucun prix n'est défini, l'item est gratuit
        return True
    
    def get_items(self):
        return self.items
    
    def get_money(self):
        return self.money

inventory_manager = InventoryManager()

# ------------------------------------- ShopManager -------------------------------------
# Gère les items disponibles à l'achat dans le shop, leur ajout et leur suppression.
class ShopManager:
    def __init__(self, biome=None, type_str=None):
        self.type = type_str or "classic"
        self.biome = biome or BIOMES[0]
        self.stock = get_classic_shop_items() if self.type == "classic" else get_wandering_shop_items(self.biome)
    
    def reload_wandering_shop_items(self):
        if self.type == "wandering":
            self.stock = get_wandering_shop_items(self.biome)
    
    def remove_item_from_stock(self, item_id, amount=1):
        item_index = -1
        for i, item in enumerate(self.stock):
            if item["id"] == item_id:
                item_index = i
                break
        
        if item_index != -1:
            if self.is_item_in_stock(item_id):
                item_amount = self.stock[item_index]["amount"]
                item_amount_to_remove = item_amount - amount
                if item_amount_to_remove > -1:
                    self.stock[item_index]["amount"] = item_amount_to_remove
                    return True
                else:
                    print(f"{self.stock[item_index]['name']} is out of stock")
                    return False
            else:
                print(f"{self.stock[item_index]['name']} is not in stock")
                return False
        return None
    
    def buy_item(self, item, amount=1):
        # Vérifier si le joueur a assez d'argent
        if not inventory_manager.is_enough_money(item):
            print(f"Fonds insuffisants pour acheter : {item['name']}")
            return {"success": False, "error": "insufficient_funds"}
        
        # Vérifier si l'item est en stock
        if not self.is_item_in_stock(item["id"], amount):
            print(f"{item['name']} n'est pas en stock")
            return {"success": False, "error": "out_of_stock"}
        
        # Déduire l'argent (O2)
        if "price_O2" in item and item["price_O2"] >= 0:
            if not inventory_manager.remove_money("O2", item["price_O2"] * amount):
                print(f"Erreur lors du paiement O2 pour {item['name']}")
                return {"success": False, "error": "payment_failed"}
        
        # Déduire l'argent (CO2)
        if "price_CO2" in item and item["price_CO2"] > 0:
            if not inventory_manager.remove_money("CO2", item["price_CO2"] * amount):
                # Rembourser O2 si le paiement CO2 échoue
                if "price_O2" in item and item["price_O2"] >= 0:
                    inventory_manager.append_money("O2", item["price_O2"] * amount)
                print(f"Erreur lors du paiement CO2 pour {item['name']}")
                return {"success": False, "error": "insufficient_funds"}
        
        # Ajouter l'item à l'inventaire et retirer du stock
        inventory_manager.append_item(item, amount)
        self.remove_item_from_stock(item["id"], amount)
        
        print(f"Achat réussi : {item['name']}")
        
        return {"success": True}
    
    def is_item_in_stock(self, item_id, amount=1):
        return any(i["id"] == item_id and i["amount"] >= amount for i in self.stock)

def get_classic_shop_items():
    return [
        {**item, "amount": float('inf')} # Les items du shop classique sont illimités
        for item in ITEMS.values()
        if not item["is_special"]
    ]

def get_wandering_shop_items(biome):
    specials = [
        {**item, "amount": 50}
        for item in ITEMS.values()
        if item["is_special"] and roll(item["rarity"])
    ]
    
    non_special_items = [item for item in ITEMS.values() if not item["is_special"]]
    random.shuffle(non_special_items)
    discounted_items = non_special_items[:2]
    
    discounted = [
        {
            **item,
            "price_O2": item["specialprice_O2"] if "price_O2" in item else None,
            "price_CO2": item["specialprice_CO2"] if "price_CO2" in item else None,
            "amount": 50
        }
        for item in discounted_items
    ]
    
    return specials + discounted

def roll(chance):
    return random.random() < chance

# Instances
wandering_shop_manager_plain = ShopManager(PLANETS[0]["biomes"][0], "wandering")
wandering_shop_manager_forest = ShopManager(PLANETS[0]["biomes"][1], "wandering")
wandering_shop_manager_lake = ShopManager(PLANETS[0]["biomes"][2], "wandering")
wandering_shop_manager_mountain = ShopManager(PLANETS[0]["biomes"][3], "wandering")

classic_shop_manager = ShopManager()

WANDERINGSHOPS = [
    {"id": 0, "shop": wandering_shop_manager_plain, "biome": "plain"},
    {"id": 1, "shop": wandering_shop_manager_forest, "biome": "forest"},
    {"id": 2, "shop": wandering_shop_manager_lake, "biome": "lake"},
    {"id": 3, "shop": wandering_shop_manager_mountain, "biome": "mountain"},
]