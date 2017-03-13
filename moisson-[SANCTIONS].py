#coding: utf-8
#on importe nos beaux modules
import csv
import requests
from bs4 import BeautifulSoup

#je crée ma variable url qui mène vers la liste de pays qui font l'objet de sanctions

url1 = "http://www.international.gc.ca/sanctions/countries-pays/index.aspx?lang=eng"

#la politesse 

entetes = {
	"User-Agent":"Alexis Boulianne - Bonjour! Je suis étudiant journaliste, permettez-moi de me servir de votre site! :)",
	"From":"alexis.boulianne@gmail.com"
}

#on crée notre opération de base

contenu = requests.get(url1, headers=entetes)
#...
page = BeautifulSoup(contenu.text,"html.parser")

fichier = "doc_final.csv"

#Mes cibles sont des éléments text dans un div, mais leur accès rapide en groupe est ardu, donc 
#je dois moissonner le div qui contient les liens des pages des pays individuels, regroupés en éléments <li> sur la page d'accueil, 
#puis aller chercher les bouts de textes que je veux, soit les sanctions imposées par le Canada à leur égard, regroupés dans des div

#J'ai eu de la difficulté à gérer les exceptions, puisque mon script s'arrêtait lorsqu'il ne trouvait pas exactement
#ce que je lui demandais. À force d'essais et d'erreurs(ssssss), ça a fini par fonctionner. 

for pays in page.find("div", class_="module").find_all("li")[1:21]: #J'évite ainsi le premier élément, qui n'est pas bâti comme les autres, et je stoppe le script avant la fin, qui m'est inutile
	debut = "http://www.international.gc.ca"
	lien = debut + pays.a["href"]
	contenu2 = requests.get(lien, headers=entetes)
	page2 = BeautifulSoup(contenu2.text,"html.parser")
		#on entamme le moissonage des "deuxièmes" pages
	for sanctions in page2.find_all("div", class_="module"): #eh oui, encore un css "module".. originaux ces programmeurs fédéraux!
		pays1 = pays.find("a").text #pour trouver le pays, son nom est contenu dans une petite balise "a" au début du div "module"
		sanctions1 = page2.find("div", class_="module").find_all(text=True) #j'ai trouvé cette petite perle (text=True) sur Stack Overflow, qui me permet d'extraire le text d'un div un peu en bordel
		final = pays1, sanctions1 #on combine les deux, ici j'ai un petit problème de formattage que j'aurais réglé dans un monde idéal où le temps n'existe pas
		with open("doc_final.csv", "a") as csv_file:
			csv_bla = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC) #le quote_nonnumeric me permet de faire deux colonnes, une pour le pays et l'autre pour toutes les sanctions ensembles, mais, comme mentionné plus haut, ça ferait une colonne par sanctions, idéalement
			csv_bla.writerow(final) #fini!
