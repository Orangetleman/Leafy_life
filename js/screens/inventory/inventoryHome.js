import { ITEMS, TYPES } from "../../data/items.js";
import { InventoryItemButton, InventoryTypeButton } from "../../components/button/InventoryItemButton.js";
import { openItemInventoryModal } from "../../components/modal/modalInventory.js";

export default class InventoryHome {
    constructor(data = {}) {
        this.inventory = data.inventory;
    }
    render() {
        console.log("Inventory:", ITEMS);
        const game = document.getElementById("game");
        game.innerHTML = `
            <div class="inventory-container">
                <div class="inventory-header" id="inventory-header"></div>
                <input type="text" placeholder="🔍 Rechercher..." class="inventory-search">
                <div class="inventory-list" id="inventory-list"></div>
            </div>
        `;
        // récupération de la zone header
        const inventoryHeader = document.getElementById("inventory-header");
        // récupération de la zone liste
        const inventoryList = document.getElementById("inventory-list");
        
        // Test inventaire:
            this.inventory.appendItem(ITEMS[0]);
            this.inventory.appendItem(ITEMS[1]);
            this.inventory.appendItem(ITEMS[2]);
            this.inventory.appendItem(ITEMS[0]);
            this.inventory.appendItem(ITEMS[1]);
            this.inventory.appendItem(ITEMS[2]);
            this.inventory.appendItem(ITEMS[4]);
            this.inventory.appendItem(ITEMS[5]);
            this.inventory.appendItem(ITEMS[6]);
            this.inventory.appendItem(ITEMS[7]);
            this.inventory.appendItem(ITEMS[8]);
            this.inventory.appendItem(ITEMS[9]);
        // Ajout des boutons de type
        TYPES.forEach(type => {
            const typeButton = InventoryTypeButton(type, () => {
                inventoryList.innerHTML = ""; // Clear les items affichés
                let itemsType = type.name;
                // Ajout des boutons items
                this.inventory.getItems().forEach(item => {
                    if (item.use === itemsType) {
                    const itemButton = InventoryItemButton(item, () => {
                        openItemInventoryModal(item);
                        console.log(`Item cliqué : ${item.name}`);
                    });
                    inventoryList.appendChild(itemButton);
                    }
                    else {
                        console.log(`Item non affiché : ${item.name} de type ${item.use} pour le type ${itemsType}`);
                    }
                });
                console.log(`Filtrer par type : ${type.name}`);
            });
            inventoryHeader.appendChild(typeButton);
        });
    }
}
