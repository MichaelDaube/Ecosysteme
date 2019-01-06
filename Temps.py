import time
from PySide2 import QtCore


class Temps():
    def __init__(self, listOfTimers):
        self.tempsMAJ = time.time()
        self.tempsEcouleAvantMAJ = 0

        self.vitesse = 1
        self.equivalentHeure = 1 / self.vitesse

        listOfTimers.ajoutTimer(self)

    def setVitesse(self, vitesse):
        self.vitesse = vitesse
        self.equivalentHeure = 1 / self.vitesse
        self.tempsEcouleAvantMAJ += self.tempsEcouleDepuisMAJ()
        self.tempsMAJ = time.time()

    def getVitesse(self):
        return self.vitesse

    def reInit(self):
        self.tempsMAJ = time.time()
        self.tempsEcouleAvantMAJ = 0
        self.vitesse = 1
        self.equivalentHeure = 1 / self.vitesse

    def getEquivalentHeure(self):
        return self.equivalentHeure

    # def getTempsInit(self):           obsolete ?
    #     return self.tempsInit

    def tempsEcouleDepuisMAJ(self):
        return (time.time() - self.tempsMAJ) / self.equivalentHeure

    def tempsEcoule(self):
        return self.tempsEcouleAvantMAJ + self.tempsEcouleDepuisMAJ()

    def getHeureSimu(self):
        return int(self.tempsEcoule() % 24)

    def getJourSimu(self):
        return int((self.tempsEcoule() // 24) % 30)

    def getMoisSimu(self):
        return int((self.tempsEcoule() // 24 // 30) % 12)

    def getAnneeSimu(self):
        return int((self.tempsEcoule() // 24 // 30 // 12) % 30)
