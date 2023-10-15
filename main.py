import pandas as pd

df = pd.read_csv('premieres_1000_lignes.csv')

df = df[['taxonID', 'scientificName','originalNameUsage','vernacularName','decimalLatitude', 'decimalLongitude', 'stateProvince', 'locality', 'eventDate']]


print(df.head)
