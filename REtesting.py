from rbner.rbNER import rbNER
from collections import OrderedDict
import pandas as pd


path = "testing/RE_testdata.xlsx"
groundtruth = pd.read_excel(path)
rbner = rbNER()


data = groundtruth.groupby(by=["Ministry","Article"])

texts = data.Text.apply(list)
paths = data.Path.apply(list)
ar_keys = data.Article.apply(list)

combined = pd.concat([texts, paths, ar_keys], axis=1)
combined["Article"] = [x[0] for x in combined["Article"]]
combined["Path"] = [x[0] for x in combined["Path"]]
combined["Text"] = [x[0] for x in combined["Text"]]


def main(text, textpath, ar_key):

    relations_list = []
    from src.fek_parser import FekParser
    from rbner.structure import structure
    FPRS, STR = FekParser(textpath), structure(textpath)

    article_paragraphs = FPRS.find_article_paragraphs(text)
    if len(article_paragraphs) > 1:
        possible_title = article_paragraphs["0"]
        if any(title_kw in possible_title for title_kw in STR.irrelevant_title):
            print("Article {} has been skipped due to irrelevant_title".format(ar_key))
            return relations_list
        
    master_unit, relation_paragraphs = STR.get_candidate_paragraphs_per_article(article_paragraphs) # returns which paragraphs meet the STRUCTURE requirements
    relations = STR.get_relations(master_unit, relation_paragraphs)
    relations_list.append(relations)
    print("Article {} has been processed".format(ar_key))

    return relations_list


combined["results"] = [main(row["Text"], row["Path"], row["Article"]) for idx, row in combined.iterrows()]
combined.drop("Text", inplace=True, axis=1)
combined.drop("Path", inplace=True, axis=1)



# results_df = combined[["Article", "results"]].to_dict()["results"]
results_df = combined[["Article", "results"]].to_dict()["results"]



