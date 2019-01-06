import matplotlib.pyplot as plt

class FenetreCourbe(object):
	"à partir de listes de valeurs (les tailles des populations relevées à intervalles réguliers) affiche des courbes d'évolution de ces population en fonction du temps"
	
	def __init__(self,donnees=[24,58,65,69,32,14,78,25,3,8]):
		self.donnees=donnees
			
	
	def afficheCourbe(self):
		nb_donnees=len(self.donnees)
		uniteTemps=[]
		for i in range (nb_donnees):
			uniteTemps.append(i)
		plt.plot(uniteTemps,self.donnees)
		plt.show()
		

		
