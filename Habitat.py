from PySide2 import QtCore


class Habitat():
    def __init__(self, position, dimension, habitats):
        self.position = position
        self.dimension = dimension
        self.representationGraphique = QtCore.QRect(self.position.x() - self.dimension / 2,
                                                    self.position.y() - self.dimension / 2,
                                                    self.dimension, self.dimension)
        self.groupe = []
        self.dessin = False
        self.habitats = habitats

    def ajoutIndividu(self, animal):
        self.groupe.append(animal)

    def retraitIndividu(self, animal):
        if self.getTaillePopulation() == 1:
            self.habitats.retraitHabitat(self)
        self.groupe.remove(animal)

    def getTaillePopulation(self):
        return len(self.groupe)

    def getPosition(self):
        return self.position

    def getDimension(self):
        return self.dimension

    def getRepresentationGraphique(self):
        return self.representationGraphique

    def habitatDessine(self):
        return self.dessin

    def changeStatuDessin(self):
        if self.dessin:
            self.dessin = False
        else:
            self.dessin = True

    def getHabitats(self):
        return self.habitats

    def getGroupe(self):
        return self.groupe
