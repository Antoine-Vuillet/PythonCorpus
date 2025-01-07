#%%
import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
#with open('E:/Master/Python/evg_esp_veg.envpdiprboucle.json', 'r') as f:
#  d_json = json.load(f)


#var = d_json['fields']
#rando = d_json['values']
#print(len(rando))
#print(rando[10]['nom'])

##Partie 2
#df =pd.DataFrame.from_dict(rando)
#print(df.head())
#print(df.tail())
#print(df.iloc[:,2:6])
#print(df["difficulte"].value_counts())
#print(df["temps_parcours"])
#df["temps_parcours"] = [int(x[:-3]) for x in df["temps_parcours"]]
#print(df["temps_parcours"])
#print(df["temps_parcours"].mean())
#print(df.groupby(['difficulte'])["temps_parcours"].mean())


##Partie 3
#counting = df["difficulte"].value_counts().sort_index()
#counting.plot.bar()
#counting.plot.pie()
#plt.show()


##Partie 4
#df["longueur"] = [x.replace(",",".") for x in df["longueur"]]
#df["longueur"] = [float(x[:-2]) for x in df["longueur"]]
#print(df["longueur"])
#ax =df.plot.scatter(x="longueur",y="temps_parcours")
#ax.set_title("Temps de parcours en fonction de la longueur")
#ax.set_xlabel("km")
#ax.set_ylabel("min")
#plt.show()
#dataframe_corr = pd.DataFrame({"longueur" : df["longueur"], "temps_parcours" : df["temps_parcours"]})
#print(dataframe_corr.corr())


##Partie 5
df_carac = pd.read_csv('caracteristiques-2018.csv', encoding='ISO-8859-1')
df_usagers = pd.read_csv('usagers-2018.csv')
df_vehicules = pd.read_csv('vehicules-2018.csv')
df_lieux = pd.read_csv('lieux-2018.csv')


accidents_lyon = df_carac[df_carac['dep']==690].copy()
accidents_velo= df_vehicules[df_vehicules['catv']== 1].copy()
accidents_paris = df_carac[df_carac['dep']==750].copy()
accidents_marseille = df_carac[df_carac['dep']==130].copy()
accidents_Toulouse = df_carac[df_carac['dep']==310].copy()

accidents_lyelo = accidents_lyon.set_index('Num_Acc').join(accidents_velo.set_index('Num_Acc'),None,'inner')

accident_grandville = pd.concat([accidents_lyon,accidents_paris,accidents_marseille,accidents_Toulouse])
df_grandville =accident_grandville.set_index('Num_Acc').join(accidents_velo.set_index('Num_Acc'),None,'inner')
df_detout = df_carac.set_index('Num_Acc').join(accidents_velo.set_index('Num_Acc'),None,'inner')

counting = df_detout["dep"].value_counts().sort_index()
counting.plot.bar()
plt.show()
counting = df_grandville["dep"].value_counts().sort_index()
counting.plot.bar()
plt.show()
