import { Router } from "../../router.js";
import { PLANETS } from "../../data/planets.js";

export default class PlanetHome {
    render() {
        const game = document.getElementById("game");
        game.innerHTML = `
            <h1>${PLANETS[0].name}</h1>
            <button id="explore">Explorer</button>
        `;

        document.getElementById("explore").onclick = () => {
            Router.navigate("planet/adventure/adventureHome", {
                biome: PLANETS[0].biomes[0]
            });
        };
    }
}
