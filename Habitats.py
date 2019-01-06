class Habitats():
    def __init__(self):
        self.habitats = []

    def ajoutHabitat(self, habitat):
        self.habitats.append(habitat)

    def retraitHabitat(self, habitat):
        self.habitats.remove(habitat)

    def getHabitats(self):
        return self.habitats
