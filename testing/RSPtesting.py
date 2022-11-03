import pandas as pd
from rbner.rbNER import rbNER
from collections import OrderedDict

path = "testing/RSP_testdata.xlsx"
groundtruth = pd.read_excel(path)
rbner = rbNER()

data = groundtruth.groupby(by=["Ministry","Article"])
respass = data.sum("NoRespa")
texts = data.Text.apply(list)
paths = data.Path.apply(list)
ar_keys = data.Article.apply(list)

combined = respass.assign(Text=texts).assign(Path=paths).assign(Article=ar_keys)
combined["Article"] = [x[0] for x in combined["Article"]]
combined["Path"] = [x[0] for x in combined["Path"]]
combined["Text"] = [x[0] for x in combined["Text"]]


def main(text, textpath, ar_key):

    result = OrderedDict()
    from src.fek_parser import FekParser
    from rbner.respas import respas
    FPRS, RSP = FekParser(textpath), respas(textpath)
    
    article_paragraphs = FPRS.find_article_paragraphs(text)
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


combined["results"] = [main(row["Text"], row["Path"], row["Article"]) for idx, row in combined.iterrows()]
combined.drop("Text", inplace=True, axis=1)
combined.drop("Path", inplace=True, axis=1)

results_df = combined[["Article", "results"]].to_dict()["results"]


