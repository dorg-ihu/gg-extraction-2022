from src.fek_parser import PreParser, FekParser
from rbner.structure import structure
import pandas as pd
import re
from fuzzywuzzy import fuzz

path = "testing/RE_testdata.xlsx"
groundtruth = pd.read_excel(path)

data = groundtruth.groupby(by=["Ministry","Article"])

paths = data.Path.apply(list)
ar_keys = data.Article.apply(list)
units = data.Unit.apply(list)
subunits = data.Subunit.apply(list)

combined = pd.concat([paths, ar_keys, units, subunits], axis=1)
combined["Article"] = [x[0] for x in combined["Article"]]
combined["Path"] = [x[0] for x in combined["Path"]]
combined["Unit"] = [x[0] for x in combined["Unit"]]
combined["NoSubunits"] = [len(x) for x in combined["Subunit"]]


def main(path, ar_key):

    text = PreParser().pdf2text(path)
    textpath = re.sub(r".pdf$", ".txt", path)
    
    FPRS, STR = FekParser(textpath), structure(textpath)
    articles = FPRS.articles
    
    article = articles[ar_key]
    article_paragraphs = FPRS.find_article_paragraphs(article)
    if len(article_paragraphs) > 1:
        possible_title = article_paragraphs["0"]
        if any(title_kw in possible_title for title_kw in STR.irrelevant_title):
            print("Article {} has been skipped due to irrelevant_title".format(ar_key))
            return []
        
    master_unit, relation_paragraphs = STR.get_candidate_paragraphs_per_article(article_paragraphs) # returns which paragraphs meet the STRUCTURE requirements
    relations = STR.get_relations(master_unit, relation_paragraphs)
    print("Article {} has been processed".format(ar_key))
    return relations


def reform_results(list_of_tuples):
    reslist = []
    for ele in list_of_tuples:
        reslist.append(ele[1].replace("\n", ""))
    return reslist

def validate_results(unit, subunit, resunit, ressubunit):
    found = True
    if fuzz.ratio(unit, resunit) > 0.8 and len(subunit) == len(ressubunit):
        ziplist = list(zip(subunit, ressubunit))
        for ele in ziplist:
            if fuzz.ratio(ele[0], ele[1]) < 0.8:
                found = False
                break
    else:
         found = False
    return found

combined["results"] = [main(row["Path"], row["Article"]) for idx, row in combined.iterrows()]
combined.drop("Path", inplace=True, axis=1)

results_df = combined[["Article", "results"]].to_dict()["results"] # to manually inspect

combined["results_number"] = [len(x) for x in combined["results"]]
new_combined = combined.copy(deep=True)
new_combined["ResultUnit"] = [x[0][0] if x else "" for x in new_combined["results"]]
new_combined["ResultSubunit"] = [reform_results(x) if x else "" for x in new_combined["results"]]
new_combined["validation"] = [validate_results(row["Unit"], row["Subunit"], row["ResultUnit"], row["ResultSubunit"]) for idx, row in new_combined.iterrows()]
print(f"The tool has correclty identified the relations for {new_combined['validation'].sum()} articles, out of total {len(new_combined)}")






