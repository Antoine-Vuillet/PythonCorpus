import pandas
from Corpus import Corpus
from Classes import Document
import SearchEngine as s
df_discours =pandas.read_csv(r'C:\Users\antoi\Documents\Etudes\Cours lyon\Python\TD5\discours_US.csv', sep ="\t")
corp = Corpus('TD8')
for index, row in df_discours.iterrows():
    phrases =row['text'].split(".")
    for k in phrases:
        if k != "":
            corp.add(Document(row["descr"],row['speaker'],row['date'],row['link'],k))
engine = s.SearchEngine(corp)
simil =engine.search(100)
print(simil)