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


def main(path, ar_key):

    text = PreParser().pdf2text(path)
    textpath = re.sub(r".pdf$", ".txt", path)
    
    FPRS, STR = FekParser(textpath), structure(textpath)
    articles = FPRS.articles
    
    content = articles[ar_key]
    article = {ar_key:content}
    return STR.main(article)
    


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


def clear_tuple_info(list_of_tuples):
    reslist = []
    for ele in list_of_tuples:
        reslist.append((ele[2], ele[3]))
    return reslist


combined["results"] = [main(row["Path"], row["Article"]) for idx, row in combined.iterrows()]
combined["fresults"] = [clear_tuple_info(x) if x else "" for x in combined["results"]]
combined.drop("Path", inplace=True, axis=1)

results_df = combined[["Article", "fresults"]].to_dict()["fresults"] # to manually inspect

combined["results_number"] = [len(x) for x in combined["results"]]
new_combined = combined.copy(deep=True)
new_combined["ResultUnit"] = [x[0][0] if x else "" for x in new_combined["fresults"]]
new_combined["ResultSubunit"] = [reform_results(x) if x else "" for x in new_combined["fresults"]]
new_combined["validation"] = [validate_results(row["Unit"], row["Subunit"], row["ResultUnit"], row["ResultSubunit"]) for idx, row in new_combined.iterrows()]
print(f"The tool has correclty identified the relations for {new_combined['validation'].sum()} articles, out of total {len(new_combined)}")






