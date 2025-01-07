import document as doc


## Praw

import praw

reddit = praw.Reddit(client_id='8_lbD0GeZJjDSixOE5cDZQ', client_secret='H9yJeE1ipbTtSt1YETjbDbt2nIfIxg', user_agent='web scrapping LPK')


sub = reddit.subreddit('coronavirus')

docs = []

textes_reddit = [] 
for posts in sub.hot(limit=100):
    titre = posts.title
    texte = posts.selftext
    contenu_textuel = titre + ". " + texte
    contenu_textuel = contenu_textuel.replace("\n", " ")    
    textes_reddit.append(contenu_textuel)

#print(textes_reddit)

# les champs disponibles sont :
# title : titre du post
# score : score du post
# id : id du post
# subreddit : subreddit du post
# url : url du post
# num_comments : nombre de commentaires
# selftext : texte du post
# created : date de création du post
# author : auteur du post



## Arxiv

import urllib, urllib.request
import xmltodict

textes_arxiv = []

# query = "covid"
# url = "http://export.arxiv.org/api/query?search_query=all:" + query + "&start=0&max_results=100"
# url_read = urllib.request.urlopen(url).read()
# data = url_read.decode()
# print(url)

query = "covid"
url = "http://export.arxiv.org/api/query?search_query=all:" + query + "&start=0&max_results=100"
url_read = urllib.request.urlopen(url).read()
data = url_read.decode()

with open ("arxiv.xml", "w") as f:
    f.write(data)


dico = xmltodict.parse(data) #xmltodict permet d'obtenir un objet ~JSON
docs = dico['feed']['entry']


for d in docs : 
    texte = d['title']+"."+d['summary']
    texte = texte.replace("\n", " ")
    textes_arxiv.append(texte)

for t in textes_reddit[0:5]:
    print("reddit : " + t)

for t in textes_arxiv[0:5]:
    print("arxiv : " + t)
    
# les champs disponibles sont :
# title : titre du document

import pandas as pd

# Créer des identifiants uniques pour chaque texte
ids_reddit = list(range(1, len(textes_reddit) + 1))
ids_arxiv = list(range(len(textes_reddit) + 1, len(textes_reddit) + len(textes_arxiv) + 1))

# Créer des DataFrames pour chaque source
df_reddit = pd.DataFrame({
    'id': ids_reddit,
    'texte': textes_reddit,
    'origine': ['reddit'] * len(textes_reddit)
})

df_arxiv = pd.DataFrame({
    'id': ids_arxiv,
    'texte': textes_arxiv,
    'origine': ['arxiv'] * len(textes_arxiv)
})

# Concaténer les DataFrames
df = pd.concat([df_reddit, df_arxiv], ignore_index=True)

df.to_csv('data.csv', sep = '\t', index=False)

# Charger le DataFrame depuis le fichier .csv
df_loaded = pd.read_csv('data.csv', sep='\t')

# Afficher les premières lignes pour vérifier
print(df_loaded.head())


### Partie 3 ###

# Afficher la taille du corpus
print(f"Taille du corpus: {len(df_loaded)} documents")

# Calculer le nombre de mots et de phrases pour chaque document

for index, row in df_loaded.iterrows():
    texte = row['texte']
    mots = texte.split()
    phrases = texte.split('.')
    print(f"Document {row['id']} : {len(mots)} mots, {len(phrases)} phrases")

# Filtrer les documents trop petits (moins de 20 caractères)
df_filtered = df_loaded[df_loaded['texte'].str.len() >= 20]

chaine_texte = ' '.join(df_filtered['texte'])
print (chaine_texte)

import datetime

aujourdhui = datetime.datetime.now()