import { Router } from "../../router.js";
import { PLANETS } from "../../data/planets.js";

export default class PlanetHome {
    render() {
        Router.navigate("planet/adventure/adventureHome", {
            biome: PLANETS[0].biomes[0]
        });
    }
}
