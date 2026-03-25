import { LeafStat } from "./leafStats.js";
export class LeafManager {
    constructor() {
        this.owned = [];
    }

    addLeaf(leaf) {
        const existingLeaf = this.owned.find(l => l.id === leaf.id);
        if (existingLeaf) {
            console.log(`Leaf déjà possédé : ${leaf.name}`);
            return;
        }
        this.owned.push(new LeafStat(leaf));
        console.log(`Leaf ajouté : ${leaf.name} dans la collection : `, this.owned);
    }
}
export const leafManager = new LeafManager();