# -*- coding: utf-8 -*-
"""
Gestionnaire de la collection de Leafs du joueur (Singleton / instance partagée).
Conversion de js/gameplay/leafs/leafManager.js.
"""

from js.gameplay.leafs.leaf_stats import LeafStat


class LeafManager:
    """Gère les Leafs possédés par le joueur."""

    def __init__(self):
        self.owned: list[LeafStat] = []

    def add_leaf(self, leaf: dict) -> None:
        """Ajoute un Leaf à la collection s'il n'est pas déjà présent."""
        existing = next((l for l in self.owned if l.id == leaf["id"]), None)
        if existing:
            return
        self.owned.append(LeafStat(leaf))


# Instance unique (équivalent du singleton JS export const leafManager)
leaf_manager = LeafManager()
