class LeafManager:
    def __init__(self, owned = []):
        self.owned = owned

    def add_leaf(self,leaf):
        h = False
        for i in self.owned:
            if i == leaf:
                print(leaf["name"] + " est déjà un de vos leafs.")
                h = True
        if h == False:
            self.owned.append(leaf)
            print(leaf["name"] + " fais maintenant parti de vos leafs !")

leafmanager = LeafManager([])