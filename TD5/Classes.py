# Correction de G. Poux-Médard, 2021-2022

# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="", montype=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = montype

# =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"

# =============== 2.3 : ACCESSEURS/MUTATEURS ===============
    def getTitre(self):
        return self.titre
    
    def setTitre(self,titre):
        self.titre = titre
    
    def getAuteur(self):
        return self.auteur
    
    def setAuteur(self,auteur):
        self.auteur = auteur
    
    def getDate(self):
        return self.date
    
    def setDate(self,date):
        self.date = date
    
    def getUrl(self):
        return self.url
    
    def setUrl(self,url):
        self.url = url

    def getTexte(self):
        return self.texte

    def setTexte(self,texte):
        self.texte = texte

    def getType(self):
        pass
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

        

class ArxivDocument(Document):
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        auteurs = auteur.split(",")
        self.coaut = ""
        if(len(auteurs)>1):
            self.coaut= ",".join(auteurs[i] for i in range(1,len(auteurs)))
            auteur = auteurs[0]
        super().__init__(titre,auteur,date,url,texte, "Arxiv")
    
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"{super().__repr__()}Co-auteur : {self.coaut}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        if len(self.auteur)>1:
            return f"{super().__str__()}, qui a comme co-auteur {self.coaut} et qui viens de {self.type}"
        else:
            return f"{super().__str__()} qui viens de {self.type}"

    # Fonction qui renvoie le nombre de commentaire
    def getCoAut(self):
        return self.coaut

    # Fonction qui écrase le nombre de commentaire
    def setCoAut(self,coaut):
        self.coaut = coaut
    
    def getType(self):
        return "Arxiv"

class RedditDocument(Document):
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="",nbcom=""):
        super().__init__(titre,auteur,date,url,texte, "Reddit")
        self.nbcom = nbcom
    
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"{super().__repr__()}Nombre commentaire : {self.nbcom}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{super().__str__()}, qui a reçu {self.nbcom} commentaires et qui viens de {self.type}"

    # Fonction qui renvoie le nombre de commentaire
    def getNbCom(self):
        return self.nbcom

    # Fonction qui écrase le nombre de commentaire
    def setNbComt(self,nbcom):
        self.nbcom = nbcom
    
    def getType(self):
        return "Reddit"