import { Router } from "../../router.js";
import { inventoryManager } from "../../gameplay/inventory/inventoryManager.js";
import { ITEMS } from "../../data/items.js";

export function renderNavbar() {
    const navbar = document.createElement("div");
    navbar.id = "navbar";

    navbar.innerHTML = `
        <button id="btnLeafs">Leafs</button>
        <button id="btnShop">Shop</button>
        <button id="btnInventory">Inventory</button>
        <button id="btnPlanet">Planet</button>
    `;

    document.body.appendChild(navbar);

    // Test inventaire :
        inventoryManager.appendItem(ITEMS[0], 4);
        inventoryManager.appendItem(ITEMS[1], 2);
        inventoryManager.appendItem(ITEMS[2], 5);
        inventoryManager.appendItem(ITEMS[3], 3);
        inventoryManager.appendItem(ITEMS[4], 4);
        inventoryManager.appendItem(ITEMS[5], 2);
        inventoryManager.appendItem(ITEMS[6], 5);
        inventoryManager.appendItem(ITEMS[7], 3);
        inventoryManager.appendItem(ITEMS[8], 4);
        inventoryManager.appendItem(ITEMS[9], 2);
        inventoryManager.appendMoney("O2", 10000);
        inventoryManager.appendMoney("CO2", 10000);

    document.getElementById("btnLeafs").onclick = () => Router.navigate("leafs/leafsHome");
    document.getElementById("btnShop").onclick = () => Router.navigate("shop/shopHome", { type: "classic", inventoryManager: inventoryManager, mustReload: true });
    document.getElementById("btnInventory").onclick = () => Router.navigate("inventory/inventoryHome", { inventory: inventoryManager });
    document.getElementById("btnPlanet").onclick = () => Router.navigate("planet/planetHome");
}
