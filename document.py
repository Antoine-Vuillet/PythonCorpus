# =============== 2.1 : La classe Document ===============
class Documents:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = "Documents"

# =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\tType : {self.type}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
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
    
class RedditDocument (Documents):
    
    def __init__(self, titre="", auteur="", date="", url="", texte="", nb_comments=0):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_comments = nb_comments
        self.type = self.getType()
        
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t# Nombre commentaire : {self.nb_comments}\t"
    
    def __str__(self):
        return f"{self.titre}, par {self.auteur}, # Nombre commentaire : {self.nb_comments}"

    def getType(self):
        return "RedditDocument"
class ArxivDocument(Documents):
    
    def __init__(self, titre="", auteur="", date="", url="", texte="", co_auteurs=None):
        if co_auteurs is None:
            co_auteurs = []
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs
        self.type = self.getType()

    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\tCo-auteurs : {', '.join(self.co_auteurs)}\t"

    def __str__(self):
        return f"{self.titre}, par {self.auteur}, Co-auteurs : {', '.join(self.co_auteurs)}"
    def getType(self):
        return "ArxivDocument"