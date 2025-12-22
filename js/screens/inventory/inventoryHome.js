import { ITEMS } from "../../data/items.js";

export default class InventoryHome {
    render() {
        console.log("Inventory:", ITEMS);
        const game = document.getElementById("game");
        game.innerHTML = `
            <div class="inventory">
                <h2>Inventory</h2>
                <ul>
                    ${ITEMS.map(item => `<li>${item.name}</li>`).join('')}
                </ul>
            </div>
        `;
    }
}
