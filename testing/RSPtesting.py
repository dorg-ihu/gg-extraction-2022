import pandas as pd
from collections import OrderedDict
import re
from src.fek_parser import PreParser, FekParser
from rbner.respas import respas
import numpy as np
from fuzzywuzzy import fuzz

path = "testing/RSP_testdata.xlsx"
groundtruth = pd.read_excel(path)

groundtruth["gtruth"] = list(zip(groundtruth.Unit, groundtruth.NoRespa))
groundtruth.drop("Unit", inplace=True, axis=1)
groundtruth.drop("NoRespa", inplace=True, axis=1)

data = groundtruth.groupby(by=["Ministry","Article"])

gtruth = data.gtruth.apply(list)
paths = data.Path.apply(list)
ar_keys = data.Article.apply(list)
combined = pd.concat([paths, ar_keys, gtruth], axis=1)

combined["Article"] = [x[0] for x in combined["Article"]]
combined["Path"] = [x[0] for x in combined["Path"]]


def main(path, ar_key):

    result = OrderedDict()
    
    text = PreParser().pdf2text(path)
    textpath = re.sub(r".pdf$", ".txt", path)
    
    FPRS, RSP = FekParser(textpath), respas(textpath)
    articles = FPRS.articles
    
    article = articles[ar_key]
    article_paragraphs = FPRS.find_article_paragraphs(article)
    if len(article_paragraphs) > 1:
        possible_title = article_paragraphs["0"]
        if any(title_kw in possible_title for title_kw in RSP.irrelevant_title):
            print("Article {} has been skipped due to irrelevant_title".format(ar_key))
            return result

    master_unit, responsibility_paragraphs = RSP.get_candidate_paragraphs_per_article(article_paragraphs) #input article text - output list of candidate paragraphs
    responsibilities = RSP.get_respas(master_unit, responsibility_paragraphs) # input list of candidate paragraphs - ouput dictionary with unit-respa pairs
    if responsibilities:
        print("We found {} pairs of responsibilities on Article {} of {}".format(len(responsibilities), ar_key, textpath.split("yp-")[1]))
        result = responsibilities
    return result


combined["results"] = [main(row["Path"], row["Article"]) for idx, row in combined.iterrows()]
combined.drop("Path", inplace=True, axis=1)

new_combined = combined.copy(deep=True)

def process_results(od):
    thelist = []
    for k, v in od.items():
        thelist.append((k, len(v)))
    return thelist

def validate_results(gtruth, results):
    found = True
    ziplist = list(zip(gtruth, results))
    for ele in ziplist:
        print(ele[0][0],"<===>", ele[1][0])
        if fuzz.ratio(ele[0][0], ele[1][0]) > 0.8 and ele[0][1]== ele[1][1]:
            pass
        else:
            found = False
            break    
    return found

new_combined["PredictedResults"] = [process_results(x) for x in new_combined["results"]]
new_combined["validation"] = [validate_results(row["gtruth"], row["PredictedResults"]) for idx, row in new_combined.iterrows()]
print(f"The tool has correclty identified the responsibilities for {new_combined['validation'].sum()} articles, out of total {len(new_combined)}")



