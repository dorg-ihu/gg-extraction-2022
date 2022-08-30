import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

# Read file
filename = "final_kodiko_data.csv"
indata = pd.read_csv(filename, keep_default_na=False)

# Find duplicates and remove
data = indata.drop_duplicates(keep='last')
dupsmask = indata.duplicated()
dups = indata[dupsmask]

data["key_split"] = [x.split(" ")[0] for x in data["key"]]
data["key_split"] = [x.split(".")[0] for x in data["key_split"]]

# Take unique values of column key_split
counts = data["key_split"].value_counts()
# Παρ 69701
# Άρθρο ~32829

number_of_articles = sum([1 if x and y else 0 for x, y in zip(data["title"], data["content"])])

pds = data.groupby("identity").size()

pds.min()
pds.max()
pds.std()
round(pds.mean(), 2)
pds.median()

data["year"] = [x.rsplit("/", 1)[-1] for x in data["identity"]]
data["year"].value_counts()
pds_per_year = data.groupby(["year", "identity"]).size().reset_index().groupby("year").size()
pds_per_year.plot(kind='bar', color='b', alpha=0.7, rot=70, fontsize=8, ylabel="Number of PDs", xlabel="Publication Year")


#pds_per_year = data.groupby(["year", "identity"]).count().reset_index().groupby("year").count()




data["clean_content"] = [x if not x.isspace() else "" for x in data["content"]]
unique_contents = data["clean_content"].drop_duplicates(keep='last').reset_index(drop=True)

# import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import string
from string import digits

extra_stopwords = ["ως", "εν", "ν", "–", "κλπ", "’", "•", "ΥΕ", "ΠΕ", "ή", "τη", "της", "σημ", "όπως", 
                   "a", "α", "δ", "β", "ε", "καθώς", "γ", "από", "τους", "ζ", "στ", "λς"]
stop = stopwords.words('greek')
stop.extend(extra_stopwords)
stopwords_dict = Counter(stop)

# clean stopwords, puncutation and numbers
#clean_dups = [" ".join([word if word not in stopwords_dict for text in dups for word in text])]
def remove_punct_and_digits(x):
    return x.translate(str.maketrans("", "", string.punctuation)).translate(str.maketrans("", "", digits))
    

clean_dups = []
for text in unique_contents:
    text = remove_punct_and_digits(text)
    temp_list = []
    words = word_tokenize(text)
    for word in words:
        if word.lower() not in stopwords_dict:
            temp_list.append(word.lower())
    clean_dups.append(' '.join(temp_list))
    
wordcloudlist = ' '.join(clean_dups)

from wordcloud import WordCloud
# word_cloud_dict = Counter(clean_dups)
wordcloud = WordCloud(width=500, height=300, background_color="white", max_words=100).generate(wordcloudlist)
plt.figure( figsize=(20,10) )
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()





# Οργανισμός ΠΔ

orgdata = pd.read_json("kodiko_href.json", orient='index').reset_index()
orgdata.columns = ["identity", "url", "title"]

mask = orgdata["title"].str.contains("Οργανισμός", case=False, na=False)
orgdata = orgdata[mask]
orgs = orgdata["identity"].tolist()
orgs = [x.split(" (")[0] for x in orgs]

finaldata = data[data["identity"].isin(orgs)]

fcounts = finaldata["key_split"].value_counts()
fnumber_of_articles = sum([1 if x and y else 0 for x, y in zip(finaldata["title"], finaldata["content"])])
fpds = finaldata.groupby("identity").size()


fpds.min()
fpds.max()
fpds.std()
round(fpds.mean(), 2)
fpds.median()









