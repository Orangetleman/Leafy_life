export function openItemInventoryModal(item, onClose) {
    // Overlay
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";

    // Modal
    const modal = document.createElement("div");
    modal.className = "modal";

    modal.innerHTML = `
        <div id="modal-inventory-cadre">
            <button class="btn-cancel" id="modal-inventory-btn-cancel">Fermer</button>
            <div id="modal-inventory-item-details">
                <div id="modal-inventory-item-icon"><img src="${item.icon}" alt="${item.name}"></div>
                <div id="modal-inventory-item-info">
                    <h3 id="modal-inventory-item-name">${item.name}</h3>
                    <p>Quantité : ${item.amount}</p>
                    <p>Type : ${item.use}</p>
                </div>
            </div>
            <p id="modal-inventory-item-description">${item.description}</p>
        </div>
    `;

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    // Fermeture
    overlay.querySelector(".btn-cancel").onclick = () => {
        overlay.remove();
        if (onClose) onClose();
    };

    // Fermer en cliquant en dehors du modal
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) {
            overlay.remove();
        };
    });
}