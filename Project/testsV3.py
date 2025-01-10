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
text2021 = "This is the text text"
text2022 = "This is the text text text"
text2023 = "This is the text text"
text2024 = "This is the text"
text2025 = "This is the "
nb_comments = 42
corp = Corpus.Corpus("thiscorpus")
years = ["2023","2024","2022","2023","2025","2024","2021","2023","2024","2022"]
# Loop through the years and create documents with different years
for year in years:
    # Format the date with the current year
    date = f"{year}/01/09"
    
    if year == "2021":
        text = text2021
    elif year == "2022":
        text = text2022
    elif year == "2023":
        text = text2023
    elif year == "2024":
        text = text2024
    elif year == "2025":
        text = text2025


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

def timeline_test():
    result = engine.timeline("text")
    if result["2023/01/09"] == 3:
        print("La méthode de timeline fonctionne")
    else:
        print("La méthode de timeline ne fonctionne pas")

timeline_test()
