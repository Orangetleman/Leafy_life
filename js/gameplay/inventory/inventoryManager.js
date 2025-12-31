export class InventoryManager {
    constructor() {
        this.items = [];
        this.money = { O2: 0, CO2: 0 };
    }
    appendItem(item,  amount = 1) {
        const existingItem = this.items.find(i => i.id === item.id);
        if (existingItem) {
            existingItem.amount += amount;
        } else {
            this.items.push({ ...item, amount: amount });
        }
        console.log(`Item ajouté : ${item.name} (Total: ${this.items.find(i => i.id === item.id).amount})`);
    }
    appendMoney(currency, amount) {
        if (this.money.hasOwnProperty(currency)) {
            this.money[currency] += amount;
        } else {
            console.warn(`Currency ${currency} not recognized.`);
        }
    }
    removeItem(itemId, amount = 1) {
        const itemIndex = this.items.findIndex(i => i.id === itemId);
        if (itemIndex !== -1) {
            this.items[itemIndex].amount -= amount;
            if (this.items[itemIndex].amount <= 0) {
                deletedItem = this.items.splice(itemIndex, 1);
                return deletedItem;
            }
        }
    }
    removeMoney(currency, amount) {
        if (!this.money.hasOwnProperty(currency)) {
            console.warn(`Currency ${currency} not recognized.`);
            return false;
        }
        
        if (this.money[currency] >= amount) {
            this.money[currency] -= amount;
            console.log(`${currency}: ${this.money[currency]} (removed ${amount})`);
            return true;
        } else {
            console.warn(`Not enough ${currency}. Required: ${amount}, Available: ${this.money[currency]}`);
            return false;
        }
    }
    isitemInInventory(itemId) {
        return this.items.some(i => i.id === itemId);
    }
    isenoughMoney(item) {
        const needsO2 = item.price_O2 !== undefined && item.price_O2 > 0;
        const needsCO2 = item.price_CO2 !== undefined && item.price_CO2 > 0;
        
        // Si l'item nécessite les deux devises
        if (needsO2 && needsCO2) {
            return this.money.O2 >= item.price_O2 && this.money.CO2 >= item.price_CO2;
        }
        // Si l'item nécessite uniquement O2
        else if (needsO2) {
            return this.money.O2 >= item.price_O2;
        }
        // Si l'item nécessite uniquement CO2
        else if (needsCO2) {
            return this.money.CO2 >= item.price_CO2;
        }
        // Si aucun prix n'est défini, l'item est gratuit
        return true;
    }
    getItems() {
        return this.items;
    }
    getMoney() {
        return this.money;
    }
}
export const inventoryManager = new InventoryManager();