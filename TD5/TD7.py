import pickle
import SearchEngine as s
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

searcheng = s.SearchEngine(corpus)
simil = searcheng.search(400)
print(simil)
