export function openItemInventoryModal(item, onClose) {
    // Overlay
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";

    // Modal
    const modal = document.createElement("div");
    modal.className = "modal";

    modal.innerHTML = `
        /*FLEX VERTICAL QUI CONTIENT BOUTON FERMER + (FLEX HORIZONTAL QUI CONTIENT L'ICON + (UN DIV VERTICAL QUI CONTIENT LE NOM + LA QUANTITÉ + LE TYPE)) + DESCRIPTION*/

        <div class="modal">
            <button class="btn-cancel">Fermer</button>
            <div id="inventory-item-details"> /* Flex horizontal */
                <div id="inventory-item-icon"><img src="${item.icon}" alt="${item.name}"></div>
                <div id="inventory-item-info"> /* Flex vertical */
                    <h3>${item.name}</h3>
                    <p>Quantité : ${item.amount}</p>
                    <p>Type : ${item.type}</p>
                </div>
            </div>
            <p>${item.description}</p>
        </div>
    `;

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    // Fermeture
    overlay.querySelector(".btn-cancel").onclick = () => {
        overlay.remove();
        if (onClose) onClose();
    };
}