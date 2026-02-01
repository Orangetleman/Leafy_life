export const LEAFS = {
    // id, name, type, rarity, atk, hp, species, regime (if animal), biome, competence_lvl, img

    // Animals
    0: { id: 0, name: "grenouille", type: 0, rarity: "default", atk: 4, hp: 5, species: "animal", regime: "carnivore", biome: 1, competence_lvl: 0, img: "assets/imgs/leafs/Leaf_frog.png" },
    2: { id: 2, name: "mouton", type : 2, rarity: "default", atk: 2, hp: 4, species: "animal", regime:"herbivore", biome: 1, competence_lvl: 0, img: "assets/imgs/leafs/Leaf_sheep.png" },
    3: { id: 3, name: "abeille", type : 2, rarity: "default", atk: 3, hp: 4, species: "animal", regime:"herbivore", biome: 1, competence_lvl: 0, img:"assets/imgs/leafs/Leaf_bee.png" },
    5: { id : 5 , name :"loup", type :1 , rarity :"default", atk :6 , hp :2 , species :"animal", regime:"carnivore", biome :2 , competence_lvl :0 , img :"assets/imgs/leafs/Leaf_wolf.png"},
    8: { id: 8, name: "poisson", type : 1, rarity: "default", atk: 5, hp: 4, species: "animal", regime:"herbivore", biome: 3, competence_lvl: 0, img: "assets/imgs/leafs/Leaf_fish.png" },
    9: { id: 9, name: "chèvre", type :3 , rarity : "default", atk :2 , hp :10 , species :"animal", regime:"herbivore", biome :4 , competence_lvl :0 , img :"assets/imgs/leafs/Leaf_goat.png" },
    12: { id: 12, name: "aigle", type : 1, rarity: "default", atk: 4, hp: 6, species: "animal", regime:"carnivore", biome: 3, competence_lvl: 0, img: "assets/imgs/leafs/Leaf_eagle.png" },
    13: { id: 13, name: "ours", type :3 , rarity : "default", atk :7 , hp :12 , species :"animal", regime:"carnivore", biome :4 , competence_lvl :0 , img :"assets/imgs/leafs/Leaf_bear.png" },
    // Plants
    1: { id: 1, name: "pissenlit", type : 1, rarity: "default", atk: 5, hp: 4, species: "plant", biome: 1, competence_lvl: 0, img: "assets/imgs/leafs/Leaf_dandelion.png" },
    4: { id: 4 , name : "sapin", type : 3 , rarity : "default", atk : 3 , hp : 8 , species: "plant", biome : 2 , competence_lvl : 0 , img: "assets/imgs/leafs/Leaf_pine.png"},
    6: { id: 6, name: "fraisier", type : 2, rarity: "default", atk: 3, hp: 6, species: "plant", biome: 2, competence_lvl: 0, img: "assets/imgs/leafs/Leaf_strawberry.png" },
    7: { id: 7, name: "roseaux", type : 3, rarity: "default", atk: 3, hp: 8, species: "plant", biome: 3, competence_lvl: 0, img: "assets/imgs/leafs/Leaf_reeds.png" },
    10:{ id :10 , name :"arbuste", type :3 , rarity :"default", atk :1 , hp :12 , species :"plant", biome :4 , competence_lvl :0 , img :"assets/imgs/leafs/Leaf_bush.png" },
    11:{ id: 11, name: "nénuphare", type : 2, rarity: "default", atk: 1, hp: 4, species: "plant", biome: 3, competence_lvl: 0, img: "assets/imgs/leafs/Leaf_lilypad.png" },
};

export const LEAFS_TYPE = [
    { id: 0, name: "default", icon: "assets/imgs/icons/leaf_type_default.png" },
    { id: 1, name: "attacker", icon: "assets/imgs/icons/leaf_type_attacker.png" },
    { id: 2, name: "healer", icon: "assets/imgs/icons/leaf_type_healer.png" },
    { id: 3, name: "tank", icon: "assets/imgs/icons/leaf_type_tank.png" }
];