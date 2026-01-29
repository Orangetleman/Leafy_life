import { Router } from "./router.js";
import { renderNavbar } from "./screens/navigation/navbar.js";
import { leafManager } from "./gameplay/leafs/leafManager.js";

document.addEventListener("DOMContentLoaded", () => {
    Router.navigate("leafs/leafsHome", { leafManager: leafManager });
});
renderNavbar();
