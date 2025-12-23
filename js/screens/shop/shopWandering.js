import { ITEMS } from "../../data/items.js";

export function getWanderingShopItems(biome) {
    const specials = ITEMS.filter(i => i.is_special && roll(i.rarity));
    const discounted = ITEMS.filter(i => !i.is_special)
                            .sort(() => Math.random() - 0.5)
                            .slice(0, 2)
                            .map(i => ({
                                ...i,
                                price_O2: i.price_O2 ? Math.floor(i.price_O2 / 2) : undefined,
                                price_CO2: i.price_CO2 ? Math.floor(i.price_CO2 / 2) : undefined
                            }));

    return [...specials, ...discounted];
}

function roll(chance) {
    return Math.random() < chance;
}
