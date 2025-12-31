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
    removeMoney(currency, amount = 1) {
        console.warn({[currency]: amount})
        const itemIndex = this.money.findIndex(i => i.id === itemId);
        if (this.isenoughMoney({[currency]: amount})) {
            currency === "O2" ? this.money.O2-=amount : currency === "CO2" ? this.money.CO2-=amount : this.money.CO2 = this.money.CO2
            console.log(this.money[currency])
        } else {
            console.warn(`Not enough ${currency}.`);
        }
    }
    isitemInInventory(itemId) {
        return this.items.some(i => i.id === itemId);
    }
    isenoughMoney(amount) {
        const existingMoneyO2 = this.money.hasOwnProperty("O2");
        const existingMoneyCO2 = this.money.hasOwnProperty("CO2");
        const existingPriceO2 = amount.price_O2 ? true : false;
        const existingPriceCO2 = amount.price_CO2 ? true : false;
        if ( existingMoneyO2 && existingMoneyCO2 && existingPriceO2 && existingPriceCO2 ) {
            return this.money.O2 >= amount.price_O2 && this.money.CO2 >= amount.price_CO2;
        } else if ( existingMoneyO2 && existingPriceO2 ) {
            return this.money.O2 >= amount.price_O2;
        } else if ( existingMoneyCO2 && existingPriceCO2) {
            return this.money.CO2 >= amount.price_CO2;
        }
    }
    getItems() {
        return this.items;
    }
    getMoney() {
        return this.money;
    }
}
export const inventoryManager = new InventoryManager();