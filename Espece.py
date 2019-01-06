class Espece():
    def __init__(self, animal):
        self.espece = animal.nom
        self.individus = []
        self.evolutionPopulation = []
        self.taillePopulation = 0

    def ajoutIndividu(self, individu):
        self.individus.append(individu)
        self.taillePopulation += 1

    def retraitIndividu(self, individu):
        self.individus.remove(individu)
        self.taillePopulation -= 1

    def accumulationDonnees(self):
        self.evolutionPopulation.append(self.taillePopulation)

    def getIndividus(self):
        return self.individus

    def getTaillePopulation(self):
        return self.taillePopulation
