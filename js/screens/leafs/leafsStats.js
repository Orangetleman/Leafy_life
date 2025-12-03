import { getLeafStats } from "../../gameplay/leafs/leafStats.js";

export default class LeafStats {
    render() {
        const stats = getLeafStats(this.data.leaf);
        console.log(stats);
    }
}
