import { generateEvent } from "../../utils/eventGenerator.js";
import { Router } from "../../router.js";

export default class AdventureUI {
    constructor(data) {
        this.biome = data.biome;
    }

    render() {
        const event = generateEvent(this.biome);
        Router.navigate(`planet/adventure/eventView`, { event });
    }

    destroy() {}
}
