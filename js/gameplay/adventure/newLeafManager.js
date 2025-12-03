import { LeafManager } from "../leafs/leafManager.js";

export function giveNewLeaf(id) {
    LeafManager.unlock(id);
}
