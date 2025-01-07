class Document:
    def __init__(self,titre,auteur,date,url,texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    def affichage():
        print("Ce document a comme titre "+self.titre+" , il a été écris par "+self.auteur+" le "+self.date+". \nSon url est "+self.url+" \n"+self.texte)

    def __str__():
        print("Le titre est "+self.titre)