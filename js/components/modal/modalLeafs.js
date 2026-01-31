export function openLeafModal(leaf) {
    // Overlay
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";

    // Modal
    const modal = document.createElement("div");
    modal.className = "modal";
    modal.id = "leaf-modal";
    
    modal.innerHTML = `
        <button class="modal-close-btn">Fermer</button>
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
    `;
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Fermer avec le bouton Fermer
    const closeBtn = modal.querySelector(".modal-close-btn");
    closeBtn.addEventListener("click", () => {
        overlay.remove();
    });
    
    // Fermer en cliquant en dehors du modal
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}
