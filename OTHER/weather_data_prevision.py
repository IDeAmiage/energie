from asyncio.windows_events import NULL

# Fonction qui calcul le DJU. On a utilisé la méthode costic (qui est utilisé par les professionnels)
def dju_costic(temp_min, temp_max):
    BASE_TEMP = 18
    
    DJU = NULL
    if(BASE_TEMP >= temp_max): # période hiver
        DJU = 18 - ((temp_min + temp_max)/2)
    elif(BASE_TEMP <= temp_min): # cas exceptionnel de début ou de fin de saison de chauffe
        DJU = 0
    elif (temp_min < BASE_TEMP < temp_max): # cas possible en début ou fin de saison de chauffe
        b = (18 - temp_min)/(temp_max - temp_min)
        a = temp_max - temp_min
        DJU = a*b*(0.08 + 0.42*b)
    
    return DJU


# Fonction de récupération des données prévisionnelles de la météo
def get_weather_data():

    import requests 
    import pandas as pd
    from settings import apiKey # il faut créer le fichier settings dans lequel on met la clée de l'API.  

    KEY = apiKey
    # L'URL : ici on utilise l'API Open Weather Map. Il faut créer un compte et générer une clé (apiKey)
    # C'est cette clé qui va permettre de pouvoir requeter l'API. 
    url = "http://api.openweathermap.org/data/2.5/forecast?q=toulouse&lang=fr&units=metric&appid="+KEY
    r = requests.get(url = url) 
  
    #  Récupération des données en format JSON
    data = r.json() 

    #  Création du dataframe vide
    df = pd.DataFrame(columns=['datetime', 'temp', 'temp_min', 'temp_max', 'DJU', 'humidity', 'windSpeed', 'windDir'])

    # On parcours le resultat (data) et pour chaque jour on récuprère les données qui nous intéresse
    for sample in  data['list']:
        # Calcul du DJU
        dju = dju_costic(round(sample['main']['temp_min']), (sample['main']['temp_max']))
        # Création d'une ligne
        row = {'datetime':sample['dt_txt'], 'temp': (sample['main']['temp']), 
        'temp_min':(sample['main']['temp_min']), 'temp_max':(sample['main']['temp_max']), 
        'DJU':dju, 'humidity':sample['main']['humidity'],'windSpeed':sample['wind']['speed'], 'windDir':sample['wind']['deg']}
        print(row)
        df = df.append(row, ignore_index=True)
    df=df.set_index('datetime')

    return df
    # print(data)






#  Le main
if __name__ == '__main__':
    import pandas as pd
    import csv

    #  On lit le CSV (notre base de données)
    data = pd.read_csv('database.csv')
    date_time = data['datetime'].to_list()
    #  On lance la fonction qui récupère les données
    df = get_weather_data()
    

    # On récupère et ajouter à la base de données (CSV) les nouvelles données 
    # qui n'étaient pas encore dans la base
    for i in df.index:
        # print(df)
        if(i not in date_time):
            fichier = open('database.csv','a', newline='')
            #Créer l'objet fichier
            obj = csv.writer(fichier)
            #Creer une ligne de data
            sample = (i, df['temp'][i], df['temp_min'][i], df['temp_max'][i], 
                    df['DJU'][i], df['humidity'][i], df['windSpeed'][i], df['windDir'][i],)
            # print(sample)
            obj.writerow(sample)
            fichier.close()
