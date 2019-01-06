from PySide2 import QtWidgets, QtCore
from random import randint, choice, random
from math import sqrt, ceil, floor
from Temps import Temps
from Habitat import Habitat


class Animal(QtWidgets.QWidget):
    nom = 'animal'

    def __init__(self, position, habitat, espece, timerSimulation, listOfTimers):
        self.espece = espece
        self.habitat = habitat
        self.habitat.ajoutIndividu(self)
        self.position = position
        self.rayon = 5
        self.representationGraphique = QtCore.QRect(self.position.x() - self.rayon, self.position.y() - self.rayon,
                                                    self.rayon, self.rayon)
        self.couleur = QtCore.Qt.black

        self.rayonTerritoire = 50
        self.rayonPerception = 50  # la perception se fera dans un carré centré sur l'animal
        self.carrePerception = QtCore.QRect(self.position.x() - self.rayonPerception,
                                            self.position.y() - self.rayonPerception, self.rayonPerception,
                                            self.rayonPerception)

        self.etat = 'oisif'
        self.objectifs = {'oisif': self.oisif, 'deplacement': self.deplacement, "repos": self.repose,
                          "fatigue": self.retourMaison, "endormi": self.dors}

        self.listOfTimers = listOfTimers

        self.destination = None
        self.chrono = Temps(self.listOfTimers)
        self.positionInit = self.position
        self.vitesse = 1

        self.retourMaisonEnCours = False
        self.abris = True

        self.tempsFaim = 0
        self.indiceFaim = 100

        self.dureePause = 0

        self.energie = 100
        self.chronoEnergie = Temps(self.listOfTimers)

        self.dureeVie = (6 + 4 * random()) * 12 * 30 * 24  # durée de vie exprimée en heures
        self.age = Temps(self.listOfTimers)

        self.timerSimulation = timerSimulation

        self.sexe = choice(["M", "F"])
        self.ageFecondite = (6 + 3 * random()) * 30 * 24  # duree exprimee en heure
        self.fecond = False
        self.dureeGestation = 30 * 24  # durée exprimée en heure
        self.partenaire = None
        self.libre = True
        self.gestante = False
        self.debutGestation = None
        self.ageAccouchement = self.age.tempsEcoule()  # initialisation

        self.nombrePortee = 0
        self.indicePortees = 0

        #############################

    # Les accesseurs
    def getPosition(self):
        return self.position

    def getRayon(self):
        return self.rayon

    def getRepresentationGraphique(self):
        return self.representationGraphique

    def getCouleur(self):
        return self.couleur

    def getHabitat(self):
        return self.habitat

    def getRayonTerritoire(self):
        return self.rayonTerritoire

    def getEspece(self):
        return self.espece

    ##############################
    # Les actions
    def activation(self):
        #        self.evolutionFaim()
        if self.timerSimulation.tempsEcoule() >= self.dureeVie:
            self.mort()
            return
        self.gestionReproduction()
        self.evolutionEnergie()
        self.objectifs[self.etat]()

        if self.nombrePortee > self.indicePortees:
            print(self.nombrePortee)
            self.indicePortees += 1

        if self.libre and not self.fecond:
            self.couleur = QtCore.Qt.green
        elif self.gestante:
            self.couleur = QtCore.Qt.blue
        elif not self.libre:
            self.couleur = QtCore.Qt.red
        else:
            self.couleur = QtCore.Qt.white

    #    def evolutionFaim(self):

    def gestionReproduction(self):
        # if self.sexe == 'F':
        #     self.gestionStatuLibre()
        self.gestionStatuFecond()

        if self.femelleFeconde() and self.libre:
            self.recherchePartenaire()
        elif self.femelleFeconde():
            self.fecond = False
            self.gestante = True
            self.debutGestation = self.age.tempsEcoule()
        if self.gestante and self.gestationTerminee():
            self.accouchement()

    def accouchement(self):  # A réécrire dans les classes filles
        taillePortee = randint(2, 10)
        for compteur in range(2, taillePortee + 1):
            bebe = Animal(self.habitat.getPosition(), self.habitat, self.espece, self.timerSimulation,
                          self.listOfTimers)
            self.espece.ajoutIndividu(bebe)
        self.gestante = False
        self.ageAccouchement = self.age.tempsEcoule()
        self.nombrePortee = self.nombrePortee + 1

    def gestationTerminee(self):
        return (self.age.tempsEcoule() - self.debutGestation) >= self.dureeGestation

    def recherchePartenaire(self):
        listeHabitats = self.habitat.getHabitats().getHabitats().copy()
        # listeHabitats.remove(self.habitat)
        listeHabitatsProches = self.rechercheHabitatsProches(listeHabitats)
        futurePartenaire = None
        if len(listeHabitatsProches) > 0:
            futurePartenaire = self.rechercheIndividuEligible(listeHabitatsProches)
        if futurePartenaire:
            self.partenaire = futurePartenaire
            self.libre = False
            self.fecond = False
            self.gestante = True
            self.debutGestation = self.timerSimulation.tempsEcoule()
            if random() < 0.3:
                self.rechercheNouvelHabitat()
            self.partenaire.nouveauPartenaire(self, self.habitat)

    def rechercheIndividuEligible(self, listeHabitats):
        for habitat in listeHabitats:
            partenairePotentiel = self.recherchePartenaireDansHabitat(habitat)
            if partenairePotentiel:
                return partenairePotentiel

    def recherchePartenaireDansHabitat(self, habitat):
        for individu in habitat.getGroupe():
            if individu.maleFecondLibre():
                return individu
        return None

    def rechercheHabitatsProches(self, listeHabitats):
        listeHabitatsProches = []
        for habitat in listeHabitats:
            if self.habitatMemeEspece(habitat) and self.distanceHabitatsFaible(habitat):
                listeHabitatsProches.append(habitat)
        return listeHabitatsProches

    def distanceHabitatsFaible(self, habitat):
        distance = sqrt((habitat.getPosition().x() - self.habitat.getPosition().x()) ** 2 + (
                habitat.getPosition().y() - self.habitat.getPosition().y()) ** 2)
        return distance <= self.rayonPerception

    def habitatMemeEspece(self, habitat):
        return habitat.getGroupe()[0].nom == self.nom

    def rechercheNouvelHabitat(self):
        nouvelHabitat = Habitat(
            QtCore.QPoint(randint(self.position.x() - self.rayonTerritoire, self.position.x() + self.rayonTerritoire),
                          randint(self.position.y() - self.rayonTerritoire, self.position.y() + self.rayonTerritoire)),
            self.habitat.getDimension(), self.habitat.getHabitats())
        listeHabitats = self.habitat.getHabitats()
        listeHabitats.ajoutHabitat(nouvelHabitat)
        self.changementHabitat(nouvelHabitat)

    def changementHabitat(self, nouvelHabitat):
        self.habitat.retraitIndividu(self)
        nouvelHabitat.ajoutIndividu(self)
        self.habitat = nouvelHabitat

    def nouveauPartenaire(self, individu, habitat):
        self.partenaire = individu
        self.libre = False
        self.changementHabitat(habitat)

    def gestionStatuLibre(self):
        if not self.libre and self.femelleEnAge() and self.age.tempsEcoule() - self.ageAccouchement > 2 * 30 * 24:
            self.libre = True

    def finCouple(self):
        self.partenaire = None

    def changeStatuLibre(self):
        if self.libre:
            self.libre = False
        else:
            self.libre = True

    def femelleFeconde(self):
        return self.sexe == 'F' and self.fecond

    def gestionStatuFecond(self):
        if not self.fecond and self.sexe == 'M' and self.age.tempsEcoule() >= self.ageFecondite :
            self.fecond = True
        elif not self.fecond and not self.gestante and self.age.tempsEcoule() >= self.ageFecondite and self.age.tempsEcoule() - self.ageAccouchement > 2 * 30 * 24:
            self.fecond = True

    def maleEnAge(self):
        return self.sexe == 'M' and self.fecond

    def maleFecondLibre(self):
        return self.maleEnAge() and self.libre

    def femelleEnAge(self):
        return self.sexe == 'F' and self.age.tempsEcoule() >= self.ageFecondite

    def mort(self):
        if self.partenaire:
            self.partenaire.changeStatuLibre()
            self.partenaire.finCouple()
        self.espece.retraitIndividu(self)
        self.habitat.retraitIndividu(self)

    def evolutionEnergie(self):
        if self.etat == "repos":
            self.energie += (4 + random()) * self.chronoEnergie.tempsEcoule()
        elif self.energie < 100:
            self.energie = 100
        elif self.etat == "endormi":
            self.energie += (15 + 2 * random()) * self.chronoEnergie.tempsEcoule()
        else:
            self.energie -= (10 + 2 * random()) * self.chronoEnergie.tempsEcoule()
        self.chronoEnergie.reInit()
        if self.energie < 0 and not self.retourMaisonEnCours:
            self.etat = "fatigue"

    def retourMaison(self):
        self.etat = 'deplacement'
        self.retourMaisonEnCours = True
        self.destination = self.habitat.getPosition()
        self.chrono.reInit()
        self.deplacement()

    def dors(self):
        if self.energie > 90:
            self.etat = "oisif"

    def oisif(self):
        choice((self.erre, self.repose))()

    def repose(self):
        if not self.etat == "repos":
            self.chrono.reInit()
            self.dureePause = random() / 2
            self.etat = "repos"
        if self.chrono.tempsEcoule() > self.dureePause:
            self.etat = "oisif"

    def erre(self):
        self.etat = 'deplacement'
        rayonAlea = randint(0, self.rayonTerritoire)
        abscisseAlea = randint(self.habitat.getPosition().x() - rayonAlea,
                               self.habitat.getPosition().x() + rayonAlea)
        horizontalAlea = abscisseAlea - self.habitat.getPosition().x()
        verticalAlea = choice([-1, 1]) * sqrt(rayonAlea ** 2 - horizontalAlea ** 2)
        ordonneeAlea = self.habitat.getPosition().y() + int(verticalAlea)
        destination = QtCore.QPoint(abscisseAlea, ordonneeAlea)
        self.destination = destination
        self.chrono.reInit()
        self.deplacement()

    def deplacement(self):
        if self.egalitePoints(self.position, self.habitat.getPosition()) and self.energie < 0:
            self.etat = 'endormi'
            self.abris = True
            self.positionInit = QtCore.QPoint(self.position.x(), self.position.y())
            self.retourMaisonEnCours = False
        elif self.egalitePoints(self.position, self.destination):
            self.etat = 'oisif'
            self.positionInit = QtCore.QPoint(self.position.x(), self.position.y())
        else:
            if self.abris:
                self.abris = False
            intervalleTemps = 0.01
            distanceRealisable = intervalleTemps * self.vitesse
            if self.chrono.tempsEcoule() > intervalleTemps:
                vecteurDestination = QtCore.QPoint(self.destination.x() - self.position.x(),
                                                   self.destination.y() - self.position.y())
                distance = sqrt(vecteurDestination.x() ** 2 + vecteurDestination.y() ** 2)
                if distance > distanceRealisable:
                    coefficient = self.chrono.tempsEcoule() * self.vitesse / distance
                    self.position = QtCore.QPoint(
                        int(self.position.x() + self.arrondi(coefficient * vecteurDestination.x())),
                        int(self.position.y() + self.arrondi(coefficient * vecteurDestination.y())))
                    self.chrono.reInit()
                else:
                    self.position = QtCore.QPoint(self.destination.x(), self.destination.y())
        self.majRepresentationGraphique()

    def majRepresentationGraphique(self):
        self.representationGraphique.moveTo(self.position.x() - self.rayon, self.position.y() - self.rayon)

    def arrondi(self, nombre):
        if nombre < 0:
            return floor(nombre)
        else:
            return ceil(nombre)

    def egalitePoints(self, point1, point2):
        return (point1.x() == point2.x()) and (point1.y() == point2.y())

#    def mange(self):
