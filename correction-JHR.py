#coding: utf-8

### MES COMMENTAIRES ET CORRECTIONS SONT MARQUÉES PAR TROIS DIÈSES

#on importe nos beaux modules
import csv
import requests
from bs4 import BeautifulSoup
import json ### nécessaire pour l'alternative 2 ci-dessous
import datetime

#je crée ma variable url qui mène vers la liste de pays qui font l'objet de sanctions

# url1 = "http://www.international.gc.ca/sanctions/countries-pays/index.aspx?lang=eng"

### Je prendrais plutôt la version française du site :)
url1 = "http://www.international.gc.ca/sanctions/countries-pays/index.aspx?lang=fra"

#la politesse 

entetes = {
	"User-Agent":"Alexis Boulianne - Bonjour! Je suis étudiant journaliste, permettez-moi de me servir de votre site! :)",
	"From":"alexis.boulianne@gmail.com"
}

#on crée notre opération de base

contenu = requests.get(url1, headers=entetes)
#...
page = BeautifulSoup(contenu.text,"html.parser")

fichierCSV = "doc_final-JHR.csv" ### Nouveau nom de fichier
fichierJSON = "doc_final-JHR.json" ### Nouveau nom de fichier pour alternative 2 ci-dessous

#Mes cibles sont des éléments text dans un div, mais leur accès rapide en groupe est ardu, donc 
#je dois moissonner le div qui contient les liens des pages des pays individuels, regroupés en éléments <li> sur la page d'accueil, 
#puis aller chercher les bouts de textes que je veux, soit les sanctions imposées par le Canada à leur égard, regroupés dans des div

#J'ai eu de la difficulté à gérer les exceptions, puisque mon script s'arrêtait lorsqu'il ne trouvait pas exactement
#ce que je lui demandais. À force d'essais et d'erreurs(ssssss), ça a fini par fonctionner. 

### Partie de code pour l'alternative 2 ci-dessous

sanctions = [] ### Ici, je commence par créer une liste qui va contenir des dictionnaires

maintenant = datetime.datetime.now()
print(maintenant)

sanctions.append(str(maintenant))

for pays in page.find("div", class_="module").find_all("li")[1:21]: #J'évite ainsi le premier élément, qui n'est pas bâti comme les autres, et je stoppe le script avant la fin, qui m'est inutile
	# pass ### Je ne connaissais pas cette commande, mais selon ce que lis dans la doc Python, elle n'était pas nécessaire
	debut = "http://www.international.gc.ca"
	lien = pays.a["href"] ### Je fais cette étape supplémentaire, car les cons, ils ont oublié de mettre le lien en français dans le cas du Soudan du Sud!
	# print(lien[-4:])
	if lien[-4:] == "aspx":
		lien = lien + "?lang=fra"
	# print(lien)

	hyperlien = debut + lien ### Je change lien pour hyperlien
	print(hyperlien) ### Affichage aux fins de vérification

	contenu2 = requests.get(hyperlien, headers=entetes)
	page2 = BeautifulSoup(contenu2.text,"html.parser")
	# 	#on entamme le moissonage des "deuxièmes" pages
	# for sanctions in page2.find_all("div", class_="module"): #eh oui, encore un css "module".. originaux ces programmeurs fédéraux! ### LOL
	# 	pays1 = pays.find("a").text #pour trouver le pays, son nom est contenu dans une petite balise "a" au début du div "module"
	# 	sanctions1 = page2.find("div", class_="module").find_all(text=True) #j'ai trouvé cette petite perle (text=True) sur Stack Overflow, qui me permet d'extraire le text d'un div un peu en bordel
	# 	final = pays1, sanctions1 #on combine les deux, ici j'ai un petit problème de formattage que j'aurais réglé dans un monde idéal où le temps n'existe pas
	# 	with open("doc_final.csv", "a") as csv_file:
	# 		csv_bla = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC) #le quote_nonnumeric me permet de faire deux colonnes, une pour le pays et l'autre pour toutes les sanctions ensembles, mais, comme mentionné plus haut, ça ferait une colonne par sanctions, idéalement
	# 		csv_bla.writerow(final) #fini!

### Comme le nombre de sanctions est différent d'un pays à l'autre, ce que tu fais est correct.
### Tu as une colonne de sanctions, à l'intérieur de laquelle le nombre de sanctions varie en fonction du pays.

### Deux alternatives sont possibles

### ALTERNATIVE 1 -> Une colonne par sanction
### On sait que le maximum est 5 sanctions, alors on va se préparer à avoir 5 colonnes

	# contenu2 = requests.get(hyperlien, headers=entetes)
	# page2 = BeautifulSoup(contenu2.text,"html.parser")

	# sanct = [] ### Je me crée une liste vide pour y mettre toutes les infos que je souhaite moissonner; chaque liste va être une ligne du CSV que je vais ultimement produire

	# nom = page2.h1.text[32:]
	# if nom[0:4] == "à la":
	# 	nom = nom[5:]
	# elif nom[0:4] == "à l'":
	# 	nom = nom[4:]
	# else:
	# 	nom = nom[3:]
	# # print(nom)

	# ### J'ajoute le nom du pays à ma liste
	# sanct.append(nom)

	# ### Je vais ensuite recueillir deux infos qui me paraissent pertinentes dans les balises méta:
	# dateEmission = page2.find("meta", attrs={"name":"dcterms.issued"})["content"]
	# dateMAJ = page2.find("meta", attrs={"name":"dcterms.modified"})["content"]

	# ### Je les ajoute à ma liste
	# sanct.append(dateEmission)
	# sanct.append(dateMAJ)

	# ### Je calcule combien de sanctions affectent ce pays
	# sanctions = page2.find_all("div", class_="span-1")
	# nbSanctions = len(sanctions)
	# # print(nbSanctions)

	# ### Je recueille les sanctions une à la fois et les place dans ma liste «sanct» 
	# for sanction in sanctions:
	# 	print(sanction.text)
	# 	sanct.append(sanction.text)

	# ### Je me crée une petite boucle dans les cas où un pays est affecté par moins de 5 sanctions
	# ### S'il y a lieu, on ajoute du vide à la liste «sanct» autant de fois que nécessaire
	# for n in range(0,5-nbSanctions):
	# 	sanct.append("")

	# print(sanct)

	# ### On écrit notre liste dans le fichier CSV
	# kim = open(fichierCSV,"a")
	# jong_un = csv.writer(kim)
	# jong_un.writerow(sanct)

### ALTERNATIVE 2 -> Créer un fichier JSON
### Des données de ce type, difficilement plaçables dans un tableau, sont mieux adaptées à un fichier JSON

	sanct = {} ### Au lieu de créer une liste pour chaque pays, je crée plutôt un dictionnaire

	### Nom du pays
	nom = page2.h1.text[32:]
	if nom[0:4] == "à la":
		nom = nom[5:]
	elif nom[0:4] == "à l'":
		nom = nom[4:]
	else:
		nom = nom[3:]
	# print(nom)
	sanct["Pays"] = nom ### Je place dans mon dictionnaire une première paire clé-valeur; ici, la clé est «Pays» et la valeur est le nom du pays correspondant

	### Les dates des balises méta:
	dateEmission = page2.find("meta", attrs={"name":"dcterms.issued"})["content"]
	dateMAJ = page2.find("meta", attrs={"name":"dcterms.modified"})["content"]

	### Je les ajoute à ma liste
	sanct["Date d'émission"] = dateEmission
	sanct["Date de mise à jour"] = dateMAJ

	sanct["Sanctions"] = {}

	n = 0

	### On va maintenant chercher les sanctions
	for sanction in page2.find_all("div", class_="span-1"):
		n += 1
		sanct["Sanctions"]["Sanction-{}".format(n)] = sanction.text

	sanctions.append(sanct) ### Je place le contenu des infos du pays que je viens de ramasser dans ma grande variable sanctions
	print(sanctions)

### Une fois que tout est fait, je sors de la boucle et j'écris le tout dans un fichier JSON

with open(fichierJSON, 'w') as f:
  json.dump(sanctions, f)

### DERNIER COMMENTAIRE
### Un petit site comme ça ne nécessite pas de moissonnage.
### Il est plus simple de copier-coller les infos qui t'intéressent.
### Cela reste néanmoins un bon exercice :)