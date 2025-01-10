import Classes
import Corpus
import Search_Engine

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

def searchEnginecreation_test():
    engine =Search_Engine.SearchEngine(corp)
    if len(engine.vocabulaire) > 0:
        print("La création du  moteur de recherche fonctionne")
    else:
        print("La création du moteur de recherche ne fonctionne pas")

def searching_test():
    test_doc = Classes.RedditDocument(
        titre="testing",
        auteur="Jane Doe",
        date="2025/01/09",
        url="Non",
        texte="Absurd new text",
        nb_comments=42
    )
    corp.add(test_doc)
    engine = Search_Engine.SearchEngine(corp)
    print(engine.vocabulaire)
    result_df =engine.search(["this"],2)
    if 3 in result_df["Document"].values:
        print("La recherche dans les documents ne fonctionne pas")
    else:
        print("La recherche dans les documents fonctionne")

searchEnginecreation_test()
searching_test()