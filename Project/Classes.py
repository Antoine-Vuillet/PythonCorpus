# Correction de G. Poux-Médard, 2021-2022

# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

# =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"

# =============== 2.3 : ACCESSEURS/MUTATEURS ===============
    def getTitre():
        return self.titre
    
    def setTitre(titre):
        self.titre = titre
    
    def getAuteur():
        return self.auteur
    
    def setAuteur(auteur):
        self.auteur = auteur
    
    def getDate():
        return self.date
    
    def setDate(date):
        self.date = date
    
    def getUrl():
        return self.url
    
    def setUrl(url):
        self.url = url

    def getTexte():
        return self.texte

    def setTexte(texte):
        self.texte = texte
# =============== 2.4 : La classe Author ===============
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
# =============== 2.5 : ADD ===============
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"


class RedditDocument(Document):
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="",nbcom=""):
        super().init(titre,auteur,date,url,texte)
        self.nbcom = nbcom
    
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"{super().__repr__}Nombre commentaire : {self.nbcom}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{super.__str__}, qui a reçu {self.nbcom} commentaires"

    # Fonction qui renvoie le nombre de commentaire
    def getNbCom():
        return self.nbcom

    # Fonction qui écrase le nombre de commentaire
    def setNbComt(nbcom):
        self.nbcom = nbcom
        

class ArxivDocument(Document):
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="",coaut=""):
        super().init(titre,auteur,date,url,texte)
        self.coaut = coaut
    
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"{super().__repr__}Co-auteur : {self.coaut}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{super.__str__}, qui a comme co-auteur {self.coaut}"

    # Fonction qui renvoie le nombre de commentaire
    def getCoAut():
        return self.coaut

    # Fonction qui écrase le nombre de commentaire
    def setCoAut(coauth):
        self.coaut = coaut