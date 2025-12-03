import { LEAFS } from "../../data/leafs.js";

export const LeafManager = {
    owned: [],

    unlock(id) {
        const leaf = LEAFS.find(l => l.id === id);
        if (leaf) this.owned.push(leaf);
    }
}