#%% libraries and initialization of objects (common for both tasks)
import time
start_time = time.time()

from rbner.rbNER import rbNER
rbner = rbNER()

from rbner.respas import respas
from src.fek_parser import PreParser, FekParser
from rbner.structure import structure
import re
from collections import OrderedDict

from src.rb_respas_tool import respas



"""give a filepath (in .pdf form)"""
filepath = "fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-ergasiaskaikoinwnikhsasfalishs-134-2017.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-ygeias-121-2017.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-psifiakhsdiakuvernhshs-40-2020.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-nautiliaskainhsiwtikhspolitikhs-13-2018.pdf"
#filepath = "fek-organismoi-upourgeiwn/yp-tourismou-127-2017.pdf"
#filepath = "fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-ypodomwnkaimetaforwn-123-2017.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-oikonomikwn-142-2017.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-periballontoskaienergeias-132-2017.pdf"

"""initialize PreParser that produces a .txt file on working directory"""
text = PreParser().pdf2text(filepath)

"""change the filename extenstion to .txt"""
textpath = re.sub(r".pdf$", ".txt", filepath)


FPRS, RSP = FekParser(textpath), respas(textpath)
FPRS, STR = FekParser(textpath), structure(textpath)
"""initialize the objects for relation and responsibilities extraction"""
FPRS, STR, RSP = FekParser(textpath), structure(textpath), respas(textpath)
FPRS = FekParser(textpath)

"""get articles on the given text"""
articles = FPRS.articles
article40 = articles["Άρθρο 40"]
paragraphs = FPRS.find_article_paragraphs(article40)
#article2 = articles["Άρθρο 2"]
#article_paragraphs = FPRS.find_article_paragraphs(article2)
keys = ["Άρθρο 2", "Άρθρο 3"]
filteredarticles = {key: articles[key] for key in keys if key in articles}
#filteredarticles = {key: articles.get(key) for key in keys}
relations = STR.main(filteredarticles)
relations = STR.main(articles)

responsibilities = RSP.main(articles)



"""tests"""
article = articles["Άρθρο 2"]

gi, depth = FPRS.find_levels_depth(paragraph)

article_paragraphs = FPRS.find_article_paragraphs(article)
paragraph = article_paragraphs["2"]
new_par = STR.remove_number_level(paragraph)
grouped_info, depth = STR.find_levels_depth(new_par)
relations = STR.main(filteredarticles)

#%%

# final_list = [x for x in relations if x]
import pandas as pd
import pydot
from networkx.drawing.nx_pydot import to_pydot
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

unit = [x[2] for x in relations]
subunit = [x[3].replace("\n", "") for x in relations]
data = {"subject":unit,
        "object":subunit}
kg_df = pd.DataFrame(data=data)

G=nx.from_pandas_edgelist(kg_df, "subject", "object", 
                          edge_attr=True, create_using=nx.MultiDiGraph())
plt.figure(figsize=(300,100))

pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
nx.draw_networkx(G, with_labels=False, node_shape= "s", node_size=40000, node_color='none', linewidths=150, width=3, arrows=True, pos = pos)

nodenames = {}

for n in G.nodes():
  splittext = n.split(" ")
  for x in range(2, len(splittext), 5):
      splittext[x] = "\n"+splittext[x].lstrip()
  text = " ".join(splittext)
  
  nodenames[n] = text

nx.draw_networkx_labels(G, pos=pos, labels=nodenames, bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.5'), font_size=12)

plt.show()










