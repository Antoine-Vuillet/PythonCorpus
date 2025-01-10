import pandas as pd
import re
import numpy as np
from scipy.sparse import csr_matrix
from Corpus import Corpus, ArxivDocument
from tqdm import tqdm


class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocabulaire = self.construire_vocabulaire()
        self.matrice_tf = self.construire_matrice_tf()
        self.matrice_tf_df = pd.DataFrame(self.matrice_tf.toarray(), columns=self.vocabulaire.keys())
        self.doc_freq = self.calculer_doc_freq()
        self.matrice_tf_df.loc['Document Frequency'] = self.doc_freq
        self.total_occurrences = self.calculer_total_occurrences()
        self.matrice_tf_df.loc['Total Occurrences'] = self.total_occurrences
        self.N = len(self.corpus.id2doc)
        self.idf = np.log(self.N / (self.doc_freq + 1)) + 1
        self.tf_array = self.matrice_tf_df.drop(['Document Frequency', 'Total Occurrences']).to_numpy()
        self.idf_array = self.idf.to_numpy().reshape(1, -1)
        self.mat_TFxIDF = self.calculer_mat_TFxIDF()
        self.mat_TFxIDF_df = pd.DataFrame(self.mat_TFxIDF, columns=self.vocabulaire.keys())

    #Méthode tokenisant (divise en mot unique) un texte donné et renvoie les mots en ordre alphabétique
    def tokeniser(self, texte):
        mots = re.findall(r'\b[a-zA-Z]+\b', texte.lower())
        return sorted(set(mots))

    #Parcours les documents du corpus et attribue un identifiant à chaque mot
    def construire_vocabulaire(self):
        vocabulaire = {}
        id_mot = 0
        for doc in self.corpus.id2doc.values():
            #Divise le texte en mot uniques
            mots = self.tokeniser(doc.texte)
            for mot in mots:
                if mot not in vocabulaire:
                    vocabulaire[mot] = id_mot
                    id_mot += 1
        return vocabulaire

    #Construit une matrice de fréquence par mot pour le corpus
    def construire_matrice_tf(self):
        lignes, colonnes, donnees = [], [], []
        for i, doc in enumerate(self.corpus.id2doc.values()):
            mots = self.tokeniser(doc.texte) 
            for mot in mots:
                if mot in self.vocabulaire:
                    lignes.append(i)
                    colonnes.append(self.vocabulaire[mot])
                    donnees.append(1)
        return csr_matrix((donnees, (lignes, colonnes)), shape=(len(self.corpus.id2doc), len(self.vocabulaire)))

    #Calcule le nombre de document dans lequel chaque mot apparait
    def calculer_doc_freq(self):
        return (self.matrice_tf_df > 0).sum(axis=0)

    #Calcule le nombre de fois ou chaque mot apparait dans la totalité du corpus
    def calculer_total_occurrences(self):
        return self.matrice_tf_df.drop('Document Frequency').sum(axis=0)

    #Construit une matrice TF-IDF pour le corpus
    def calculer_mat_TFxIDF(self):
        return self.tf_array * self.idf_array
    
    #Recherche les documents les plus pertinents en fonction des mots clefs choisis
    def search(self, mots_cles, n_docs):
        vecteur_requete = np.zeros((1, len(self.vocabulaire)))
        # Pour chaque mot-clé dans la requête (mots_cles), marquer sa position dans le vecteur de requête si il est dans le vocabulaire
        for mot in mots_cles:
            if mot in self.vocabulaire:
                vecteur_requete[0, self.vocabulaire[mot]] = 1
        #Calcule la similarité cosinus en effectuant le produit entre le vecteur créé et la Transposée de la matrice tf-IDF
        scores = np.dot(vecteur_requete, self.mat_TFxIDF.T)
         # Aplatir les scores en un tableau 1D pour une manipulation plus facile
        scores = scores.flatten()
        # Trier les scores par ordre décroissant et obtenir les indices des scores triés
        sorted_indices = np.argsort(scores)[::-1]
        result_docs = []
        #Parcoure les scores et prends les "n_docs" plus haut
        for index in tqdm(sorted_indices[:n_docs], desc="Recherche des documents"):
            result_docs.append((index + 1, scores[index]))
        result_df = pd.DataFrame(result_docs, columns=['Document', 'Score'])
        return result_df