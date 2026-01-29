export function openLeafModal(leaf) {
    const modal = document.createElement("div");
    modal.className = "modal";
    modal.id = "leaf-modal";
    
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>${leaf.name}</h2>
                <button class="modal-close-btn">&times;</button>
            </div>
            <div class="modal-body">
                <div class="leaf-modal-info">
                    <img src="${leaf.img}" alt="${leaf.name}" class="leaf-modal-img">
                    <div class="leaf-modal-stats">
                        <p><strong>Type:</strong> ${leaf.type}</p>
                        <p><strong>Rareté:</strong> ${leaf.rarity}</p>
                        <p><strong>Espèce:</strong> ${leaf.species}</p>
                        <p><strong>Biome:</strong> ${leaf.biome}</p>
                        <p><strong>Niveau:</strong> ${leaf.lvl}</p>
                        <p><strong>HP:</strong> ${leaf.hp}</p>
                        <p><strong>Attaque:</strong> ${leaf.atk}</p>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="modal-btn modal-btn-close">Fermer</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Fermer avec le bouton X
    const closeBtn = modal.querySelector(".modal-close-btn");
    closeBtn.addEventListener("click", () => {
        modal.remove();
    });
    
    // Fermer avec le bouton Fermer
    const closeFooterBtn = modal.querySelector(".modal-btn-close");
    closeFooterBtn.addEventListener("click", () => {
        modal.remove();
    });
    
    // Fermer en cliquant en dehors du modal
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}
