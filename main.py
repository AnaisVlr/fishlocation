import pandas as pd

df = pd.read_csv('premieres_1000_lignes.csv')

#Traitement du csv pour ne garder que certaines colonnes qui nous sont utiles
colonnes_a_conserver = ['taxonID', 'scientificName', 'vernacularName','decimalLatitude', 'decimalLongitude']

nouveau_df = df[colonnes_a_conserver]

# Créez un dictionnaire pour stocker les informations de chaque zone en utilisant les coordonnées comme clé
zones = {}

# Parcourez les lignes du DataFrame pour collecter les informations
for index, row in nouveau_df.iterrows():
    if 'decimalLatitude' in row and 'decimalLongitude' in row:
        # Créez une clé unique en fonction des coordonnées
        coord_key = (row['decimalLatitude'], row['decimalLongitude'])
        
        # Vérifiez si la zone existe déjà dans le dictionnaire
        if coord_key in zones:
            # La zone existe, ajoutez simplement le nom scientifique du poisson à la liste des poissons
            zone = zones[coord_key]
            # Vérifiez si le poisson n'est pas déjà dans la liste
            poisson = row['vernacularName']
            if poisson not in zone['poissons']:
                # Le poisson n'est pas dans la liste, ajoutez-le
                zone['poissons'].append(poisson)
        else:
            # La zone n'existe pas, créez une nouvelle zone
            zone = {
                'latitude': row['decimalLatitude'],
                'longitude': row['decimalLongitude'],
                'poissons': [row['vernacularName']]  # Créez une liste avec le premier poisson
            }
            
            # Ajoutez la zone au dictionnaire
            zones[coord_key] = zone