import AdventureUI from "../../../gameplay/adventure/adventureUI.js";

export default class AdventureHome {
    render() {
        const ui = new AdventureUI(this.data);
        ui.render();
    }
}
