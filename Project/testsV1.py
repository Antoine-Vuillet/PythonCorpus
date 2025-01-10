import Classes
import Corpus



def add_author_test():
    author = Classes.Author("Pierre")
    author.add("newDocument")
    if author.ndoc==1 and author.production[0] == "newDocument":
        print("Le test de la fonction add() d'Auteur fonctionne")
    else:
        print("le test de la fonction add() d'Auteur ne fonctionne pas")

def newDocumentTest():
    arxiv_doc = Classes.ArxivDocument(
        titre="ArxivTitle",
        auteur="John Doe",
        date="2025/01/10",
        url="Non",
        texte="This is the text",
        co_auteurs=["John John", "Doe Doe"]
    )
    reddit_doc = Classes.RedditDocument(
        titre="RedditTitle",
        auteur="Jane Doe",
        date="2025/01/09",
        url="Non",
        texte="This is the text",
        nb_comments=42
    )
    if reddit_doc.getType() == "RedditDocument" :
        print("La création d'un document de type RedditDocument fonctionne")
    else:
        print("La création d'un document de type RedditDocument ne fonctionne pas")
    if arxiv_doc.getType() == "ArxivDocument" :
        print("La création d'un document de type ArxivDocument fonctionne")
    else:
        print("La création d'un document de type ArxivDocument ne fonctionne pas")


def additionToCorpus_test():
    arxiv_doc = Classes.ArxivDocument(
        titre="ArxivTitle",
        auteur="John Doe",
        date="2025/01/10",
        url="Non",
        texte="This is the text",
        co_auteurs=["John John", "Doe Doe"]
    )
    reddit_doc = Classes.RedditDocument(
        titre="RedditTitle",
        auteur="Jane Doe",
        date="2025/01/09",
        url="Non",
        texte="This is the text",
        nb_comments=42
    )
    corp = Corpus.Corpus("thiscorpus")
    corp.add(reddit_doc)
    corp.add(arxiv_doc)
    if corp.ndoc == 2:
        print("L'addition de nouveaux documents au corpus fonctionne")
    else:
        print("L'addition de nouveaux documents au corpus ne fonctionne pas")
    vocab = corp.construire_vocabulaire()
    if len(vocab)>0:
        print("La création du vocabulaire fonctionne")
    else:
        print("La création du vocabulaire ne fonctionne pas")


add_author_test()
newDocumentTest()
additionToCorpus_test()