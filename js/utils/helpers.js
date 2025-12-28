export function rand(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
};

export function loadSprite(path) {
    const img = new Image();
    img.scr = path;
    return img;
};

export function is_search_mode() {
    const searchInput = document.querySelector(".search-bar");
    console.log(`Search input value: "${searchInput.value}"`);
    return searchInput && searchInput.value.trim() !== "";
}