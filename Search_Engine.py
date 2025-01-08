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

    def tokeniser(self, texte):
        mots = re.findall(r'\b\w+\b', texte.lower())
        return sorted(set(mots))

    def construire_vocabulaire(self):
        vocabulaire = {}
        id_mot = 0
        for doc in self.corpus.id2doc.values():
            mots = self.tokeniser(doc.texte)
            for mot in mots:
                if mot not in vocabulaire:
                    vocabulaire[mot] = id_mot
                    id_mot += 1
        return vocabulaire

    def construire_matrice_tf(self):
        lignes, colonnes, donnees = [], [], []
        for i, doc in enumerate(self.corpus.id2doc.values()):
            mots = re.findall(r'\b\w+\b', doc.texte.lower())
            for mot in mots:
                if mot in self.vocabulaire:
                    lignes.append(i)
                    colonnes.append(self.vocabulaire[mot])
                    donnees.append(1)
        return csr_matrix((donnees, (lignes, colonnes)), shape=(len(self.corpus.id2doc), len(self.vocabulaire)))

    def calculer_doc_freq(self):
        return (self.matrice_tf_df > 0).sum(axis=0)

    def calculer_total_occurrences(self):
        return self.matrice_tf_df.drop('Document Frequency').sum(axis=0)

    def calculer_mat_TFxIDF(self):
        return self.tf_array * self.idf_array
    

    def search(self, mots_cles, n_docs):
        vecteur_requete = np.zeros((1, len(self.vocabulaire)))
        for mot in mots_cles:
            if mot in self.vocabulaire:
                vecteur_requete[0, self.vocabulaire[mot]] = 1
        scores = np.dot(vecteur_requete, self.mat_TFxIDF.T)
        scores = scores.flatten()
        sorted_indices = np.argsort(scores)[::-1]
        result_docs = []
        for index in tqdm(sorted_indices[:n_docs], desc="Recherche des documents"):
            result_docs.append((index + 1, scores[index]))
        result_df = pd.DataFrame(result_docs, columns=['Document', 'Score'])
        return result_df