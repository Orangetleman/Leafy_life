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
        "atk": 3, "hp": 10,
        "biome": ["lake"], "lvl": 1,
        "visual": "assets/imgs/npc/crab.png",
        "met": False, "prez": "Un crabe minuscule, mais ses pinces font mal.",
        "reward": {"currency": "O2", "amount": 8},
    },
    {
        "id": 1, "name": "Ours", "rarity": "common",
        "atk": 7, "hp": 30,
        "biome": ["forest"], "lvl": 1,
        "visual": "assets/imgs/npc/bear.png",
        "met": False, "prez": "Un ours.",
        "reward": {"currency": "CO2", "amount": 20},
    },
    {
        "id": 2, "name": "Snake", "rarity": "rare",
        "atk": 5, "hp": 20,
        "biome": ["plain"], "lvl": 3,
        "visual": "assets/imgs/npc/snake.png",
        "met": False, "prez": "Un serpent agile. Difficile à esquiver.",
        "reward": {"currency": "O2", "amount": 18},
    },
    {
        "id": 1, "name": "Crabefaible", "rarity": "common",
        "atk": 3, "hp": 10,
        "biome": ["plain"], "lvl": 1,
        "visual": "assets/imgs/npc/crabfaible.png",
        "met": False, "prez": "Un crabe minuscule, mais ses pinces font mal.",
        "reward": {"currency": "O2", "amount": 8},
    },
]

# ------------------------------------ Npcs palette --------------------------------------
NPCS = [
    { "id": 1, "name": "Heron", "biome": "lake", "visual": "assets/imgs/npc/heron.png"},
    { "id": 1, "name": "Cat", "biome": "plain", "visual": "assets/imgs/npc/cat.png"}
]

# ------------------------------------ Objects palette -----------------------------------
OBJECTS = [
    { "id": 1, "name": "flaque", "visual": "assets/imgs/icons/flaque.png",    "gives": "Eau minérale"},
    { "id": 2, "name": "rien",   "visual": "assets/imgs/icons/Undefined.png", "gives": "Eau minérale"}
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
        "price_O2": 55, "is_special": True, "rarity": 0.3,
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
        "icon": "assets/imgs/items/mineral_water.png",
        "tags": ["seve", "soin", "regeneration"],
        "description": "Cette sève régénératrice restaure les tissus végétaux.",
        "species": ["plant"],
    },
    9: {
        "id": 9, "name": "Poudre d'os 🌟", "category": "nouriture",
        "effect": {"stat": "nutrients", "amount": 50},
        "price_CO2": 55, "is_special": True, "rarity": 0.3,
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
        "price_O2": 180, "price_CO2": 180, "is_special": True, "rarity": 0.2,
        "icon": "assets/imgs/items/elixir.png",
        "tags": ["elixir_of_life", "revitaliseur", "special"],
        "description": "Cet élixir agit directement sur les mécanismes vitaux et défie le cycle naturel de la vie.",
    },
    11: {
        "id": 11, "name": "Potion d'attaque 🌟", "category": "boost",
        "effect": {"stat": "atk", "amount": 5},
        "price_O2": 85, "price_CO2": 85, "is_special": True, "rarity": 0.2,
        "icon": "assets/imgs/items/attack_boost.png",
        "tags": ["attack_boost", "boost", "special"],
        "description": "Booste temporairement l'attaque pour toute la durée d'un combat.",
    },
    12: {
        "id": 12, "name": "Potion de vie 🌟", "category": "boost",
        "effect": {"stat": "hp", "amount": 15},
        "price_O2": 80, "price_CO2": 80, "is_special": True, "rarity": 0.2,
        "icon": "assets/imgs/items/health_boost.png",
        "tags": ["health_boost", "boost", "special"],
        "description": "Augmente durablement le maximum de points de vie d'un leaf.",
    },
    13: {
        "id": 13, "name": "Livre de la connaissance 🌟", "category": "boost",
        "effect": {"stat": "level", "amount": 5},
        "price_O2": 150, "price_CO2": 150, "is_special": True, "rarity": 0.1,
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
    2:  { "id": 2,  "name": "mouton",    "type": 2, "rarity": "default", "atk": 2, "hp": 40,  "species": "animal", "regime": "herbivore", "biome": 1, "level": 0, "img": "assets/imgs/leafs/Leaf_sheep.png",      "xp": 0, "met": False, "prez":"hehe" },
    3:  { "id": 3,  "name": "abeille",   "type": 2, "rarity": "default", "atk": 3, "hp": 40,  "species": "animal", "regime": "herbivore", "biome": 1, "level": 0, "img": "assets/imgs/leafs/Leaf_bee.png",        "xp": 0, "met": False, "prez":"hehe" },
    5:  { "id": 5,  "name": "loup",      "type": 1, "rarity": "default", "atk": 6, "hp": 20,  "species": "animal", "regime": "carnivore", "biome": 2, "level": 0, "img": "assets/imgs/leafs/Leaf_wolf.png",       "xp": 0, "met": False, "prez":"hehe" },
    8:  { "id": 8,  "name": "poisson",   "type": 1, "rarity": "default", "atk": 5, "hp": 40,  "species": "animal", "regime": "herbivore", "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_fish.png",       "xp": 0, "met": False, "prez":"hehe" },
    9:  { "id": 9,  "name": "chèvre",    "type": 3, "rarity": "default", "atk": 2, "hp": 100, "species": "animal", "regime": "herbivore", "biome": 4, "level": 0, "img": "assets/imgs/leafs/Leaf_goat.png",       "xp": 0, "met": False, "prez":"hehe" },
    12: { "id": 12, "name": "aigle",     "type": 1, "rarity": "default", "atk": 4, "hp": 60,  "species": "animal", "regime": "carnivore", "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_eagle.png",      "xp": 0, "met": False, "prez":"hehe" },
    13: { "id": 13, "name": "trefle",    "type": 3, "rarity": "default", "atk": 7, "hp": 120, "species": "plant", "biome": 4, "level": 0, "img": "assets/imgs/leafs/Leaf_clover.png",       "xp": 0, "met": False, "prez":"hehe" },
    1:  { "id": 1,  "name": "pissenlit", "type": 1, "rarity": "default", "atk": 5, "hp": 40,  "species": "plant",  "biome": 1, "level": 0, "img": "assets/imgs/leafs/Leaf_dandelion.png",   "xp": 0, "met": False, "prez":"hehe" },
    4:  { "id": 4,  "name": "sapin",     "type": 3, "rarity": "default", "atk": 3, "hp": 80,  "species": "plant",  "biome": 2, "level": 0, "img": "assets/imgs/leafs/Leaf_pine.png",        "xp": 0, "met": False, "prez":"hehe" },
    6:  { "id": 6,  "name": "fraisier",  "type": 2, "rarity": "default", "atk": 3, "hp": 60,  "species": "plant",  "biome": 2, "level": 0, "img": "assets/imgs/leafs/Leaf_strawberry.png",  "xp": 0, "met": False, "prez":"hehe" },
    7:  { "id": 7,  "name": "roseaux",   "type": 3, "rarity": "default", "atk": 3, "hp": 80,  "species": "plant",  "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_reeds.png",       "xp": 0, "met": False, "prez":"hehe" },
    10: { "id": 10, "name": "arbuste",   "type": 3, "rarity": "default", "atk": 1, "hp": 120, "species": "plant",  "biome": 4, "level": 0, "img": "assets/imgs/leafs/Leaf_bush.png",        "xp": 0, "met": False, "prez":"hehe" },
    11: { "id": 11, "name": "nénuphare", "type": 2, "rarity": "default", "atk": 1, "hp": 40,  "species": "plant",  "biome": 3, "level": 0, "img": "assets/imgs/leafs/Leaf_lilypad.png",     "xp": 0, "met": False, "prez":"hehe" },
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
    # Décale le pic naturel vers la droite (x=e²-1 ≈ 6.39) et reste strictement positif
    # sur tout l'intervalle [0, +∞), ce qui évite toute explosion aux hauts niveaux.
    # Voir calculate_atk_from_level et calculate_hp_from_level pour les valeurs exactes.
    def calculate_atk_from_level(self):
        if self.level <= 0:
            return self.atk_base
        # Toujours calculé depuis atk_base (valeur originale immuable du leaf),
        # jamais depuis atk_max qui évolue lui aussi — sinon effet exponentiel garanti.
        # ln(x+1)/sqrt(x+1) : monte vite sur les premiers niveaux, pic vers niveau 2-5,
        # puis décroît très doucement sans jamais exploser — aucun terme linéaire.
        #   niveau  1  → ATK ×1.59   niveau 20 → ATK ×1.80
        #   niveau  2  → ATK ×1.76   niveau 50 → ATK ×1.66
        #   niveau  5  → ATK ×1.88   niveau 100→ ATK ×1.55
        factor = 1 + (math.log(self.level + 1) / math.sqrt(self.level + 1)) * 1.20
        return max(self.atk_base, int(self.atk_base * factor))

    def calculate_hp_from_level(self):
        if self.level <= 0:
            return self.hp_base
        # Même principe : calculé depuis hp_base, pas hp_max.
        # Coefficient plus élevé pour que les HP restent significatifs
        # aux hauts niveaux, notamment pour les leafs tank.
        #   niveau  1  → HP ×1.98   niveau 20 → HP ×2.33
        #   niveau  2  → HP ×2.27   niveau 50 → HP ×2.10
        #   niveau  5  → HP ×2.46   niveau 100→ HP ×1.92
        factor = 1 + (math.log(self.level + 1) / math.sqrt(self.level + 1)) * 2.00
        return max(self.hp_base, int(self.hp_base * factor))

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
        ratio = (nut_base_ratio + hyd_ratio) / 2.0 + (nut_boost_ratio * 0.5)
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


LORE = [{'dialogue':s1,'visual':"assets/imgs/leafs/Leaf_dandelion.png",'combat':False,"add":1},
        {'dialogue':s2,'visual':"assets/imgs/npc/crabfaible.png",'combat':True,"add":None},
        {'dialogue':s2,'visual':"assets/imgs/leafs/Leaf_clover.png",'combat':False,"add":None},
        {'dialogue':s2,'visual':"assets/imgs/leafs/Leaf_clover.png",'combat':False,"add":None},
        {'dialogue':s2,'visual':"assets/imgs/leafs/Leaf_clover.png",'combat':False,"add":None},
        ]