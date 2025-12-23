import { ITEMS } from "../../data/items.js";
export default class ShopHome {
    render() {
        console.log("Shop opened");
        const game = document.getElementById("game");
        game.innerHTML = `
            <div class="shop">
                <h2>Shop</h2>
                <ul>
                    ${ITEMS.map(item => `
                        <li>
                            ${item.name},
                            O2 : ${item.price_O2 ?? "-"},
                            CO2 : ${item.price_CO2 ?? "-"},
                            O2_s : ${item.specialprice_O2 ?? "-"},
                            CO2_s : ${item.specialprice_CO2 ?? "-"},
                            Spécial : ${item.is_special}
                        </li>
                    `).join("")}
                </ul>
            </div>
        `;
    }
}