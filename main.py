import pandas as pd

df = pd.read_csv('premieres_1000_lignes.csv')

#Traitement du csv pour ne garder que certaines colonnes qui nous sont utiles
colonnes_a_conserver = ['taxonID', 'scientificName', 'vernacularName','decimalLatitude', 'decimalLongitude']

nouveau_df = df[colonnes_a_conserver]

#Création d'une liste de dictionnaires contenant la position des zones de prélèvement
zones = []

for index, row in df.iterrows():
    if 'decimalLatitude' in row and 'decimalLongitude' in row:
        zone = {
            'latitude': row['decimalLatitude'],
            'longitude': row['decimalLongitude']
        }
        zones.append(zone)
