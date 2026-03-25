import { leafButton } from "../../components/button/LeafButton.js";
import { openLeafModal } from "../../components/modal/modalLeafs.js";
import { is_search_mode } from "../../utils/helpers.js";

export default class LeafsHome {
    constructor(data) {
        this.leafManager = data.leafManager;
        this.searchQuery = "";
    }

    render() {
        const game = document.getElementById("game");
        game.innerHTML = `
            <div class="leafs-container">
                <div class="leafs-header">
                    <div id="leafs-header-title-box">
                        <div id="leafs-header-title"><h2>Vos leafs</h2></div>
                    </div>
                    <div id="leafs-search-box">
                        <input type="text" placeholder="🔍 Rechercher..." id="leafs-search" class="search-bar">
                    </div>
                </div>
                <div class="leafs-list" id="leafs-list"></div>
            </div>
        `;
        // récupération de la zone liste
        const leafsList = document.getElementById("leafs-list");
        const searchInput = document.getElementById("leafs-search");

        // Événement focus : vider la liste
        searchInput.addEventListener("focus", () => {
            leafsList.innerHTML = "";
        });
        searchInput.addEventListener("blur", () => {
            this.refreshLeafsList(leafsList);
        });
        
        // Événement input : mettre à jour la recherche et actualiser la liste
        searchInput.addEventListener("input", (e) => {
            this.searchQuery = e.target.value;
            this.refreshLeafsList(leafsList);
        });

        // Affichage initial des leafs
        this.refreshLeafsList(leafsList);
    }

    refreshLeafsList(leafsList) {
        leafsList.innerHTML = "";
        
        // Vérifier si on recherche par tag (commence par #)
        const isTagSearch = this.searchQuery.startsWith("#");
        const searchTag = isTagSearch ? this.searchQuery.slice(1).toLowerCase() : "";
        
        // Filtrer les leafs selon la recherche
        const leafsToDisplay = this.leafManager.owned.filter(leaf => {
            if (is_search_mode()) {
                // Recherche par tag (biome, espèce, rareté)
                if (isTagSearch) {
                    const tags = [leaf.biome?.toLowerCase(), leaf.species?.toLowerCase(), leaf.rarity?.toLowerCase()];
                    return tags.some(tag => tag && tag.includes(searchTag));
                }
                // Recherche par nom
                return leaf.name.toLowerCase().includes(this.searchQuery.toLowerCase());
            }
            return true;
        });
        
        // Créer les boutons pour les leafs filtrés
        leafsToDisplay.forEach(leaf => {
            const leafBtn = leafButton(leaf, this.leafManager.owned, () => {
                openLeafModal(leaf);
            });
            leafsList.appendChild(leafBtn);
        });
        console.log(`Affichage de ${leafsToDisplay.length} leaf(s)`);
    }
}
