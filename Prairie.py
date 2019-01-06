from PySide2 import QtCore, QtGui, QtWidgets
from Lapin import Lapin
from Habitat import Habitat
from Habitats import Habitats
from random import randint


class Prairie(QtWidgets.QWidget):
    def __init__(self, espece, timer, gestionnaireLabels, timerSimulation, listOfTimers):
        QtWidgets.QWidget.__init__(self)

        self.setPalette(QtGui.QPalette(QtGui.QColor(210, 250, 200)))
        self.setAutoFillBackground(True)

        self.espece = espece
        self.habitats = Habitats()
        self.dimensionHabitat = 8
        self.initDone = False

        self.timer = timer
        self.gestionnaireLabels = gestionnaireLabels
        self.timerSimulation = timerSimulation

        self.listOfTimers = listOfTimers

        self.nombreLapins = 200  # à passer en paramètres
        self.nombreRenards = 20

    def animation(self):
        for individu in self.espece.getIndividus():
            individu.activation()
        self.update()
        self.gestionnaireLabels.misesAJour()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        if not self.initDone:
            self.initDone = True
            self.generateurPopulationInit(self.espece)

        for habitat in self.habitats.getHabitats():
            self.placementHabitat(painter, habitat)

        for individu in self.espece.getIndividus():
            self.placementIndividus(painter, individu)

        self.timer.start(10)

    def placementHabitat(self, painter, habitat):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.black)
        painter.drawRect(habitat.getRepresentationGraphique())

    def placementIndividus(selfself, painter, individu):
        painter.setBrush(individu.getCouleur())
        painter.setPen(QtCore.Qt.black)
        painter.drawEllipse(individu.getRepresentationGraphique())

    def generateurPopulationInit(self, espece):
        lapinsRestant = self.nombreLapins
        popMax = 10
        while lapinsRestant > 0:
            habitat = Habitat(
                QtCore.QPoint(randint(10, self.width() - 10), randint(10, self.height() - 10)),
                self.dimensionHabitat, self.habitats)
            self.habitats.ajoutHabitat(habitat)
            if lapinsRestant < 10:
                popMax = lapinsRestant
            popHabitat = randint(1, popMax)
            lapinsRestant = lapinsRestant - popHabitat
            for i in range(0, popHabitat):
                lapin = Lapin(habitat.getPosition(), habitat, espece, self.timerSimulation, self.listOfTimers)
                espece.ajoutIndividu(lapin)

    def resizeEvent(self, event):
        for individu in self.espece.getIndividus():
            if individu.habitat.habitatDessine():
                individu.habitat.changeStatuDessin()
    # fonction appelée lors d'un changement de taille de la fenêtre
    # pour réinitialiser l'état 'dessiné' des habitats à false
    # afin que ceux-ci soient bien représentés après le changement de taille
