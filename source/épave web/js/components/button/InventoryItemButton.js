// Variable partagée pour tracker le bouton de type actuellement actif
let activeTypeButton = null;

// Fonction pour créer et afficher un tooltip
function showTooltip(element, text) {
    // Enlever les anciens tooltips
    const oldTooltip = document.querySelector(".inventory-tooltip");
    if (oldTooltip) oldTooltip.remove();

    const tooltip = document.createElement("div");
    tooltip.className = "inventory-tooltip";
    tooltip.textContent = text;
    
    document.body.appendChild(tooltip);

    // Positionner le tooltip au niveau de la souris
    const rect = element.getBoundingClientRect();
    tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + "px";
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + "px";
}

function hideTooltip() {
    const tooltip = document.querySelector(".inventory-tooltip");
    if (tooltip) tooltip.remove();
}

export function InventoryItemButton(item, onClick = null) {
    const itemContainer = document.createElement("div");
    itemContainer.className = "inventory-item-btn-container";
        const button = document.createElement("button");
        button.className = "inventory-item-btn";
        button.type = "button";
        button.innerHTML = `<img src="${item.icon}" alt="${item.name}">`;
        button.addEventListener("click", onClick);
    itemContainer.appendChild(button);
    const amountBadge = document.createElement("div");
        amountBadge.className = "inventory-item-amount-badge";
        amountBadge.textContent = item.amount;
    itemContainer.appendChild(amountBadge);
    // Tooltip pour les items
    button.addEventListener("mouseenter", () => {
        showTooltip(button, item.name);
    });
    button.addEventListener("mouseleave", hideTooltip);
    
    return itemContainer;
}
export function InventoryTypeButton(type, onClick = null) {
    const button = document.createElement("button");
    button.className = "inventory-type-btn";
    button.type = "button";
    button.innerHTML = `<img src="${type.icon}" alt="${type.name}">`;
    
    button.addEventListener("mousedown", () => {
        button.classList.remove("hover");  // Enlever hover d'abord
        button.classList.add("active");
    });
    
    button.addEventListener("mouseup", () => {
        button.classList.remove("active");
        button.classList.add("hover");  // Remettre hover après
    });
    
    button.addEventListener("mouseleave", () => {
        hideTooltip();
        button.classList.remove("active");
        button.classList.remove("hover");
    });

    button.addEventListener("mouseenter", () => {
        button.classList.add("hover");
        showTooltip(button, type.name);
    });
    
    if (typeof onClick === "function") {
        button.addEventListener("click", () => {
            // Si un autre bouton était actif, le désactiver
            if (activeTypeButton !== null && activeTypeButton !== button) {
                activeTypeButton.classList.remove("while-active");
            }
            
            // Basculer l'état du bouton actuel
            if (button.classList.contains("while-active")) {
                button.classList.remove("while-active");
                activeTypeButton = null;
            } else {
                button.classList.add("while-active");
                activeTypeButton = button;
            }
            
            onClick();
        });
    }
    
    return button;
}