import { ITEMS } from "../../data/items.js";
import { PLANETS, BIOMES } from "../../data/planets.js"
import { inventoryManager } from "../inventory/inventoryManager.js";
export class ShopManager {
    constructor(biome,type) {
        this.type = type || "classic"
        this.biome = biome || BIOMES[0]
        this.stock = this.type === "classic" ? getClassicShopItems() : getWanderingShopItems(this.biome)
    }
    reloadWanderingShopItems() {
        this.stock = this.type === "wandering" ? getWanderingShopItems(this.biome) : this.stock
    }
    removeItemFromStock(itemId, amount = 1) {
        const itemIndex = this.stock.findIndex(i => i.id === itemId);
        if (itemIndex !== -1) {
            if (this.isIteminStock(itemId)) {
                const itemAmount = this.stock[itemIndex].amount
                const itemAmountToRemove = itemAmount - amount
                if (itemAmountToRemove > -1) {
                    this.stock[itemIndex].amount = itemAmountToRemove
                    return true
                } else {
                    warn(`${this.stock[itemIndex].name} is out of stock`)
                    return false
                }
            } else {
                warn(`${this.stock[itemIndex].name} is not in stock`)
                return false
            }
        }
    }
    buyItem(item, amount = 1) {
        // Vérifier si le joueur a assez d'argent
        if (!inventoryManager.isenoughMoney(item)) {
            console.warn(`Fonds insuffisants pour acheter : ${item.name}`);
            return { success: false, error: "insufficient_funds" };
        }
        // Vérifier si l'item est en stock
        if (!this.isIteminStock(item.id, amount)) {
            console.warn(`${item.name} n'est pas en stock`);
            return { success: false, error: "out_of_stock" };
        }
        // Déduire l'argent (O2)
        if (item.price_O2 !== undefined && item.price_O2 >= 0) {
            if (!inventoryManager.removeMoney("O2", item.price_O2*amount)) {
                console.error(`Erreur lors du paiement O2 pour ${item.name}`);
                return { success: false, error: "payment_failed" };
            }
        }
        // Déduire l'argent (CO2)
        if (item.price_CO2 !== undefined && item.price_CO2 > 0) {
            if (!inventoryManager.removeMoney("CO2", item.price_CO2*amount)) {
                // Rembourser O2 si le paiement CO2 échoue (si on a assez d'O2 mais pas assez de CO2 -> ça rembourse le O2 et ça annul l'achat)
                if (item.price_O2 !== undefined && item.price_O2 >= 0) {
                    inventoryManager.appendMoney("O2", item.price_O2*amount);
                }
                console.error(`Erreur lors du paiement CO2 pour ${item.name}`);
                return { success: false, error: "insufficient_funds" };
            }
        }
        // Ajouter l'item à l'inventaire et retirer du stock
        inventoryManager.appendItem(item, amount);
        this.removeItemFromStock(item.id, amount);

        console.log(`Achat réussi : ${item.name}`);

        return { success: true };
    }
    isIteminStock(itemId, amount = 1) {
        return this.stock.some((i) => (i.id === itemId && i.amount >= amount))
    }
}
function getClassicShopItems() {
    return ITEMS.filter(item => !item.is_special).map((itm) => ({...itm, amount: 99999}));
}
function getWanderingShopItems(biome) {
    const specials = ITEMS.filter(i => i.is_special && roll(i.rarity)).map(i => ({...i, amount: 50/*quantité dispo dans le shop itinérant d'items spéciaux*/}));
    const discounted = ITEMS.filter(i => !i.is_special)
                            .sort(() => Math.random() - 0.5)
                            .slice(0, 2)
                            .map(i => ({
                                ...i,
                                price_O2: i.price_O2 ? i.specialprice_O2 : undefined,
                                price_CO2: i.price_CO2 ? i.specialprice_CO2 : undefined,
                                amount : 50 // Quantité dispo dans le shop itinérant d'items normaux
                            }));
    return [...specials, ...discounted];
}

function roll(chance) {
    return Math.random() < chance;
}


const wanderingShopManagerPlain = new ShopManager(PLANETS[0].biomes[0], "wandering");
const wanderingShopManagerForest = new ShopManager(PLANETS[0].biomes[1], "wandering");
const wanderingShopManagerLake = new ShopManager(PLANETS[0].biomes[2], "wandering");
const wanderingShopManagerMountain = new ShopManager(PLANETS[0].biomes[3], "wandering");

export const classicShopManager = new ShopManager();
export const WANDERINGSHOPS = [
    {id:0, shop: wanderingShopManagerPlain, biome: "plain"},
    {id:1, shop: wanderingShopManagerForest, biome: "forest"},
    {id:2, shop: wanderingShopManagerLake, biome: "lake"},
    {id:3, shop: wanderingShopManagerMountain, biome: "Mountain"},
]