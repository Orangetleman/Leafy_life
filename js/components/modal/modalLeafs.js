import { createBadge } from "../button/LeafButton.js";
import { LEAFS_TYPE } from "../../data/leafs.js";
import { BIOMES } from "../../data/planets.js";
import { ITEMS } from "../../data/items.js";

export function openLeafModal(leaf) {
    // Overlay
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";

    // Modal
    const modal = document.createElement("div");
    modal.className = "modal";
    modal.id = "leaf-modal";
    
    modal.innerHTML = `
        <button id="leaf-modal-close-btn">Fermer</button>
        <div id="leaf-modal-info">
            <div  id="leaf-modal-img"><img src="${leaf.img}" alt="${leaf.name}"></div>
            <div id="leaf-modal-infos">
                <p><strong>Nom:</strong> ${leaf.name}</p>
                <p><strong>Biome:</strong> ${BIOMES[leaf.biome].name}</p>
                <p><strong>Type:</strong> ${LEAFS_TYPE[leaf.type].name}</p>
                <p><strong>Rareté:</strong> ${leaf.rarity}</p>
                <p><strong>Espèce:</strong> ${leaf.species}</p>
            </div>
        </div>
        <div id="leaf-modal-level" class="leaf-modal-stats"></div>
        <div id="leaf-modal-hp" class="leaf-modal-stats"></div>
        <div id="leaf-modal-nutrients" class="leaf-modal-stats"></div>
        <div id="leaf-modal-hydration" class="leaf-modal-stats"></div>
        <div id="leaf-modal-attack" class="leaf-modal-stats"></div>
        </div>
    `;
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Remplir les stats avec des badges
    statDisplay(leaf, "level", "Niveau", leaf.competence_lvl);
    statDisplay(leaf, "hp", "Points de vie", leaf.hp);
    statDisplay(leaf, "nutrients", "Nourriture", leaf.nutrients);
    statDisplay(leaf, "hydration", "Hydratation", leaf.hydration);
    statDisplay(leaf, "attack", "Attaque", leaf.atk);

    // Fermer avec le bouton Fermer
    const closeBtn = modal.querySelector("#leaf-modal-close-btn");
    closeBtn.addEventListener("click", () => {
        overlay.remove();
    });
    
    // Fermer en cliquant en dehors du modal
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) {
            overlay.remove();
        }
    });
}

function statDisplay(leaf, statName, frStatName, value) {
    console.log("Displaying stat :", statName,"of", leaf.name, "with value:", value);
    const statElement = document.querySelector(`#leaf-modal-${statName}`);
    if (statElement) {
        // Créer un conteneur pour le nom et la barre
        const statContainer = document.createElement("div");
        statContainer.className = "stat-display-container";
        
        // Ajouter le nom de la stat
        const nameElement = document.createElement("div");
        nameElement.className = "stat-name";
        nameElement.textContent = `${frStatName}`;
        statContainer.appendChild(nameElement);
        
        // Ajouter la barre ou la valeur
        if (statName === "level") {
            const valueElement = document.createElement("div");
            valueElement.id = `leaf-modal-${statName}-value`;
            valueElement.className = "stat-value-level";
            valueElement.textContent = value;
            statContainer.appendChild(valueElement);
        } else {
            statContainer.appendChild(createProgressBar(leaf, statName, value, 100));
        }
        
        statElement.appendChild(statContainer);

        // Ajouter le badge correspondant
        const badge = createBadge(itemTypeSelector(leaf, statName), "boost", () => { /* Ajouter logique de boost / de ravitaillement */ });
        statElement.appendChild(badge);
    }
}
function itemTypeSelector(leaf, statName) {
    console.log("Selecting item for stat:", statName, "of leaf:", leaf.name, "who is type:", leaf.species, "and regime:", leaf.regime);
    switch (statName) {
        case "nutrients":
            switch (leaf.species) {
                case "plant":
                    return ITEMS["2"]; // Fertilizer 🌱
                case "animal":
                    switch (leaf.regime) {
                        case "herbivore":
                            return ITEMS["4"]; // Grass 🥗
                        case "carnivore":
                            return ITEMS["3"]; // Meat 🍖
                    }
            }
        case "hydration":
            return ITEMS["1"]; // Water 💧
        case "hp":
            switch (leaf.species) {
                case "plant":
                    return ITEMS["5"]; // Mineral Water 💧
                case "animal":
                    return ITEMS["6"]; // Bandage 🩹
            }
        case "level":
            return ITEMS["13"]; // Book of knowledge 🌟
        case "attack":
            return ITEMS["11"]; // Attack boost potion 🌟
    }
    console.log("No item found for stat:", statName);
}
function createProgressBar(leaf, statName, value, maxValue, boostvalue = 10, color = "green", boostColor = "lightgreen") {
    const finalValue = Math.min(value + boostvalue, maxValue);
    const barContainerContainer = document.createElement("div");
    barContainerContainer.className = "progress-bar-container-wrapper";
    
    const barContainer = document.createElement("div");
    barContainer.className = "progress-bar-container";
    barContainer.id = `leaf-modal-${statName}-bar`;
    
    const bar = document.createElement("div");
    bar.className = "progress-bar";
    const percentage = (value / maxValue) * 100;
    bar.style.width = `${percentage}%`;
    bar.style.backgroundColor = color;
    barContainer.appendChild(bar);
    
    if (finalValue > value) {
        const boostBar = document.createElement("div");
        boostBar.className = "progress-bar-boost";
        const boostPercentage = (boostvalue / maxValue) * 100;
        boostBar.style.width = `${boostPercentage}%`;
        boostBar.style.backgroundColor = boostColor;
        barContainer.appendChild(boostBar);
    }
    
    barContainerContainer.appendChild(barContainer);
    
    // Ajouter le texte numérique sous la barre
    const textContainer = document.createElement("div");
    textContainer.className = "progress-bar-text";
    textContainer.textContent = `${finalValue} / ${maxValue}`;
    barContainerContainer.appendChild(textContainer);
    
    return barContainerContainer;
}
function refreshProgressBar(leaf, statName, value, maxValue, boostvalue = 0) {
    const barContainer = document.querySelector(`#leaf-modal-${statName} .progress-bar-container`);
    if (barContainer) {
        const bar = barContainer.querySelector(".progress-bar");
        const percentage = (value / maxValue) * 100;
        bar.style.width = `${percentage}%`;
        const boostBar = barContainer.querySelector(".progress-bar-boost");
        if (boostBar) {
            const boostPercentage = (boostvalue / maxValue) * 100;
            boostBar.style.width = `${boostPercentage}%`;
        }
    }
}