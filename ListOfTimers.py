class ListOfTimers():

    def __init__(self):
        self.liste = []

    def ajoutTimer(self, timer):
        self.liste.append(timer)

    def retraitTimer(self, timer):
        self.liste.remove(timer)

    def getListe(self):
        return self.liste