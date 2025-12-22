import { LeafManager } from "../../gameplay/leafs/leafManager.js";
import { Router } from "../../router.js";

export default class LeafsHome {
    render() {
        console.log("Leafs:", LeafManager.owned);
        const game = document.getElementById("game");
        game.innerHTML = `
            <h1>Leafs</h1>
            <p>Voici tes leafs</p>
        `;
    }
}
