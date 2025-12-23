export const ITEMS = [
    /* Consomables Leafs Mobs (O2): */
        /* Normaux : */
    { id: 3, name: "Meat", use: "food", price_O2: 64, specialprice_O2: 32, is_special: false, icon: "assets/imgs/icons/meat.png" },
    { id: 4, name: "Grass", use: "food", price_O2: 32, specialprice_O2: 16, is_special: false, icon: "assets/imgs/icons/grass.png" },
    { id: 6, name: "Bandage", use: "heal", price_O2: 100, specialprice_O2: 50, is_special: false, icon: "assets/imgs/icons/bandage.png" },
        /* Spéciaux : */
    { id: 8, name: "Lait", use: "food", specialprice_O2: 64, is_special: true, rarity: 0.5, icon: "assets/imgs/icons/milk.png" },
    /* Consomables Leafs Plantes (CO2): */
        /* Normaux : */
    { id: 2, name: "Fertilizer", use: "food", price_CO2: 32, specialprice_CO2: 16, is_special: false, icon: "assets/imgs/icons/fertilizer.png" },
    { id: 5, name: "Mineral Water", use: "heal", price_CO2: 100, specialprice_CO2: 50, is_special: false, icon: "assets/imgs/icons/mineral_water.png" },
        /* Spéciaux : */
    { id: 9, name: "Bone Meal", use: "food", specialprice_O2: 64, is_special: true, rarity: 0.5, icon: "assets/imgs/icons/bone_meal.png" },
    /* Consomables Leafs Plantes et Mobs (O2 + CO2): */
        /* Normaux : */
    { id: 1, name: "H2O", use: "beverage", price_O2: 4, price_CO2: 4, specialprice_O2: 2, specialprice_CO2: 2, is_special: false, icon: "assets/imgs/icons/water.png" },
    { id: 7, name: "Ray of sunshine", use: "resurrector", price_O2: 200, price_CO2: 200, is_special: false, icon: "assets/imgs/icons/sunshine.png" },
        /* Spéciaux : */
    { id: 10, name: "Elixir of life", use: "resurrector", specialprice_O2: 300, specialprice_CO2: 300, is_special: true, rarity: 0.2, icon: "assets/imgs/icons/elixir.png" },
];