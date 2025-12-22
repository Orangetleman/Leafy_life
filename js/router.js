export const Router = {
    currentScreen: null,

    navigate(screenName, data = null) {
        if (this.currentScreen && this.currentScreen.destroy) {
            this.currentScreen.destroy();
        }

        import(`/js/screens/${screenName}.js`)
            .then(module => {
                this.currentScreen = new module.default(data);
                this.currentScreen.render();
            })
            .catch(err => console.error("Screen error,", err));
        }
    };