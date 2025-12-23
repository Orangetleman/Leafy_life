import { ITEMS } from "../../data/items.js";
import { ShopItemButton } from "../../components/button/ShopItemButton.js";
import { openBuyModal } from "../../components/modal/modal.js";

export default class ShopHome {
    constructor(data = {}) {
        this.type = data.type || "classic";
        this.biome = data.biome || null;
    }

    render() {
        const game = document.getElementById("game");
        
        game.innerHTML = `
            <div class="shop-container">
                
                <!-- HEADER (recherche + monnaies) -->
                <div class="shop-header">
                    <input type="text" placeholder="🔍 Rechercher..." class="shop-search">
                    <div class="player-currency">
                        <div class="currency-badge o2">120 O2</div>
                        <div class="currency-badge co2">85 CO2</div>
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

        // Récupération de la zone liste
        const shopList = document.getElementById("shop-list");
        const items = this.type === "wandering" ? getWanderingShopItems(this.biome) : getClassicShopItems();

        // Ajout des items
        ITEMS.forEach(item => {
            const itemButton = ShopItemButton(item, (itm) => {
                openBuyModal(itm, (confirmedItem) => {
                    console.log(`Achat confirmé pour l'item : ${confirmedItem.name}`);
                    // plus tard : gérer l'achat (vérif monnaie, ajout inventaire, etc)
                });
            });
            shopList.appendChild(itemButton);
        });
    }
}