from src.fek_parser import PreParser, FekParser
from rbner.structure import structure
import pandas as pd
import re
from fuzzywuzzy import fuzz

path = "testing/RE_testdata_v2.xlsx"
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


def clear_tuple_info(list_of_tuples):
    reslist = []
    for ele in list_of_tuples:
        reslist.append((ele[2]))
    return reslist


def clear_problematic(list_of_strings):
    reslist = []
    for ele in list_of_strings:
        reslist.append(ele.replace("\xa0", " "))
    return reslist


def main(path, ar_key):

    text = PreParser().pdf2text(path)
    textpath = re.sub(r".pdf$", ".txt", path)
    
    FPRS, STR = FekParser(textpath), structure(textpath)
    articles = FPRS.articles
    
    content = articles[ar_key]
    # article = {ar_key:content}
    
    
    article_paragraphs = FPRS.find_article_paragraphs(content)
    master_unit, candidate_paragraphs = STR.get_candidate_paragraphs_per_article(ar_key, article_paragraphs)
    
    return candidate_paragraphs

def words_count(st):
    return len(st.split(" "))

combined["paragraphs"] = [main(row["Path"], row["Article"]) for idx, row in combined.iterrows()]
combined["final_paragraphs"] = [clear_tuple_info(x) if x else "" for x in combined["paragraphs"]]
combined["paragraph"] = [clear_problematic(x) if x else "" for x in combined["final_paragraphs"]]
combined["paragraph"] = [x[0] if x else "" for x in combined["paragraph"]]
combined = combined.drop(combined[combined["paragraph"] == ""].index)
combined["words"] = [words_count(x) for x in combined["paragraph"]]

export_dataframe = combined[["Unit", "Subunit", "paragraph"]]

#export_dataframe.to_csv("paragraphs_re_v2.csv", index=False)




#v3
# import time
export_dataframe["Unit"][2] = "Διεύθυνση"
export_dataframe["Unit"][4] = "Δ.Α." 
export_dataframe["Unit"][2] = "Διεύθυνση (Α1)"
export_dataframe.to_csv("paragraphs_re_v3.csv", index=False)





























