import sys
from FenetreSimulation import FenetreSimulation
from PySide2 import QtWidgets

if __name__ == "__main__":
    simu = QtWidgets.QApplication(sys.argv)
    fenetreSimu = FenetreSimulation()
    fenetreSimu.showMaximized()
    fenetreSimu.prairie.update()
    sys.exit(simu.exec_())
