# PythonCorpus

Exemple d’utilisation : 

le programme suit le schéma d’utilisation suivant : 
## création du corpus
## initialisation du moteur de recherche
## utilisation des différentes fonctionnalités du moteur de recherche.


## création du corpus
  La première étape de l’utilisation du programme est la création d’un corpus qui peut être réalisé via les différentes API (ex : creation_corpus.py) ou     
  l’instanciation d’un objet de la classe corpus créé à partir de données.

## initialisation du moteur de recherche
  Une fois le corpus importé, le moteur de recherche est initialisé à partir du corpus et génère les données nécessaires à l’emploi de ses différentes 
  fonctionnalités.

## le moteur de recherche présent dans l’application permet de réaliser un certains nombres d’opérations.
  La recherche d’un terme au sein du corpus, permettant de sélectionner le nombre de documents à retourner en résultats. et affichant l’index du document dans     lequel le terme à été trouvé ainsi que son score (tf-idf), par lesquels ils sont rangés dans l’ordre décroissant 

## utilisation des différentes fonctionnalités du moteur de recherche.

- La construction d’un vocabulaire, les mots du corpus sont intégrés dans un ensemble d’éléments distincts et indexés. cet ensemble est affichable est consultable par l’utilisateur
- l’affichage de la fréquence documentaire  et du nombre total d'occurrences de chaque termes dans le corpus
- l’affichage des matrices TF et TF-IDF
- affichage de l’évolution dans le temps de l'occurrence d’un terme dans le corpus
