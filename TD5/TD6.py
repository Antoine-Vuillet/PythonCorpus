import pickle
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

w =corpus.search("data")

print(w)

print(corpus.concorde("data",17))
freq_table = corpus.construire_tableau_freq()

# Afficher le tableau enrichi
print(freq_table.head(10))