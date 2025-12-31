import { ITEMS } from "../../data/items.js";
import { inventoryManager } from "../inventory/inventoryManager.js";
export class ShopManager {
    constructor(biome,type) {
        this.type = type || "classic"
        this.biome = biome || "plain"
        this.stock = this.type === "classic" ? getClassicShopItems() : getWanderingShopItems(this.biome)
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
    buyItem(item) {
        const price = {price_O2 : item.price_O2 ? item.price_O2 : undefined, price_CO2: item.price_CO2 ? item.price_CO2 : undefined}
        const existingPriceO2 = item.price_O2 ? true : false;
        const existingPriceCO2 = item.price_CO2 ? true : false;
        if (inventoryManager.isenoughMoney(price)) {
            if ( existingPriceO2 && existingPriceCO2 ) {
                inventoryManager.removeMoney("price_O2", item.price_O2 || undefined);
                inventoryManager.removeMoney("price_CO2", item.price_CO2 || undefined);
            } else if ( existingPriceO2 ) {
                inventoryManager.removeMoney("price_O2", item.price_O2 || undefined);
            } else if ( existingPriceCO2 ) {
                inventoryManager.removeMoney("price_CO2", item.price_CO2 || undefined);
            }
            inventoryManager.appendItem(item, 1);
            this.removeItemFromStock(item.id, 1);
            console.log(`Achat réussi : ${item.name}`);
            return true;
        } else {
            console.warn(`Fonds insuffisants pour acheter : ${item.name}`);
            return false;
        }
    }
    isIteminStock(itemId) {
        return this.stock.some((i) => (i.id === itemId || i.amount > 0))
    }
}
export function getClassicShopItems() {
    return ITEMS.filter(item => !item.is_special).map((itm) => ({...itm, amount: 99999}));
}
export function getWanderingShopItems(biome) {
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
