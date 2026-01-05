export const ITEMS = [
    /* Consomables Leafs Mobs (O2): */
        /* Normaux : */
    { id: 3, name: "Meat", use: "food", price_O2: 64, specialprice_O2: 32, is_special: false, icon: "assets/imgs/icons/meat.png",
        tags : ["meat", "growth", "food"],
        description: "Riche en protéines et en énergie, cette viande est essentielle au métabolisme des leafs carnivores. Elle soutient leur croissance et leur endurance." },
    { id: 4, name: "Grass", use: "food", price_O2: 32, specialprice_O2: 16, is_special: false, icon: "assets/imgs/icons/grass.png",
        tags : ["grass", "growth", "food"],
        description: "Cette herbe fraîche fournit fibres et nutriments de base aux leafs herbivores. Un apport simple mais vital à leur équilibre digestif." },
    { id: 6, name: "Bandage", use: "heal", price_O2: 100, specialprice_O2: 50, is_special: false, icon: "assets/imgs/icons/bandage.png",
        tags : ["bandage", "heal", "regeneration"],
        description: "Conçu pour stabiliser les tissus et limiter les pertes d’énergie, ce bandage favorise une cicatrisation rapide chez les leafs animaux." },

        /* Spéciaux : */
    { id: 8, name: "Milk 🌟", use: "food", price_O2: 64, is_special: true, rarity: 1/*0.5*/, icon: "assets/imgs/icons/milk.png",
        tags : ["milk", "nutrients", "food", "special"],
        description: "Riche en calcium et en nutriments essentiels, le lait renforce la structure et la vitalité des leafs animaux. Une ressource rare à forte valeur biologique." },

    /* Consomables Leafs Plantes (CO2): */
        /* Normaux : */
    { id: 2, name: "Fertilizer", use: "food", price_CO2: 32, specialprice_CO2: 16, is_special: false, icon: "assets/imgs/icons/fertilizer.png",
        tags : ["fertilizer", "growth", "food"],
        description: "Ce fertilisant enrichit le sol en éléments nutritifs et stimule la photosynthèse des leafs plantes. Indispensable à leur développement." },
    { id: 5, name: "Mineral Water", use: "heal", price_CO2: 100, specialprice_CO2: 50, is_special: false, icon: "assets/imgs/icons/mineral_water.png",
        tags : ["mineral_water", "heal", "regeneration"],
        description: "Chargée en minéraux essentiels, cette eau restaure les tissus végétaux et aide les leafs plantes à se régénérer durablement." },

        /* Spéciaux : */
    { id: 9, name: "Bone Meal 🌟", use: "food", price_O2: 64, is_special: true, rarity: 1/*0.5*/, icon: "assets/imgs/icons/bone_meal.png",
        tags : ["bone_meal", "growth", "food", "special"],
        description: "Riche en phosphore et en calcium, cette poudre stimule fortement la croissance des leafs plantes. Un engrais puissant issu de matières anciennes." },

    /* Consomables Leafs Plantes et Mobs (O2 + CO2): */
        /* Normaux : */
    { id: 1, name: "H2O", use: "beverage", price_O2: 4, price_CO2: 4, specialprice_O2: 2, specialprice_CO2: 2, is_special: false, icon: "assets/imgs/icons/water.png",
        tags : ["water", "hydration", "beverage"],
        description: "Molécule indispensable à toute forme de vie, l’eau régule les échanges internes et maintient l’équilibre vital de tous les leafs." },
    { id: 7, name: "Ray of sunshine", use: "resurrector", price_O2: 200, price_CO2: 200, specialprice_O2: 100, specialprice_CO2: 100, is_special: false, icon: "assets/imgs/icons/sunshine.png",
        tags : ["sunshine", "resurrector"],
        description: "Concentré d’énergie solaire, ce rayon relance les processus vitaux et peut ramener un leaf au seuil de la vie." },

        /* Spéciaux : */
    { id: 10, name: "Elixir of life 🌟", use: "resurrector", price_O2: 300, price_CO2: 300, is_special: true, rarity: 1/*0.2*/, icon: "assets/imgs/icons/elixir.png",
        tags : ["elixir_of_life", "resurrector", "special"],
        description: "Composé d’essences rares et hautement énergétiques, cet élixir agit directement sur les mécanismes vitaux et défie le cycle naturel de la vie." },
];

export const TYPES = [
    { id: 1, name: "food", icon: "assets/imgs/icons/type_food.png" },
    { id: 2, name: "heal", icon: "assets/imgs/icons/type_heal.png" },
    { id: 3, name: "beverage", icon: "assets/imgs/icons/type_beverage.png" },
    { id: 4, name: "resurrector", icon: "assets/imgs/icons/type_resurrector.png" }
];