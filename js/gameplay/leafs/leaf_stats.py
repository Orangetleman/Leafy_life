# -*- coding: utf-8 -*-
"""
Statistiques d'un Leaf (instance en jeu).
Conversion de js/gameplay/leafs/leafStats.js.
"""


class LeafStat:
    """Représente un Leaf possédé par le joueur, avec états (nutrients, hydration)."""

    def __init__(self, leaf: dict):
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
        self.nutrients = 100
        self.hydration = 100
        self.regime = leaf.get("regime")  # uniquement pour les animaux
