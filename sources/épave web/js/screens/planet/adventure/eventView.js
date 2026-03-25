import { Router } from "../../../router.js";

export default class EventView {
    render() {
        const event = this.data.event;

        if (event.type === "enemy") Router.navigate("planet/adventure/dynamicEvent/combatUI", event.data);
        else if (event.type === "npc") Router.navigate("planet/adventure/dynamicEvent/npcUI", event.data);
        else if (event.type === "new_leaf") Router.navigate("planet/adventure/dynamicEvent/newLeafUI", event.data);
    }
}
