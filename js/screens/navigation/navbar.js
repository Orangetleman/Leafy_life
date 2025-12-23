import { Router } from "../../router.js";

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

    document.getElementById("btnLeafs").onclick = () => Router.navigate("leafs/leafsHome");
    document.getElementById("btnShop").onclick = () => Router.navigate("shop/shopHome", { type: "classic" });
    document.getElementById("btnInventory").onclick = () => Router.navigate("inventory/inventoryHome");
    document.getElementById("btnPlanet").onclick = () => Router.navigate("planet/planetHome");
}
