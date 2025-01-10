import Classes
import Corpus
import Search_Engine


#Création du corpus de base
documents = []

# Define other constant attributes
title = "RedditTitle"
author = "Doe Doe"
date_format = "YYYY/01/09"  # You can customize this format if needed
url = "Non"
text = "This is the text"
nb_comments = 42
corp = Corpus.Corpus("thiscorpus")
years = [2023,2024,2022,2023,2025,2024,2021,2023,2024,2022]
# Loop through the years and create documents with different years
for year in years:
    # Format the date with the current year
    date = f"{year}/01/09"
    
    # Create the document and append it to the list
    document = Classes.RedditDocument(
        titre=title,
        auteur=author,
        date=date,
        url=url,
        texte=text,
        nb_comments=nb_comments
    )
    corp.add(document)  

engine = Search_Engine.SearchEngine(corp)

print(engine.timeline("text"))
    
