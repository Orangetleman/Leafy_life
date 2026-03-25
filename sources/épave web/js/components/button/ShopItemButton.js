// Sous-fonction INTERNE
function createPriceBadge(value, type) {
    if (type === "stock") {
        const badge = document.createElement("div");
        badge.className = "price-badge stock-badge";
        badge.textContent = `Stock: ${value}`;
        return badge;
    } else {
        const badge = document.createElement("div");
        badge.className = `price-badge price-${type.toLowerCase()}`;
        badge.textContent = `${value} ${type}`;
        return badge;
    }
}

// Fonction EXPORTÉE
export function ShopItemButton(item, shop, onClick = null) {
    const button = document.createElement("button");
    button.className = "shop-item-btn";
    button.type = "button";

    // ── Partie gauche
    const left = document.createElement("div");
    left.className = "shop-item-left";

    const icon = document.createElement("div");
    icon.className = "shop-item-icon";
    icon.innerHTML = `<img src="${item.icon}" alt="${item.name}">`;

    const name = document.createElement("div");
    name.className = "shop-item-name";
    name.textContent = `${item.name}`;

    left.appendChild(icon);
    left.appendChild(name);

    // ── Partie droite (prix)
    const prices = document.createElement("div");
    prices.className = "shop-item-prices";

    if (item.price_O2 !== undefined) {
        prices.appendChild(createPriceBadge(item.price_O2, "O2"));
    }

    if (item.price_CO2 !== undefined) {
        prices.appendChild(createPriceBadge(item.price_CO2, "CO2"));
    }

    if (shop.stock.find((i) => i.name === item.name)?.amount !== undefined) {
        prices.appendChild(createPriceBadge(shop.stock.find((i) => i.name === item.name).amount, "stock"));
    }
    button.appendChild(left);
    button.appendChild(prices);

    // ── Clic (prévu pour la modal)
    if (onClick) {
        button.addEventListener("click", () => onClick(item));
    }

    return button;
}


