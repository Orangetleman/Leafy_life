export class LeafStat {
    constructor(leaf) {
        this.id = leaf.id;
        this.name = leaf.name;
        this.type = leaf.type;
        this.rarity = leaf.rarity;
        this.atk = leaf.atk;
        this.hp = leaf.hp;
        this.species = leaf.species;
        this.biome = leaf.biome;
        this.competence_lvl = leaf.competence_lvl;
        this.img = leaf.img;
        this.nutrients = 100;
        this.hydration = 100;
        this.regime = leaf.regime || null;
    }
}