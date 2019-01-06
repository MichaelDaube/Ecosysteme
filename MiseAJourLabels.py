class MiseAJourLabels():
    def __init__(self, labelTimerSimulation, timerSimulation, listOfTimers, vitesseLabel, sliderUniteTemps, labelPopLapins, lapins, timer):
        self.labelTimerSimulation = labelTimerSimulation
        self.timerSimulation = timerSimulation

        self.listOfTimers = listOfTimers

        self.vitesseLabel = vitesseLabel
        self.sliderUniteTemps = sliderUniteTemps

        self.labelPopLapins = labelPopLapins
        self.lapins = lapins

        self.timer = timer

    def misesAJour(self):
        self.labelPopLapins.setText(("Nombre de lapins: " + str(self.lapins.getTaillePopulation())))

        self.labelTimerSimulation.setText(" Durée de la simulation :     " + str(self.timerSimulation.getHeureSimu()) +
                                          " heures, " + str(self.timerSimulation.getJourSimu()) + " jours, " +
                                          str(self.timerSimulation.getMoisSimu()) + " mois, " +
                                          str(self.timerSimulation.getAnneeSimu()) + " années.")

        for timer in self.listOfTimers.getListe():
            timer.setVitesse(self.sliderUniteTemps.value())
        self.vitesseLabel.setText("  Vitesse:  " + str(self.timerSimulation.getVitesse()))
