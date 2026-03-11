import random

# ————————————————————————————————————————————————————————————————————————————————————————
# ————————————————————————————————————— DATA PALETTE —————————————————————————————————————
# ————————————————————————————————————————————————————————————————————————————————————————

# ------------------------------------ Enemies palette -----------------------------------
ENEMIES = [
    { "id": 1, "name": "Crabe", "rarity": "common", "atk": 3, "hp": 10, "biome": ["plain"], "lvl": 2, "visual": "assets/imgs/npc/crab.png"},
    { "id": 1, "name": "Snake", "rarity": "rare", "atk": 5, "hp": 15, "biome": ["plain"], "lvl": 2, "visual": "assets/imgs/npc/snake.png"},
]

# ------------------------------------ Npcs palette --------------------------------------
NPCS = [
    { "id": 1, "name": "Heron", "biome": "plain", "visual": "assets/imgs/npc/heron.png"}
]

# ------------------------------------ Events palette ------------------------------------
EVENTS = {
    "plain": [
        { "type": "enemy", "data": { "enemyId": 1 } },
        { "type": "npc",   "data": { "npcId": 1 } },
        { "type": "lore",  "data": { "leafId": 1 } },
        { "type": "empty",  "data": { "itemId": 1 } },
    ]
}

# ------------------------------------ Items palette ------------------------------------
# category  : clé de filtrage UI (inventaire / shop)
# effect    : { "stat": nom_attribut_LeafStat, "amount": valeur appliquée }
#             stat = None pour les revitaliseurs (logique spéciale hp=0)

ITEMS = {
    # ── Animaux (O2) ────────────────────────────────────────────────────────────────────
    3: {
        "id": 3, "name": "Viande", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 30},
        "price_O2": 64, "specialprice_O2": 32, "is_special": False,
        "icon": "assets/imgs/items/meat.png",
        "tags": ["meat", "growth", "nouriture"],
        "description": "Riche en protéines et en énergie, cette viande est essentielle au métabolisme des leafs carnivores. Elle soutient leur croissance et leur endurance.",
        "species": ["animal"], "regime": ["carnivore"],
    },
    4: {
        "id": 4, "name": "Herbe", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 20},
        "price_O2": 32, "specialprice_O2": 16, "is_special": False,
        "icon": "assets/imgs/items/grass.png",
        "tags": ["grass", "growth", "nouriture"],
        "description": "Cette herbe fraîche fournit fibres et nutriments de base aux leafs herbivores. Un apport simple mais vital à leur équilibre digestif.",
        "species": ["animal"], "regime": ["herbivore"],
    },
    6: {
        "id": 6, "name": "Bandage", "category": "soin",
        "effect": {"stat": "hp", "amount": 3},
        "price_O2": 100, "specialprice_O2": 50, "is_special": False,
        "icon": "assets/imgs/items/bandage.png",
        "tags": ["bandage", "soin", "regeneration"],
        "description": "Conçu pour stabiliser les tissus et limiter les pertes d'énergie, ce bandage favorise une cicatrisation rapide chez les leafs animaux.",
        "species": ["animal"],
    },
    8: {
        "id": 8, "name": "Lait 🌟", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 40},
        "price_O2": 64, "is_special": True, "rarity": 1,
        "icon": "assets/imgs/items/milk.png",
        "tags": ["milk", "nutrients", "nouriture", "special"],
        "description": "Riche en calcium et en nutriments essentiels, le lait renforce la structure et la vitalité des leafs animaux. Une ressource rare à forte valeur biologique.",
        "species": ["animal"],
    },

    # ── Plantes (CO2) ────────────────────────────────────────────────────────────────────
    2: {
        "id": 2, "name": "Fertilisant", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 20},
        "price_CO2": 32, "specialprice_CO2": 16, "is_special": False,
        "icon": "assets/imgs/items/fertilizer.png",
        "tags": ["fertilizer", "growth", "nouriture"],
        "description": "Ce fertilisant enrichit le sol en éléments nutritifs et stimule la photosynthèse des leafs plantes. Indispensable à leur développement.",
        "species": ["plant"],
    },
    5: {
        "id": 5, "name": "Sève", "category": "soin",
        "effect": {"stat": "hp", "amount": 3},
        "price_CO2": 100, "specialprice_CO2": 50, "is_special": False,
        "icon": "assets/imgs/items/mineral_water.png",
        "tags": ["seve", "soin", "regeneration"],
        "description": "Cette sève régénératrice restaure les tissus végétaux et aide les leafs plantes à se régénérer durablement.",
        "species": ["plant"],
    },
    9: {
        "id": 9, "name": "Poudre d'os 🌟", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 40},
        "price_CO2": 64, "is_special": True, "rarity": 1,
        "icon": "assets/imgs/items/bone_meal.png",
        "tags": ["bone_meal", "growth", "nouriture", "special"],
        "description": "Riche en phosphore et en calcium, cette poudre stimule fortement la croissance des leafs plantes. Un engrais puissant issu de matières anciennes.",
        "species": ["plant"],
    },

    # ── Universels (O2 + CO2) ────────────────────────────────────────────────────────────
    1: {
        "id": 1, "name": "Eau minérale", "category": "boisson",
        "effect": {"stat": "hydration", "amount": 20},
        "price_O2": 4, "price_CO2": 4, "specialprice_O2": 2, "specialprice_CO2": 2, "is_special": False,
        "icon": "assets/imgs/items/water.png",
        "tags": ["water", "hydration", "boisson"],
        "description": "Indispensable à toute forme de vie, l'eau minérale régule les échanges internes et maintient l'équilibre vital de tous les leafs.",
    },
    7: {
        "id": 7, "name": "Rayon de soleil", "category": "revitaliseur",
        "effect": {"stat": "hp", "amount": 1},   # revitalise depuis hp=0
        "price_O2": 200, "price_CO2": 200, "specialprice_O2": 100, "specialprice_CO2": 100, "is_special": False,
        "icon": "assets/imgs/items/sunshine.png",
        "tags": ["sunshine", "revitaliseur"],
        "description": "Concentré d'énergie solaire, ce rayon relance les processus vitaux et peut ramener un leaf au seuil de la vie.",
    },
    10: {
        "id": 10, "name": "Elixir de vie 🌟", "category": "revitaliseur",
        "effect": {"stat": "hp", "amount": 5},   # revitalise + soigne davantage
        "price_O2": 300, "price_CO2": 300, "is_special": True, "rarity": 1,
        "icon": "assets/imgs/items/elixir.png",
        "tags": ["elixir_of_life", "revitaliseur", "special"],
        "description": "Composé d'essences rares et hautement énergétiques, cet élixir agit directement sur les mécanismes vitaux et défie le cycle naturel de la vie.",
    },
    11: {
        "id": 11, "name": "Potion d'attaque 🌟", "category": "boost",
        "effect": {"stat": "atk", "amount": 2},
        "price_O2": 100, "price_CO2": 100, "is_special": True, "rarity": 1,
        "icon": "assets/imgs/items/attack_boost.png",
        "tags": ["attack_boost", "boost", "special"],
        "description": "Cette potion spéciale augmente temporairement la puissance d'attaque des leafs, leur conférant un avantage stratégique en combat.",
    },
    12: {
        "id": 12, "name": "Potion de vie 🌟", "category": "boost",
        "effect": {"stat": "hp", "amount": 3},
        "price_O2": 100, "price_CO2": 100, "is_special": True, "rarity": 1,
        "icon": "assets/imgs/items/health_boost.png",
        "tags": ["health_boost", "boost", "special"],
        "description": "Cette potion spéciale augmente les points de vie des leafs, renforçant leur endurance face aux défis environnementaux.",
    },
    13: {
        "id": 13, "name": "Livre de la connaissance 🌟", "category": "boost",
        "effect": {"stat": "level", "amount": 5},
        "price_O2": 150, "price_CO2": 150, "is_special": True, "rarity": 1,
        "icon": "assets/imgs/items/book_of_knowledge.png",
        "tags": ["book_of_knowledge", "boost", "special"],
        "description": "Ce livre ancien renferme des savoirs oubliés qui, une fois assimilés, augmentent les capacités et la sagesse des leafs.",
    },
}

TYPES = [
    { "id": 1, "name": "nouriture",   "icon": "assets/imgs/icons/type_food.png" },
    { "id": 2, "name": "soin",        "icon": "assets/imgs/icons/type_heal.png" },
    { "id": 3, "name": "boisson",     "icon": "assets/imgs/icons/type_beverage.png" },
    { "id": 4, "name": "revitaliseur","icon": "assets/imgs/icons/type_resurrector.png" },
]

# ------------------------------------ Leafs palette ------------------------------------
LEAFS = {
    2:  { "id": 2,  "name": "mouton",     "type": 2, "rarity": "default", "atk": 2,  "hp": 40,  "species": "animal", "regime": "herbivore", "biome": 1, "level": 0, "img": "assets/imgs/leafs/Leaf_sheep.png",      "xp": 0  },
    3:  { "id": 3,  "name": "abeille",    "type": 2, "rarity": "default", "atk": 3,  "hp": 40,  "species": "animal", "regime": "herbivore", "biome": 1, "level": 0, "img": "assets/imgs/leafs/Leaf_bee.png",        "xp": 0  },
    5:  { "id": 5,  "name": "loup",       "type": 1, "rarity": "default", "atk": 6,  "hp": 20,  "species": "animal", "regime": "carnivore", "biome": 2, "level": 0, "img": "assets/imgs/leafs/Leaf_wolf.png",       "xp": 0  },
    8:  { "id": 8,  "name": "poisson",    "type": 1, "rarity": "default", "atk": 5,  "hp": 40,  "species": "animal", "regime": "herbivore", "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_fish.png",       "xp": 0  },
    9:  { "id": 9,  "name": "chèvre",     "type": 3, "rarity": "default", "atk": 2,  "hp": 100, "species": "animal", "regime": "herbivore", "biome": 4, "level": 0, "img": "assets/imgs/leafs/Leaf_goat.png",       "xp": 0  },
    12: { "id": 12, "name": "aigle",      "type": 1, "rarity": "default", "atk": 4,  "hp": 60,  "species": "animal", "regime": "carnivore", "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_eagle.png",      "xp": 0  },
    13: { "id": 13, "name": "ours",       "type": 3, "rarity": "default", "atk": 7,  "hp": 120, "species": "animal", "regime": "carnivore", "biome": 4, "level": 0, "img": "assets/imgs/leafs/Leaf_bear.png",       "xp": 0  },
    1:  { "id": 1,  "name": "pissenlit",  "type": 1, "rarity": "default", "atk": 5,  "hp": 40,  "species": "plant",  "biome": 1, "level": 0, "img": "assets/imgs/leafs/Leaf_dandelion.png",   "xp": 0  },
    4:  { "id": 4,  "name": "sapin",      "type": 3, "rarity": "default", "atk": 3,  "hp": 80,  "species": "plant",  "biome": 2, "level": 0, "img": "assets/imgs/leafs/Leaf_pine.png",        "xp": 0  },
    6:  { "id": 6,  "name": "fraisier",   "type": 2, "rarity": "default", "atk": 3,  "hp": 60,  "species": "plant",  "biome": 2, "level": 0, "img": "assets/imgs/leafs/Leaf_strawberry.png",  "xp": 0  },
    7:  { "id": 7,  "name": "roseaux",    "type": 3, "rarity": "default", "atk": 3,  "hp": 80,  "species": "plant",  "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_reeds.png",       "xp": 0  },
    10: { "id": 10, "name": "arbuste",    "type": 3, "rarity": "default", "atk": 1,  "hp": 120, "species": "plant",  "biome": 4, "level": 0, "img": "assets/imgs/leafs/Leaf_bush.png",        "xp": 0  },
    11: { "id": 11, "name": "nénuphare",  "type": 2, "rarity": "default", "atk": 1,  "hp": 40,  "species": "plant",  "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_lilypad.png",     "xp": 0  },
}

LEAFS_TYPE = [
    { "id": 0, "name": "default",  "icon": "assets/imgs/icons/leaf_type_default.png"  },
    { "id": 1, "name": "attacker", "icon": "assets/imgs/icons/leaf_type_attacker.png" },
    { "id": 2, "name": "healer",   "icon": "assets/imgs/icons/leaf_type_healer.png"   },
    { "id": 3, "name": "tank",     "icon": "assets/imgs/icons/leaf_type_tank.png"     },
]

BIOMES = [
    { "id": 1, "name": "plain",    "icon": "assets/imgs/icons/biome_plain.png"    },
    { "id": 2, "name": "forest",   "icon": "assets/imgs/icons/biome_forest.png"   },
    { "id": 3, "name": "lake",     "icon": "assets/imgs/icons/biome_lake.png"     },
    { "id": 4, "name": "mountain", "icon": "assets/imgs/icons/biome_mountain.png" },
]

PLANETS = [
    { "id": 1, "name": "Earth", "biomes": [BIOMES[0], BIOMES[1], BIOMES[2], BIOMES[3]] }
]

# ————————————————————————————————————————————————————————————————————————————————————————
# ————————————————————————————————————— DATA MANAGER —————————————————————————————————————
# ————————————————————————————————————————————————————————————————————————————————————————

class LeafStat:
    def __init__(self, leaf):
        self.id            = leaf["id"]
        self.name          = leaf["name"]
        self.type          = leaf["type"]
        self.rarity        = leaf["rarity"]
        self.atk           = leaf["atk"]
        self.hp            = leaf["hp"]
        self.species       = leaf["species"]
        self.biome         = leaf["biome"]
        self.level         = leaf["level"]
        self.img           = leaf["img"]
        self.nutrients     = 100
        self.hydration     = 100
        self.regime        = leaf.get("regime", None)
        self.xp            = leaf["xp"]
        self.hp_max        = leaf["hp"]
        self.atk_max       = leaf["atk"]
        self.STAT_MAX = {
            "hp":        self.hp_max,
            "nutrients": 100,
            "hydration": 100,
            "atk":       self.atk_max,
            "level":     100,
        }

    # Limites max par stat
    STAT_MAX = {
        "hp": 10, "nutrients": 100, "hydration": 100, "atk": 10, "level": 100,
    }

    def stat_update(self, stat: str, amount: int):
        if not hasattr(self, stat):
            print(f"Stat '{stat}' inexistante pour {self.name}.")
            return
        current = getattr(self, stat)
        max_val = self.STAT_MAX.get(stat, 9999)
        new_val = max(0, min(current + amount, max_val))
        setattr(self, stat, new_val)
        print(f"{self.name} - {stat} : {current} -> {new_val}")


class LeafManager:
    def __init__(self):
        self.owned = []

    def add_leaf(self, leaf):
        if any(l.id == leaf["id"] for l in self.owned):
            print(f"{leaf['name']} est déjà dans votre collection.")
            return
        self.owned.append(LeafStat(leaf))
        print(f"{leaf['name']} ajouté à votre collection !")


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
        needs_O2  = item.get("price_O2",  0) > 0
        needs_CO2 = item.get("price_CO2", 0) > 0
        if needs_O2 and needs_CO2:
            return self.money["O2"] >= item["price_O2"] and self.money["CO2"] >= item["price_CO2"]
        if needs_O2:
            return self.money["O2"]  >= item["price_O2"]
        if needs_CO2:
            return self.money["CO2"] >= item["price_CO2"]
        return True

    def get_items(self):  return self.items
    def get_money(self):  return self.money


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
    specials   = [{**i, "amount": 50} for i in ITEMS.values() if i["is_special"] and roll(i["rarity"])]
    non_special = [i for i in ITEMS.values() if not i["is_special"]]
    random.shuffle(non_special)
    discounted = [
        {**i,
        "price_O2":  i.get("specialprice_O2"),
        "price_CO2": i.get("specialprice_CO2"),
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

# ── Dialogues ────────────────────────────────────────────────────────────────────────────
s1 = ["hey", "bonjour", "tfq", "rien et toi", "quoi", "feur"]