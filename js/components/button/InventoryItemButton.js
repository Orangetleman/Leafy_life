// Variable partagée pour tracker le bouton de type actuellement actif
let activeTypeButton = null;

export function InventoryItemButton(item, onClick = null) {
    const button = document.createElement("button");
    button.className = "inventory-item-btn";
    button.type = "button";
    button.innerHTML = `<img src="${item.icon}" alt="${item.name}">`;
    button.addEventListener("click", onClick);
    return button;
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
        button.classList.remove("active");
        button.classList.remove("hover");
    });

    button.addEventListener("mouseenter", () => {
        button.classList.add("hover");
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