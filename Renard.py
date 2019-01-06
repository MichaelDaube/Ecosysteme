from PySide2 import QtCore
from Animal import Animal
from random import randint, random


class Renard(Animal):
    nom = 'renard'

    def __init__(self, position, habitat, espece, timerSimulation, listOfTimers):
        super().__init__(position, habitat, espece, timerSimulation, listOfTimers)
        self.rayon = 4
        self.couleur = QtCore.Qt.red

        self.rayonTerritoire = 200
        self.rayonPerception = 100
        self.vitesse = 60

        self.dureeVie = (2 + 3 * random()) * 12 * 30 * 24  # durée de vie exprimée en heures
        self.dureeGestation = 52 * 24  # durée exprimée en heure
        self.ageFecondite = (6 + 3 * random()) * 30 * 24  # duree exprimee en heure

    def accouchement(self):
        taillePortee = randint(2, 10)
        for compteur in range(2, taillePortee + 1):
            bebe = Renard(self.habitat.getPosition(), self.habitat, self.espece, self.timerSimulation,
                          self.listOfTimers)
            self.espece.ajoutIndividu(bebe)
        self.gestante = False
        self.ageAccouchement = self.age.tempsEcoule()
        self.nombrePortee = self.nombrePortee + 1
