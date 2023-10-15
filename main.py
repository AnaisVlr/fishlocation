import pandas as pd

df = pd.read_csv('premieres_1000_lignes.csv')

df = df[['taxonID', 'scientificName','originalNameUsage','vernacularName','decimalLatitude', 'decimalLongitude', 'stateProvince', 'locality', 'eventDate']]

zones = []


for index, row in df.iterrows():
    if 'decimalLatitude' in row and 'decimalLongitude' in row:
        zone = {
            'latitude': row['decimalLatitude'],
            'longitude': row['decimalLongitude']
        }
        zones.append(zone)
