import Corpus
import numpy as np
import re
from scipy.sparse import csr_matrix
from tqdm import tqdm

class SearchEngine:
    def __init__(self, corpus):
        self.myCorp = corpus
        self.tfidftab = self.myCorp.construire_tab_doc_motTFIDF()

    def transform_query_to_vector(self,query, vocabulaire):
    # Nettoyage du texte
        cleaned_query = Corpus.Corpus.nettoyer_texte(query)

    #Création d'un dictionnaire copie de vocabulaire (même keys)
        query_dico = vocabulaire.copy()
    
    #Nettoyage des valeurs de notre nouveau dictionnaire
        for x in query_dico.keys():
            query_dico[x] = 0

    #Création d'un dictionnaire contenant les mots non référencés
        false_dico = dict()
    
    # Séparer le texte en mots
        mots = re.split(r'\s+|[^\w]+', cleaned_query)
    
    # Mettre à jour le vecteur en fonction des mots présents dans la requête
        for mot in mots:
            if mot in query_dico.keys():
                query_dico[mot] = 1 
            else:
                false_dico[mot] = 0
        return np.array(list(query_dico.values()))
  
    def similarité_cosinus(self,queryvect, docvect):
            if np.linalg.norm(queryvect) == 0 or np.linalg.norm(docvect) == 0:
                return 0.0
            return np.dot(queryvect,docvect)/(np.linalg.norm(queryvect)*np.linalg.norm(docvect))


        

    def compare_vectors(self,queryvect, doctab,num):
            similarities = []
            for i, doc_vector in tqdm(enumerate(doctab)):
                score = self.similarité_cosinus(queryvect, doc_vector)  # Calculer la similarité
                similarities.append((self.myCorp.id2doc[i + 1].getTitre(), score))  # Associer le document avec son score

            # Trier les documents par score (similarité)
            similarities.sort(key=lambda x: x[1], reverse=True)  # Tri par similarité décroissante
            return similarities[0:num]

    def get_user_query(self):
        query = input("Entrez des mots-clés pour la recherche : ")
        return query




    def search(self,num, query = ","):
            if query == ",":
                query = self.get_user_query()
            vocab = self.myCorp.construire_vocabulaire()
            query_vect = self.transform_query_to_vector(query,vocab)
            return self.compare_vectors(query_vect,self.tfidftab,num)
    

