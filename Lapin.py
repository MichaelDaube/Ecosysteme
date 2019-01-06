from PySide2 import QtCore
from Animal import Animal
from random import randint, random


class Lapin(Animal):
    nom = 'lapin'

    def __init__(self, position, habitat, espece, timerSimulation, listOfTimers):
        super().__init__(position, habitat, espece, timerSimulation, listOfTimers)
        self.rayon = 2
        self.couleur = QtCore.Qt.white

        self.rayonTerritoire = 100
        self.rayonPerception = 250
        self.vitesse = 50

        self.dureeVie = (1 + 8 * random()) * 12 * 30 * 24  # durée de vie exprimée en heures
        self.dureeGestation = 30 * 24  # durée exprimée en heure
        self.ageFecondite = (6 + 3 * random()) * 30 * 24  # duree exprimee en heure

    def accouchement(self):
        taillePortee = randint(2, 10)
        for compteur in range(2, taillePortee + 1):
            bebe = Lapin(self.habitat.getPosition(), self.habitat, self.espece, self.timerSimulation, self.listOfTimers)
            self.espece.ajoutIndividu(bebe)
        self.gestante = False
        self.ageAccouchement = self.age.tempsEcoule()
        self.nombrePortee = self.nombrePortee + 1
