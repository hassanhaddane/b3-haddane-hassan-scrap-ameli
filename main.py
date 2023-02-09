import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

url = "http://annuairesante.ameli.fr/recherche.html"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/189.8.0.8 Safari/537.36"
}

req = requests.session()
payload= {
    "type": "ps",
    "ps_profession" : "34",
    "ps_profession_label": "Médecin généraliste",
    "ps_localisation": "HERAULT (34)",
    "localisation_category": "departements",
}

page = req.post(url, params=payload, headers=header)

if page.status_code == 200:
    lienrecherche = page.url

soup = BeautifulSoup(page.text, 'html.parser')

medecins = soup.find_all("div", class_="item-professionnel")

listeMedecins = []

for i in range(1001):
    for medecin in medecins[:70]:
        nomMedecins = medecin.find("div", class_="nom_pictos").text.strip()
        numeroMedecins = None
        if medecin.find("div", class_="tel") is not None:
            numeroMedecins = medecin.find("div", class_="tel").text.strip()
        adresseMedecins = medecin.find("div", class_="adresse").text.strip()
        listeMedecins.append({"nom": nomMedecins, "numero": numeroMedecins, "adresse": adresseMedecins})

# Création du fichier csv "medecins_generalistes.csv"
with open('medecins_generalistes.csv', 'w+') as fichier_csv:
    writer = csv.DictWriter(fichier_csv, fieldnames=listeMedecins[0].keys(), delimiter=";")
    writer.writeheader()
    writer.writerows(listeMedecins)


print(listeMedecins)