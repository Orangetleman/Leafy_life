import { LeafManager } from "../../gameplay/leafs/leafManager.js";
import { Router } from "../../router.js";

export default class LeafsHome {
    render() {
        console.log("Leafs:", LeafManager.owned);
    }
}
