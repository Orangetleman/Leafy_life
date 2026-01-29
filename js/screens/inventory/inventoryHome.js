import { TYPES } from "../../data/items.js";
import { InventoryItemButton, InventoryTypeButton } from "../../components/button/InventoryItemButton.js";
import { openItemInventoryModal } from "../../components/modal/modalInventory.js";
import { is_search_mode } from "../../utils/helpers.js";

export default class InventoryHome {
    constructor(data = {}) {
        this.inventory = data.inventory;
        this.searchQuery = "";
        this.activeType = null;
        this.temp_type = null;
    }
    render() {
        console.log("Inventory:", this.inventory.getItems());
        const game = document.getElementById("game");
        game.innerHTML = `
            <div class="inventory-container">
                <div class="inventory-header">
                    <div id="inventory-header-title-box">
                        <div id="inventory-header-title"><h2>Inventory</h2></div>
                    </div>
                    <div class="inventory-type-list" id="inventory-type-list"></div>
                    <div id="inventory-search-box">
                        <input type="text" placeholder="🔍 Rechercher..." id="inventory-search" class="search-bar">
                    </div>
                </div>
                <div class="inventory-list" id="inventory-list"></div>
            </div>
        `;
        // récupération de la zone header
        const inventoryHeader = document.getElementById("inventory-type-list");
        // récupération de la zone liste
        const inventoryList = document.getElementById("inventory-list");
        const searchInput = document.getElementById("inventory-search");
        
        // Événement focus : désactiver le filtre de type et vider la liste
        searchInput.addEventListener("focus", () => {
            this.temp_type = this.activeType;
            this.activeType = null;
            inventoryList.innerHTML = "";
        });
        searchInput.addEventListener("blur", () => {
            this.activeType = this.temp_type;
            this.refreshItemList(inventoryList);
        });
        
        // Événement input : mettre à jour la recherche et actualiser la liste
        searchInput.addEventListener("input", (e) => {
            this.searchQuery = e.target.value;
            this.refreshItemList(inventoryList);
        });
        
        // Ajout des boutons de type
        TYPES.forEach(type => {
            const typeButton = InventoryTypeButton(type, () => {
                this.activeType = type;
                this.refreshItemList(inventoryList);
            });
            inventoryHeader.appendChild(typeButton);
        });
    }

    refreshItemList(inventoryList) {
        inventoryList.innerHTML = ""; // Clear les items affichés
        
        // Vérifier si on recherche par tag (commence par #)
        const isTagSearch = this.searchQuery.startsWith("#");
        const searchTag = isTagSearch ? this.searchQuery.slice(1).toLowerCase() : "";
        
        // Filtrer les items selon la recherche et le type
        const itemsToDisplay = this.inventory.getItems().filter(item => {
            // Si on est en mode recherche
            if (is_search_mode()) {
                // Recherche par tag
                if (isTagSearch) {
                    return item.tags && item.tags.some(tag => tag.toLowerCase().includes(searchTag));
                }
                // Recherche par nom
                return item.name.toLowerCase().includes(this.searchQuery.toLowerCase());
            }
            // Sinon, filtrer par type si un type est sélectionné
            if (this.activeType) {
                return item.use === this.activeType.name;
            }
            // Par défaut, afficher rien
            return false;
        });
        
        // Créer les boutons pour les items filtrés
        itemsToDisplay.forEach(item => {
            const itemButton = InventoryItemButton(item, () => {
                openItemInventoryModal(item);
            });
            inventoryList.appendChild(itemButton);
        });
        console.log(`Affichage de ${itemsToDisplay.length} item(s)`);
    }
}