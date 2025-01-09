import praw
import urllib.request
import xmltodict
import datetime
import pickle
from Classes import RedditDocument, ArxivDocument
from Corpus import Corpus

# Identification Reddit
reddit = praw.Reddit(client_id='8_lbD0GeZJjDSixOE5cDZQ', client_secret='H9yJeE1ipbTtSt1YETjbDbt2nIfIxg', user_agent='web scrapping LPK')

# Requête Reddit
limit = 100
hot_posts = reddit.subreddit('artificial').hot(limit=limit)

# Récupération des posts Reddit
docs_bruts = []
for post in hot_posts:
    if post.selftext != "":
        titre = post.title.replace("\n", '')
        auteur = str(post.author)
        date = datetime.datetime.fromtimestamp(post.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/" + post.permalink
        texte = post.selftext.replace("\n", "")
        nb_comments = post.num_comments
        doc_classe = RedditDocument(titre, auteur, date, url, texte, nb_comments)
        docs_bruts.append(("Reddit", doc_classe))

# Requête ArXiv
query_terms = ["artificial intelligence"]
max_results = 50
encoded_query = urllib.parse.quote(" ".join(query_terms))
url = f'http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)
data = xmltodict.parse(data.read().decode('utf-8'))

# Récupération des articles ArXiv
if "entry" in data["feed"]:
    for entry in data["feed"]["entry"]:
        titre = entry["title"].replace('\n', '')
        authors = entry["author"]
        date = datetime.datetime.strptime(entry["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")
        summary = entry["summary"]
        if isinstance(authors, list):
            first_author = authors[0]["name"]
            co_auteurs = [author["name"] for author in authors[1:]]
        else:
            first_author = authors["name"]
            co_auteurs = []
        doc_classe = ArxivDocument(titre, first_author, date, entry["id"], summary, co_auteurs)
        docs_bruts.append(("ArXiv", doc_classe))
else:
    print("Aucun article trouvé pour la requête ArXiv.")


# Création du corpus
corpus = Corpus("Corpus sur l'intelligence artificielle")
for nature, doc in docs_bruts:
    corpus.add(doc)

# Sauvegarde du corpus
with open("corpus_ai.pkl", "wb") as f:
    pickle.dump(corpus, f)

print("Corpus créé et sauvegardé avec succès.")
