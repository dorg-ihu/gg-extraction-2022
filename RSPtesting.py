import pandas as pd
from src.fek_parser import PreParser, FekParser
from src.respa_extractor import RespExtractor
from rbner.rbNER import rbNER
import re
import random
from rbner.structure import structure
from rbner.respas import respas
from collections import OrderedDict

path = "testing/RSP_testdata.xlsx"
groundtruth = pd.read_excel(path)
rbner = rbNER()

data = groundtruth.groupby(by=["Ministry","Article"])
respas = data.sum("NoRespa")
texts = data.Text.apply(list)
paths = data.Path.apply(list)
ar_keys = data.Article.apply(list)

combined = respas.assign(Text=texts).assign(Path=paths).assign(Article=ar_keys)
combined["Article"] = [x[0] for x in combined["Article"]]
combined["Path"] = [x[0] for x in combined["Path"]]
combined["Text"] = [x[0] for x in combined["Text"]]


def main(text, textpath, ar_key):

    result = OrderedDict()
    from src.fek_parser import PreParser, FekParser
    from rbner.respas import respas
    FPRS, RSP = FekParser(textpath), respas(textpath)
    
    article_paragraphs = FPRS.find_article_paragraphs(text)
    if len(article_paragraphs) > 1:
        possible_title = article_paragraphs["0"]
        if any(title_kw in possible_title for title_kw in RSP.irrelevant_title):
            print("Article {} has been skipped due to irrelevant_title".format(ar_key))
            return result
        else:
            master_unit, responsibility_paragraphs = RSP.get_candidate_paragraphs_per_article(article_paragraphs) #input article text - output list of candidate paragraphs
            responsibilities = RSP.get_respas(master_unit, responsibility_paragraphs) # input list of candidate paragraphs - ouput dictionary with unit-respa pairs
            if responsibilities:
                print("We found {} pairs of responsibilities on Article {} has been processed".format(len(responsibilities), ar_key))
                return responsibilities
    else:
        pass
    return result
    
# def analyze_dict_numbers(resultsdict):
#     NoRespas = 0
#     for k, v in resultsdict.items():
#         print(type(v))
#         print(len(v))
#         NoRespas += len(v)
#     return NoRespas
 

# combined_dummy = [()]
combined["results"] = [main(row["Text"], row["Path"], row["Article"]) for idx, row in combined.iterrows()]
combined.drop("Text", inplace=True, axis=1)
combined.drop("Path", inplace=True, axis=1)

results_df = combined[["Article", "results"]].to_dict()["results"]



# combined["results_number"] = [analyze_dict(x) for x in combined["results"]]
# combined["results_units_length"] = [len(x) for x in combined["results"]]
# combined["results_units"] = [list(x.keys()) for x in combined["results"]]
# combined["results_respas"] = [x.values() for x in combined["results"]]

# # testresults = pd.json_normalize(combined["results"])
# test_results = dict(zip(combined["Article"], combined["results"]))

# test_results = dict(zip(combined.Article, combined.results))


# combined["results_unit"] = [x for x in combined["results"].tolist()]
# combined["results_respa"] = [x[1] for x in combined["results"].items()]

# combined["number_of_results"] = []


# FPRS, RSP = FekParser(textpath), respas(textpath)





























data = groundtruth.groupby(by=["Ministry","Article"])
respas = data.sum("NoRespa")
text = data.Text.apply(list)

data = groundtruth.groupby(by=["Ministry","Article"]).sum("NoRespa")
text = data.Text.apply(list)
print(data.Text)
articles = data["Text"]


for group in data.groups:
    current_group = data.get_group(group)
    print(current_group.head(2))








gby_ministry = groundtruth.groupby(by="Ministry")
gby_ministry.ngroups
gby_ministry.groups

for group in gby_ministry.groups:
    current_group = gby_ministry.get_group(group)
    gby_article = current_group.groupby(by="Article")
    for gr in gby_article:
        article = gr
    print(current_group.head(2))

articles = 

responsibilities_dict = OrderedDict()
for AR_key, AR_value in articles.items():
    try:
        article_paragraphs = FPRS.find_article_paragraphs(AR_value)
        if len(article_paragraphs) > 1:
            possible_title = article_paragraphs["0"]
            if any(title_kw in possible_title for title_kw in RSP.irrelevant_title):
                print("Article {} has been skipped due to irrelevant_title".format(AR_key))
                continue
            else:
                master_unit, responsibility_paragraphs = RSP.get_candidate_paragraphs_per_article(article_paragraphs) #input article text - output list of candidate paragraphs
                print(master_unit)
                responsibilities = RSP.get_respas(master_unit, responsibility_paragraphs) # input list of candidate paragraphs - ouput dictionary with unit-respa pairs
                if responsibilities:
                    responsibilities_dict[AR_key] = responsibilities
                    print("We found {} pairs of responsibilities on Article {} has been processed".format(len(responsibilities), AR_key))
        else:
            continue
    except Exception as e:
        print("Article {} resulted in error".format(AR_key))
        pass