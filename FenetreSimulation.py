from PySide2 import QtCore, QtGui, QtWidgets
from Lapin import Lapin
from Espece import Espece
from Temps import Temps
from Prairie import Prairie
from MiseAJourLabels import MiseAJourLabels
from ListOfTimers import ListOfTimers


class FenetreSimulation(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.quit = QtWidgets.QPushButton("Quit", self)
        self.quit.setGeometry(62, 40, 75, 30)
        self.quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(self.quit, QtCore.SIGNAL("clicked()"),
                     QtWidgets.qApp, QtCore.SLOT("quit()"))

        self.listOfTimers = ListOfTimers()

        self.timerSimulation = Temps(self.listOfTimers)
        self.timerSimulationLabel = QtWidgets.QLabel()

        self.sliderUniteTemps = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sliderUniteTemps.setRange(1, 1000)
        self.sliderUniteTemps.setValue(1)
        self.vitesseLabel = QtWidgets.QLabel()

        self.popLapinsLabel = QtWidgets.QLabel()
        self.lapins = Espece(Lapin)

        self.timerMAJ = QtCore.QTimer()
        self.gestionnaireLabels = MiseAJourLabels(self.timerSimulationLabel, self.timerSimulation, self.listOfTimers,
                                                  self.vitesseLabel, self.sliderUniteTemps, self.popLapinsLabel,
                                                  self.lapins, self.timerMAJ)

        self.timerPrairie = QtCore.QTimer()
        self.prairie = Prairie(self.lapins, self.timerPrairie, self.gestionnaireLabels, self.timerSimulation, self.listOfTimers)
        self.timerPrairie.start(10)
        self.connect(self.timerPrairie, QtCore.SIGNAL("timeout()"), self.prairie, QtCore.SLOT("animation()"))

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.quit, 50, 4)
        self.gridLayout.addWidget(self.popLapinsLabel, 1, 4)
        self.gridLayout.addWidget(self.timerSimulationLabel, 0, 2)
        self.gridLayout.addWidget(self.vitesseLabel, 0, 1)
        self.gridLayout.addWidget(self.sliderUniteTemps, 0, 0)
        self.gridLayout.addWidget(self.prairie, 1, 0, 50, 4)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(3, 3)
        self.setLayout(self.gridLayout)


################################################
# L'appel de la classe se fera de la manière suivante :

#    simu = QtWidgets.QApplication(sys.argv)
#    fenetreSimu = FenetreSimulation()
#    fenetreSimu.show()
#    sys.exit(simu.exec_())
