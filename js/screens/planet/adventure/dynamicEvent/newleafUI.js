import { giveNewLeaf } from "../../../../gameplay/adventure/newLeafManager.js";

export default class NewLeafUI {
    render() {
        giveNewLeaf(this.data.leafId);
        console.log("You unlocked a new leaf!");
    }
}
