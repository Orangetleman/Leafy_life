// Modale d'erreur temporaire
export function openErrorModal(message, duration = 10000) {
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";
    
    const modal = document.createElement("div");
    modal.className = "modal modal-error";
    
    const title = document.createElement("h3");
    title.textContent = "Erreur";
    title.style.fontFamily = "var(--comic-font)";
    
    const messageDiv = document.createElement("p");
    messageDiv.textContent = message;
    messageDiv.style.margin = "1rem 0";
    messageDiv.style.fontFamily = "var(--comic-font)";
    
    const closeBtn = document.createElement("button");
    closeBtn.className = "btn-cancel";
    closeBtn.textContent = "Fermer";
    closeBtn.style.marginTop = "1rem";
    closeBtn.style.borderRadius = "1em";
    
    modal.appendChild(title);
    modal.appendChild(messageDiv);
    modal.appendChild(closeBtn);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Fermer au clic
    closeBtn.onclick = () => overlay.remove();
    
    // Fermer automatiquement après le délai
    setTimeout(() => {
        if (overlay.parentElement) {
            overlay.remove();
        }
    }, duration);
}

export function openBuyModal(item, shop, inventoryManager, onConfirm) {
    // Overlay
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";

    // Modal
    const modal = document.createElement("div");
    modal.className = "modal";
    modal.id = "shop-buy-modal";

    // Contenu du Modal
        // Titre
        const title = document.createElement("h3");
        title.textContent = "Confirmer l'achat";

        // Info item
        const itemInfo = document.createElement("div");
        itemInfo.id = "modal-item";
        itemInfo.innerHTML = `
            <div id="shop-item-icon"><img src="${item.icon}" alt="${item.name}"></div>
            <div id="shop-item-info">
                <span>${item.name}</span>
                <span>Remaining : ${shop.stock.find((i) => i.name === item.name).amount}</span>
            </div>
        `;

    // Actions
    const actions = document.createElement("div");
    actions.id = "shop-modal-action";
        const amountLabel = document.createElement("div");
        amountLabel.id = "shop-amount-label";
        amountLabel.textContent = "Quantité :";
        actions.appendChild(amountLabel);
        const amountSelection = document.createElement("div");
        amountSelection.id = "shop-amount-selection";
            const removeBtn = document.createElement("button");
            removeBtn.id = "shop-remove-amount-btn";
            removeBtn.textContent = "-";
            const amountDisplay = document.createElement("span");
            amountDisplay.id = "shop-amount-display";
            amountDisplay.textContent = "1";
            const addBtn = document.createElement("button");
            addBtn.id = "shop-add-amount-btn";
            addBtn.textContent = "+";
            amountSelection.appendChild(removeBtn);
            amountSelection.appendChild(amountDisplay);
            amountSelection.appendChild(addBtn);
        actions.appendChild(amountSelection);

        // Prix
        const prices = document.createElement("div");
        prices.id = "modal-prices";
            if (item.price_O2 !== undefined) {
                const priceO2 = document.createElement("div");
                priceO2.className = "price-badge price-o2";
                priceO2.textContent = `${item.price_O2} O2`;
                prices.appendChild(priceO2);
            }
            if (item.price_CO2 !== undefined) {
                const priceCO2 = document.createElement("div");
                priceCO2.textContent = `${item.price_CO2} CO2`;
                priceCO2.className = "price-badge price-co2";
                prices.appendChild(priceCO2);
            }
        actions.appendChild(prices);

        // Boutons Annuler / Confirmer
        const confirmButtons = document.createElement("div");
        confirmButtons.className = "modal-actions";
            const cancelButton = document.createElement("button");
            cancelButton.className = "btn-cancel";
            cancelButton.textContent = "Annuler";
            const confirmButton = document.createElement("button");
            confirmButton.className = "btn-confirm";
            confirmButton.textContent = "Acheter";
            confirmButtons.appendChild(cancelButton);
            confirmButtons.appendChild(confirmButton);
        actions.appendChild(confirmButtons);

    // Assemblage finale
        
    modal.appendChild(title);
    modal.appendChild(itemInfo);
    modal.appendChild(actions);

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    // Gestion de la quantité
    let currentAmount = 1;
    let currentO2Price = item.price_O2 !== undefined ? item.price_O2 : 0;
    let currentCO2Price = item.price_CO2 !== undefined ? item.price_CO2 : 0;
    const maxAmount = shop.stock.find((i) => i.name === item.name).amount;
    const maxO2Affordable = currentO2Price > 0 ? Math.floor(inventoryManager.money.O2 / currentO2Price) : Infinity;
    const maxCO2Affordable = currentCO2Price > 0 ? Math.floor(inventoryManager.money.CO2 / currentCO2Price) : Infinity;
    const updateAmountDisplay = () => {
        amountDisplay.textContent = currentAmount;
        // Mettre à jour les prix
        if (item.price_O2 !== undefined && item.price_O2 > 0) {
            prices.querySelector(".price-o2").textContent = `${currentO2Price * currentAmount} O2`;
        }
        if (item.price_CO2 !== undefined && item.price_CO2 > 0) {
            prices.querySelector(".price-co2").textContent = `${currentCO2Price * currentAmount} CO2`;
        }
    };

    removeBtn.onclick = () => {
        if (currentAmount > 1) {
            currentAmount--;
            updateAmountDisplay();
        }
    };
    addBtn.onclick = () => {
        if (currentAmount < maxAmount && currentAmount < maxO2Affordable && currentAmount < maxCO2Affordable) {
            currentAmount++;
            updateAmountDisplay();
        }
    };
    // Fermeture
    overlay.querySelector(".btn-cancel").onclick = () => overlay.remove();

    // Confirmation
    overlay.querySelector(".btn-confirm").onclick = () => {
        overlay.remove();
        if (onConfirm) onConfirm(item, currentAmount);
    };
}
