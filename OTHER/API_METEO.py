import requests
import pandas as pd

# Récupération des données météo sur l'API
url='https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/download/?format=csv&refine.nom=TOULOUSE-BLAGNAC&refine.date=2022&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B'
res = requests.get(url)

# Lecture des données
output = res.content.decode()
with open('output.csv', 'w') as file:
    file.write(output)
df = pd.read_csv('output.csv',sep=';')

# Nettoyage des données
df.rename(columns={'Temp�rature':'Temperature'},inplace=True)
df['Temperature'] = df['Temperature']-273.15

# Suppression de toutes les colonnes qui ont plus de 20% de valeurs nulles
nb_na = df.isna().sum()
liste_suppr = []
for i in range(0,len(nb_na)):
    if nb_na[i] > df.shape[0]*0.2:
        liste_suppr.append(i)
df.drop(df.columns[liste_suppr], axis = 1, inplace = True)

# Création du dataset qui sera injecté dans la BDD
df_a_injec = df[['Date','Temperature','Direction du vent moyen 10 mn','Vitesse du vent moyen 10 mn']]
for i in range (0,df_a_injec.shape[0]):
    df_a_injec['Date'][i] = df_a_injec['Date'][i].replace('T','')
    df_a_injec['Date'][i] = df_a_injec['Date'][i][0:10]+' '+df_a_injec['Date'][i][10:18]
df_a_injec
pd.to_datetime(df_a_injec['Date'],format="%Y-%m-%d %H:%M:%S")
df_a_injec.set_index("Date",inplace = True)

# Création du CSV
# (temporaire -> à terme à intégrer dans l'architecture sans passer par un CSV pour permettre l'automatisation
df_a_injec.to_csv('Histo_meteo.csv')
