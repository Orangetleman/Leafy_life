import { rand } from "./helpers.js";
import { EVENTS } from "../data/event.js"

export function generateEvent(biome) {
    const pool = EVENTS[biome]
    const index = rand(0, pool.lengh -1);
    return pool[index]; //{type:"enemy" | "npc" | "new_leaf", data:{...}}
}