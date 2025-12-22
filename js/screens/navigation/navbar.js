import { Router } from "../../router.js";

export function setupNavbar() {
    document.getElementById("btnLeafs").onclick = () => Router.navigate("leafs/leafsHome");
    document.getElementById("btnShop").onclick = () => Router.navigate("shop/shopHome");
    document.getElementById("btnInventory").onclick = () => Router.navigate("inventory/inventoryHome");
    document.getElementById("btnPlanet").onclick = () => Router.navigate("planet/planetHome");
}