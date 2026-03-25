let plain = "plain";
let forest = "forest";
let lake = "lake";
let mountain = "mountain";

export const BIOMES = [
    {id: 1, name: plain, icon: "assets/imgs/icons/biome_plain.png"},
    {id: 2, name: forest, icon: "assets/imgs/icons/biome_forest.png"},
    {id: 3, name: lake, icon: "assets/imgs/icons/biome_lake.png"},
    {id: 4, name: mountain, icon: "assets/imgs/icons/biome_mountain.png"}
];
export const PLANETS = [
    { id: 1, name: "Earth", biomes: [BIOMES[0], BIOMES[1], BIOMES[2], BIOMES[3]] }
];