export function openBuyModal(item, onConfirm) {
    // Overlay
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";

    // Modal
    const modal = document.createElement("div");
    modal.className = "modal";

    modal.innerHTML = `
        <h3>Confirmer l'achat</h3>

        <div id="modal-item">
            <div id="shop-item-icon"><img src="${item.icon}" alt="${item.name}"></div>
            <span>${item.name}</span>
        </div>

        <div id="modal-prices">
            ${item.price_O2 !== undefined ? `<div class="price-badge price-o2">${item.price_O2} O2</div>` : ""}
            ${item.price_CO2 !== undefined ? `<div class="price-badge price-co2">${item.price_CO2} CO2</div>` : ""}
        </div>

        <div class="modal-actions">
            <button class="btn-cancel">Annuler</button>
            <button class="btn-confirm">Acheter</button>
        </div>
    `;

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    // Fermeture
    overlay.querySelector(".btn-cancel").onclick = () => overlay.remove();

    // Confirmation
    overlay.querySelector(".btn-confirm").onclick = () => {
        overlay.remove();
        if (onConfirm) onConfirm(item);
    };
}
