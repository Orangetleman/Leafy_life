import { Router } from "./router.js";
import { renderNavbar } from "./screens/navigation/navbar.js";

document.addEventListener("DOMContentLoaded", () => {
    Router.navigate("leafs/leafsHome");
});
renderNavbar();
