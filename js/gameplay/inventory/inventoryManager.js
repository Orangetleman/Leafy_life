export class InventoryManager {
    constructor() {
        this.items = [];
    }
    appendItem(item) {
        const existingItem = this.items.find(i => i.id === item.id);
        if (existingItem) {
            existingItem.amount += item.amount || 1;
        } else {
            this.items.push({ ...item, amount: item.amount || 1 });
        }
        console.log(`Item ajouté : ${item.name} (Total: ${this.items.find(i => i.id === item.id).amount})`);
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
    isitemInInventory(itemId) {
        return this.items.some(i => i.id === itemId);
    }
    getItems() {
        return this.items;
    }
}
export const inventoryManager = new InventoryManager();