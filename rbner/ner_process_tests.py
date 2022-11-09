#%%
from src import dictionaries as dc

def remove_first_level(txt):
    first_line, rest_lines = txt.split("\n", 1)[0], "\n" + txt.split("\n", 1)[1]
    first_line = re.sub(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", first_line)
    return "\n" + first_line + rest_lines

#TODO check if it is working as expected and add on tool
def remove_number_level(txt):
    first_line, rest_lines = txt.split("\n", 1)[0], "\n" + txt.split("\n", 1)[1]
    first_line = re.sub(r"^[ ]*[0-9]+[\.\)] ", "", first_line)
    return "\n" + first_line + rest_lines

def get_paragraph_levels(items):
    levels = []
    for i, item in enumerate(items):
        if item in dc.alphabet:
            levels.append((item, "alphabet"))  # alphabet
        elif item in dc.ab_double_combs:
            levels.append((item, "abcombinations"))  # ab combinations
        elif item in dc.latin_numbers:
            levels.append((item, "latinnumbers"))  # latin numbers
        elif item in dc.numbers:
            levels.append((item, "therest"))  #
    return levels


def find_levels_depth(txt):
    split_all = FPRS.split_all_int(txt)
    split_all = [x for x in split_all if isinstance(x, tuple)]

    pointers_list = [x[0] for x in split_all]
    
    levels = get_paragraph_levels(pointers_list)
    depth = 1
    type_of_levels = {levels[0][1]: depth}
    info = [levels[0] + (depth,) + (split_all[0][1],)]
    for idx, (key, tag) in enumerate(levels[1:]):
        if tag not in type_of_levels:
            depth += 1
            type_of_levels[tag] = depth
            info.append((key, tag) + (depth,) + (split_all[idx+1][1],))
        else:
            cur_depth = type_of_levels[tag]
            info.append((key, tag) + (cur_depth,) + (split_all[idx+1][1],))
    
    # reconstructs the flat list of points into groups under the depth = 1
    split_points = [i for i, (point, typ, dep, text) in enumerate(info) if dep == 1]
    total_split = split_points + [len(info)]
    grouped_info = [info[i:j] for i, j in zip(split_points, total_split[1:])]

    return grouped_info, len(type_of_levels)


#%% libraries and initialization of objects (common for both tasks)

import time
start_time = time.time()

#from src.respa_extractor import RespExtractor
from rbner.rbNER import rbNER
rbner = rbNER()
#import random

from rbner.respas import respas
from src.fek_parser import PreParser, FekParser
from rbner.structure import structure
import re
from collections import OrderedDict

from src.rb_respas_tool import respas



"""give a filepath (in .pdf form)"""
filepath = "fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-ergasiaskaikoinwnikhsasfalishs-134-2017.pdf"
# filepath = "fek-organismoi-upourgeiwn/yp-ygeias-121-2017.pdf"

#filepath = "fek-organismoi-upourgeiwn/yp-tourismou-127-2017.pdf"
#filepath = "fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"
#filepath = "fek-organismoi-upourgeiwn/yp-ypodomwnkaimetaforwn-123-2017.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-oikonomikwn-142-2017.pdf"

"""initialize PreParser that produces a .txt file on working directory"""
text = PreParser().pdf2text(filepath)

"""change the filename extenstion to .txt"""
textpath = re.sub(r".pdf$", ".txt", filepath)


FPRS, RSP = FekParser(textpath), respas(textpath)
FPRS, STR = FekParser(textpath), structure(textpath)
"""initialize the objects for relation and responsibilities extraction"""
FPRS, STR, RSP = FekParser(textpath), structure(textpath), respas(textpath)


"""get articles on the given text"""
articles = FPRS.articles

#%% relations extraction
relations_list = []
for AR_key, AR_value in articles.items():
    try:
        article_paragraphs = FPRS.find_article_paragraphs(AR_value)
        if len(article_paragraphs) > 1:
            possible_title = article_paragraphs["0"]
            if any(title_kw in possible_title for title_kw in STR.irrelevant_title):
                print("Article {} has been skipped due to irrelevant_title".format(AR_key))
                continue
        
        master_unit, relation_paragraphs = STR.get_candidate_paragraphs_per_article(article_paragraphs) # returns which paragraphs meet the STRUCTURE requirements
        relations = STR.get_relations(master_unit, relation_paragraphs)
        relations_list.append(relations)
        print("Article {} has been processed".format(AR_key))
    except Exception as e:
        print("Article {} resulted in error".format(AR_key))
        pass

final_list = [x for x in relations_list if x]




import pydot
from networkx.drawing.nx_pydot import to_pydot
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

interim_relations = [t for sublist in final_list for l in sublist for t in l]
final_relations = []
for i in range(0, len(interim_relations), 2):
    final_relations.append((interim_relations[i], interim_relations[i+1]))


the_subject = [x[0] for x in final_relations]
the_object = [x[1] for x in final_relations]

df = pd.DataFrame({"subject": the_subject,
                   "object": the_object})

G=nx.from_pandas_edgelist(df, "subject", "object", 
                  edge_attr=None, create_using=nx.MultiDiGraph())
plt.figure(figsize=(30,10))
pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='red', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()




fl = [t for sublist in final_list for l in sublist for t in l]
tfl = []
for i in range(0, len(fl), 2):
    tfl.append((fl[i], fl[i+1]))


tfl = list(zip(fl, fl[1:]))
"""create a graph given the resulted tuples"""
processed_relations = []
for lst in final_list:
    tuplist = []
    for (x,y) in lst:
        newvalue = rbner.remove_intonations(y).replace("\n", "").strip()
        tuplist.append((x, newvalue))
    processed_relations.append(tuplist)

# for lst in processed_relations:
#     for tup in lst:
#         print(tup)
# processed_relations = [rbner.remove_intonations(t2) for x in final_list for (t1, t2) in x]

graph = STR.get_relations_graph(final_list)
# processed_relations.insert(0, [("ΓΕΝΙΚΗ ΔΙΕΥΘΥΝΣΗ ΤΕΣΤΑΡΙΣΜΑΤΟΣ", "ΔΙΕΥΘΥΝΣΗ ΕΥΡΩΠΑΪΚΗΣ ΚΑΙ ΔΙΕΘΝΟΥΣ ΣΥΝΕΡΓΑΣΙΑΣ"), ("ΓΕΝΙΚΗ ΔΙΕΥΘΥΝΣΗ ΤΕΣΤΑΡΙΣΜΑΤΟΣ", "ΔΙΕΥΘΥΝΣΗ ΥΠΟΔΟΜΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΕΠΙΚΟΙΝΩΝΙΩΝ")])

print("Execution time {}".format(time.time() - start_time))

#%% responsibilities extraction
responsibilities_dict = OrderedDict()
for AR_key, AR_value in articles.items():
    try:
        article_paragraphs = FPRS.find_article_paragraphs(AR_value)
        if len(article_paragraphs) > 1:
            possible_title = article_paragraphs["0"]
            if any(title_kw in possible_title for title_kw in RSP.irrelevant_title):
                print("Article {} has been skipped due to irrelevant_title".format(AR_key))
                continue

        master_unit, responsibility_paragraphs = RSP.get_candidate_paragraphs_per_article(article_paragraphs) #input article text - output list of candidate paragraphs

        responsibilities = RSP.get_respas(master_unit, responsibility_paragraphs) # input list of candidate paragraphs - ouput dictionary with unit-respa pairs
        if responsibilities:
            responsibilities_dict[AR_key] = responsibilities
            print("We found {} pairs of responsibilities on Article {} has been processed".format(len(responsibilities), AR_key))
        
    except Exception as e:
        print("Article {} resulted in error".format(AR_key))
        pass

# final_list = [x for x in responsibilities_list if x]

#%%

article17 = articles["Άρθρο 17"]
paragraphs = FPRS.find_article_paragraphs(article17)
paragraphs_list = list(paragraphs.values())
# paragraph3 = paragraphs["3"]
paragraphs_list = [paragraphs_list.pop(-2)]

respas = RSP.get_respas(paragraphs_list)


new_par3 = remove_first_level(paragraph3)

respas = RSP.get_respas(new_par3)

results = find_levels_depth(new_par3)

if len(paragraphs) > 1:
    potential_title = paragraphs["0"]
print(potential_title)
#%%



filepath = "fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-ergasiaskaikoinwnikhsasfalishs-134-2017.pdf"
# filepath = "fek-organismoi-upourgeiwn/yp-ygeias-121-2017.pdf"

#filepath = "fek-organismoi-upourgeiwn/yp-tourismou-127-2017.pdf"
#filepath = "fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"
#filepath = "fek-organismoi-upourgeiwn/yp-ypodomwnkaimetaforwn-123-2017.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-oikonomikwn-142-2017.pdf"

"""initialize PreParser that produces a .txt file on working directory"""
text = PreParser().pdf2text(filepath)








