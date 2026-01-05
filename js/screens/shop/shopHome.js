import { ShopItemButton } from "../../components/button/ShopItemButton.js";
import { openBuyModal } from "../../components/modal/modalShop.js";
import { is_search_mode } from "../../utils/helpers.js";
import { inventoryManager } from "../../gameplay/inventory/inventoryManager.js";
import { classicShopManager, WANDERINGSHOPS } from "../../gameplay/shop/shopManager.js";
import { Router } from "../../router.js"

export default class ShopHome {
    constructor(data = {}) {
        this.type = data.type || "classic";
        this.biome = data.biome || "plain";
        this.mustReload = data.mustReload || false;
        this.searchQuery = "";
        if (this.type === "classic") {
            this.shop = classicShopManager
        } else if (this.type === "wandering") {
            this.shop = WANDERINGSHOPS.find((i) => i.biome === this.biome)?.shop;
        }
        if (this.mustReload) {
            this.shop.reloadWanderingShopItems()
        }
    }

    render() {
        const game = document.getElementById("game");
        
        game.innerHTML = `
            <div class="shop-container">
                
                <!-- HEADER (recherche + monnaies) -->
                <div class="shop-header">
                    <input type="text" placeholder="🔍 Rechercher..." id="shop-search" class="search-bar">
                    <div class="player-currency">
                        <div class="currency-badge o2">${inventoryManager.money.O2} O2</div>
                        <div class="currency-badge co2">${inventoryManager.money.CO2} CO2</div>
                    </div>
                </div>

                <!-- TITRE -->
                <div class="shop-title">
                    <h2>${this.type === "wandering" ? "Shop itinérant" : "Shop"}</h2>
                </div>

                <!-- LISTE SCROLLABLE -->
                <div class="shop-list" id="shop-list">
                </div>

            </div>
        `;

        // Récupération de la barre de recherche
        const searchInput = document.getElementById("shop-search");
        // Récupération de la zone liste
        const shopList = document.getElementById("shop-list");

        searchInput.addEventListener("focus", () => {
            shopList.innerHTML = "";
        });
        searchInput.addEventListener("blur", () => {
            this.refreshShopList(shopList);
        });

        searchInput.addEventListener("input", (e) => {
            this.searchQuery = e.target.value;
            this.refreshShopList(shopList);
        });
        this.refreshShopList(shopList);
    }
    refreshShopList(shopList) {
        shopList.innerHTML = "";
        // vérification du type de recherche
        const isTagSearch = this.searchQuery.startsWith("#");
        const searchTag = isTagSearch ? this.searchQuery.slice(1).toLowerCase() : this.searchQuery.toLowerCase();
        // Filtrer les items selon le mode de shop puis selon la recherche
        const items = this.shop.stock
        const itemsToDisplay = items.filter(item => {
            if (is_search_mode()) {
                if (isTagSearch) {
                    return item.tags && item.tags.some(tag => tag.toLowerCase().includes(searchTag));
                }
                return item.name.toLowerCase().includes(searchTag);
            }
            return item.name.toLowerCase().includes(searchTag);
        });

        itemsToDisplay.forEach(item => {
            const itemButton = ShopItemButton(item, (itm) => {
                openBuyModal(itm, this.shop, (confirmedItem) => {
                    this.shop.buyItem(confirmedItem)
                    console.warn(`O2 : ${inventoryManager.money.O2}, CO2 : ${inventoryManager.money.CO2}`)
                    Router.navigate("shop/shopHome", { type: this.type, inventoryManager: inventoryManager })
                });
            });
            shopList.appendChild(itemButton);
        });
    }
}