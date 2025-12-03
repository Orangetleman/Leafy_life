export function rand(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
};

export function loadSprite(path) {
    const img = new Image();
    img.scr = path;
    return img;
};