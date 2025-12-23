import { ITEMS } from "../../data/items.js";

export function getClassicShopItems() {
    return ITEMS.filter(item => !item.is_special);
}
