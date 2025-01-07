import praw;
import urllib.request as req
import xmltodict
import pandas as pd
'''docs = [];

#reddit = praw.Reddit(client_id='_CatCjIAUe7w15loxjHQ_Q', client_secret='I7inFd8ZcNcr_uiJUBpq2xAe8ogvEQ', user_agent='WebScraping');
#hot_posts = reddit.subreddit('MachineLearning').hot(limit=10);


##L'api a comme champ :subreddit,submission et le reste peu importe
##les posts ont comme champs : title, score, id, subreddit, url, num_comments,selftext et created

for x in hot_posts:
    docs.append([x.selftext.replace("\n",""),"reddit"]);

##ARXIV
url = "http://export.arxiv.org/api/query?search_query=all:electron+AND+all:proton"
u = req.urlopen(url)
content = u.read()
xmlstr = content.decode('utf8') 
newdict = xmltodict.parse(xmlstr)
df = pd.DataFrame(newdict["feed"]["entry"])
for x in df['summary']:
    docs.append(x)


dfTextes = pd.DataFrame(columns=['id','text','origine'])
for i in range(0,len(docs)):
    if docs[i][1]=="reddit":
        new =pd.DataFrame({'id': [i], 'text': [docs[i][0]], 'origine': [docs[i][1]]})
        dfTextes = pd.concat([dfTextes,new])
    else:
        new =pd.DataFrame({'id': [i], 'text': [docs[i]], 'origine': ["arxiv"]})
        dfTextes = pd.concat([dfTextes,new])

dfTextes.to_csv("./TP3.csv", index = False, header = True, sep ="\t");
'''
readData = pd.read_csv("TP3.csv",sep="\t")
#print(readData.iloc[-1,0])
'''
def nombremot():
    nbr = []
    for x in readData['text']:
        try:
            nbr.append(len(x.split(" ")))
        except:
            nbr.append(0)
    return nbr
print(nombremot())

def nombrephrase():
    nbr = []
    for x in readData['text']:
        try:
            nbr.append(len(x.split(".")))
        except:
            nbr.append(0)
    return nbr
print(nombrephrase())
'''
def lessthantwenty():
    global readData
    droper = []
    for x in range(0,len(readData['text'])-1):
        try:
            if(len(readData['text'][x])<20):
                droper.append(x)
        except:
            droper.append(x)
    readData = readData.drop(droper)
lessthantwenty()
print(readData)

def singleline():
    global readData
    line = ""
    for x in readData['text']:
        line = line + x
    return line
print(singleline())