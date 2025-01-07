# Correction de G. Poux-Médard, 2021-2022
import re
import pandas
from Classes import Author
from scipy.sparse import csr_matrix

import numpy as np

# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.fullchaine = ""

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

# =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))

    def search(self, mot):
        if self.fullchaine == "":
            self.fullchaine = "".join(doc.getTexte() for doc in self.id2doc.values())
        res= re.findall(rf"(.*?\b{mot}\b.*?)", self.fullchaine, re.IGNORECASE)
        return res


    def concorde(self, mot, contexte=17):
        if self.fullchaine == "":
            self.fullchaine = "".join(doc.getTexte() for doc in self.id2doc.values())
        pattern = rf"(?:.{{0,{contexte}}})(?P<motif>{mot})(?:.{{0,{contexte}}})"
        matches = re.finditer(pattern, self.fullchaine, re.IGNORECASE)

        # Construire les données pour le DataFrame
        data = []
        for match in matches:
            # Extraire les positions du motif trouvé
            start, end = match.span("motif")
            contexte_gauche = self.fullchaine[max(0, start - contexte):start]
            motif_trouve = match.group("motif")
            contexte_droit = self.fullchaine[end:end + contexte]
            
            # Ajouter les données au tableau
            data.append({
                "contexte gauche": contexte_gauche.strip(),
                "motif trouvé": motif_trouve,
                "contexte droit": contexte_droit.strip(),
            })

        # Créer un DataFrame
        df = pandas.DataFrame(data, columns=["contexte gauche", "motif trouvé", "contexte droit"])
        
        return df
    
    def nettoyer_texte(chaine):
        if not isinstance(chaine, str):  # Si l'entrée n'est pas une chaîne, retournez une chaîne vide
            return ""
        chaine = chaine.lower()
        chaine.replace("\n"," ").replace("0","zero").replace("1","un").replace("2","deux").replace("3","trois").replace("4","quatre").replace("5","cinq").replace("6","six").replace("7","sept").replace("8","huit").replace("9","neuf")
        chaine = re.sub(r"[^\w\s]", " ", chaine)
        chaine = re.sub(r"\s+", " ", chaine)
        return chaine.strip()

    def construire_vocabulaire(self):
        vocabulaire = {}
        for doc in self.id2doc.values():
            texte = Corpus.nettoyer_texte(doc.getTexte())
            mots = re.split(r'\s+|[^\w]+', texte)  # Séparer par espaces ou ponctuation
            for mot in mots:
                if mot:  # Ignorer les chaînes vides
                    vocabulaire[mot] = vocabulaire.get(mot, 0) + 1
        return vocabulaire

    #Pour chaque mot, donne un tableau contenant pour chaque mot sa fréquence dans le document et le nombre de documents où il apparait
    def construire_tableau_freq(self):
        term_freq = {}  # TF
        doc_freq = {}   # IDF

        # Parcourir les documents
        for doc in self.id2doc.values():
            texte = doc.getTexte()

            texte = Corpus.nettoyer_texte(texte)
            mots = re.split(r'\s+|[^\w]+', texte)  # Séparer par espaces ou ponctuation
            mots_uniques = set()  # Utiliser un ensemble pour trouver les mots uniques dans ce document

            for mot in mots:
                if mot:  # Ignorer les chaînes vides
                    term_freq[mot] = term_freq.get(mot, 0) + 1
                    mots_uniques.add(mot)

            # Mettre à jour la fréquence des documents pour chaque mot unique
            for mot in mots_uniques:
                doc_freq[mot] = doc_freq.get(mot, 0) + 1

        # Construire un DataFrame
        data = [{"Mot": mot, "Term Frequency": tf, "Document Frequency": doc_freq[mot]}
                for mot, tf in term_freq.items()]
        freq_df = pandas.DataFrame(data)
        freq_df = freq_df.sort_values(by="Term Frequency", ascending=False).reset_index(drop=True)
        
        return freq_df
    
    def construire_tab_doc_motTF(self):
        indptr = [0]
        indices = []
        data = []
        vocabulary = {}
        for doc in self.id2doc.values():
            texte = Corpus.nettoyer_texte(doc.getTexte())
            mots = re.split(r'\s+|[^\w]+', texte)  # Séparer par espaces ou ponctuation
            for mot in mots:
                index = vocabulary.setdefault(mot, len(vocabulary))
                indices.append(index)
                data.append(1)
            indptr.append(len(indices))
        return csr_matrix((data, indices, indptr), dtype=int).toarray()
    
    def construire_tab_doc_motTFIDF(self):
        indptr = [0]
        indices = []
        data = []
        vocabulary = {}

        # Get the Document Frequency (DF) for each word
        df = self.construire_tableau_freq()
        doc_freq = df.set_index("Mot")["Document Frequency"].to_dict()

        for doc in self.id2doc.values():
            texte = Corpus.nettoyer_texte(doc.getTexte())
            mots = re.split(r'\s+|[^\w]+', texte)  # Séparer par espaces ou ponctuation
            
            for mot in mots:
                if mot:  # Ignorer les chaînes vides
                    # Add word to vocabulary if not already present
                    index = vocabulary.setdefault(mot, len(vocabulary))
                    indices.append(index)
                    data.append(1)  # All occurrences will get a TF of 1 initially
            
            indptr.append(len(indices))
        
        # Map each word occurrence (by its index) to its document frequency
        tfidf_data = np.multiply(data, [doc_freq.get(list(vocabulary.keys())[index], 0) for index in indices])

        # Create the CSR matrix with the updated data
        return csr_matrix((tfidf_data, indices, indptr), dtype=int).toarray()
