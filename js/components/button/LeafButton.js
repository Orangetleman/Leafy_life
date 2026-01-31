import { LEAFS_TYPE } from "../../data/leafs.js";

export function createBadge(value, type, onClick = null) {
    if (type === "lvl") {
        const badge = document.createElement("div");
        badge.className = "leaf-button-badge lvl-badge";
        badge.textContent = `Lvl: ${value}`;
        return badge;
    } else {
        const badge = document.createElement("button");
        badge.className = "leaf-button-badge boost-badge";
            const text = document.createElement("div");
            text.textContent = `+`;
            badge.appendChild(text);
            const icon = document.createElement("img");
            icon.src = `${value.icon}`;
            icon.alt = `Boost : ${value.name}`;
            badge.appendChild(icon);
        badge.onclick = () => onClick(value);
        return badge;
    }
}

export function leafButton(leaf, leafs, onClick = null) {
    const button = document.createElement("button");
    button.className = "leaf-button";
        // Left side with image and info
        const left = document.createElement("div");
        left.className = "leaf-button-left";
            const img = document.createElement("div");
            img.className = "leaf-button-img";
                const imgContent = document.createElement("img");
                imgContent.src = leaf.img;
                imgContent.alt = leaf.name;
                img.appendChild(imgContent);
            left.appendChild(img);
            const info = document.createElement("div");
            info.className = "leaf-button-info";
                const name = document.createElement("div");
                name.className = "leaf-button-name";
                name.textContent = `${leaf.name}`;
                const rarity = document.createElement("div");
                rarity.className = "leaf-button-rarity";
                rarity.textContent = `Rarity: ${leaf.rarity}`;
                const type_icon = document.createElement("img");
                type_icon.className = "leaf-button-type-icon";
                type_icon.src = LEAFS_TYPE[leaf.type].icon;
                type_icon.alt = LEAFS_TYPE[leaf.type].name;
                info.appendChild(name);
                info.appendChild(rarity);
                info.appendChild(type_icon);
            left.appendChild(info);
        button.appendChild(left);

        // Right side with lvl
        const right = document.createElement("div");
        right.className = "leaf-button-right";
        right.appendChild(createBadge(leaf.lvl, "lvl")); 
        button.appendChild(right);

    button.onclick = () => onClick(leaf, leafs);
    return button;
}