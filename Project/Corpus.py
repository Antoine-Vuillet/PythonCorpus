# Correction de G. Poux-Médard, 2021-2022

from Classes import Author, ArxivDocument
import re
import pandas as pd


# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        # Gérer l'auteur principal
        auteur_principal = doc.auteur if isinstance(doc.auteur, str) else str(doc.auteur)
        if auteur_principal not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(auteur_principal)
            self.aut2id[auteur_principal] = self.naut
        self.authors[self.aut2id[auteur_principal]].add(doc.texte)

        # Gérer les co-auteurs
        if isinstance(doc, ArxivDocument):
            for co_auteur in doc.co_auteurs:
                co_auteur_str = co_auteur if isinstance(co_auteur, str) else str(co_auteur)
                if (co_auteur_str not in self.aut2id):
                    self.naut += 1
                    self.authors[self.naut] = Author(co_auteur_str)
                    self.aut2id[co_auteur_str] = self.naut
                self.authors[self.aut2id[co_auteur_str]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        for doc in docs:
            print(f"{repr(doc)}\tType : {doc.getType()}")

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))
        return "\n".join([f"{str(doc)}\tType : {doc.getType()}" for doc in docs])

    # def search(self,)
    
    def generer_chaine(self):
        return ' '.join(doc.texte for doc in self.id2doc.values())
    
    def search(self, keywords):
        results = []
        corpus_text = self.generer_chaine()
        passages = re.findall(r'([^.]*?(' + '|'.join(re.escape(keyword) for keyword in keywords) + ')[^.]*\.)', corpus_text, re.IGNORECASE)
        for passage in passages:
            results.append(passage[0])
        return results

    
    def concorde (self, expression, taille_contexte):
        results = []
        corpus_text = self.generer_chaine()
        pattern = re.compile(r'(.{0,' + str(taille_contexte) + r'})(' + re.escape(expression) + r')(.{0,' + str(taille_contexte) + r'})', re.IGNORECASE)
        matches = pattern.findall(corpus_text)
        for match in matches:
            gauche, motif, droit = match
            results.append([gauche.strip(), motif, droit.strip()])
        df = pd.DataFrame(results, columns=['Contexte gauche', 'Motif trouvé', 'Contexte droit'])
        return df

    def nettoyer_texte(self,texte):
        # Mise en minuscule
        texte = texte.lower()
        
        # Remplacement des passages à la ligne
        texte = texte.replace('\n', ' ')
        
        # Remplacement des ponctuations et des chiffres
        texte = re.sub(r'[^\w\s]', ' ', texte)  # Remplace les ponctuations par des espaces
        texte = re.sub(r'\d+', ' ', texte)  # Remplace les chiffres par des espaces
        
        # Suppression des espaces multiples
        texte = re.sub(r'\s+', ' ', texte).strip()
        return texte

    def construire_vocabulaire(self):
        vocabulaire = set()
        for doc in self.id2doc.values():
            mots = self.nettoyer_texte(doc.texte).split()
            vocabulaire.update(mots)
        return {mot: idx for idx, mot in enumerate(vocabulaire)}
    
    
    def construire_tableau_freq(self):
        vocabulaire = self.construire_vocabulaire()
        freq = pd.DataFrame(0, index=self.id2doc.keys(), columns=vocabulaire.keys())
        
        for doc_id, doc in self.id2doc.items():
            mots = self.nettoyer_texte(doc.texte).split()
            for mot in mots:
                if mot in vocabulaire:
                    freq.at[doc_id, mot] += 1
                    
        doc_freq = self.calculer_document_frequency(freq)
        
        freq.loc['Document Frequency'] = doc_freq
        
        return freq

    def calculer_document_frequency(self, freq):
        doc_freq = (freq > 0).sum(axis=0)
        return doc_freq

    def stats(self, d):
        vocabulaire = self.construire_vocabulaire()
        tableau_freq = self.construire_tableau_freq()
        
        # Affichage du tableau de fréquence
        print("\nTableau de fréquence :")
        print(tableau_freq)
        
        # Nombre de mots différents
        nb_mots_differents = len(vocabulaire)
        print(f"Nombre de mots différents dans le corpus: {nb_mots_differents}")
        
        # Les n mots les plus fréquents
        n = d  # Nombre de mots à afficher
        mots_les_plus_frequents = tableau_freq.loc['Document Frequency'].sort_values(ascending=False).head(n)
        print(f"Les {n} mots les plus fréquents dans le corpus:")
        print(mots_les_plus_frequents)


