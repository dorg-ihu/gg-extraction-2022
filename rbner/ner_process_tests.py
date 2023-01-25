fpath = "fek-organismoi-upourgeiwn/yp-psifiakhsdiakuvernhshs-40-2020.pdf"
from src.fek_parser import PreParser, FekParser
import re
text = PreParser().pdf2text(fpath)
textpath = re.sub(r".pdf$", ".txt", fpath)
from src.mlrsp import farm
RSP, FPRS = farm(textpath), FekParser(textpath)
articles = FPRS.articles
article = articles["Άρθρο 26"]
paragraphs = FPRS.find_article_paragraphs(article)
mu, rsp_p = RSP.get_candidate_paragraphs_per_article(paragraphs)
respas = RSP.get_respas(mu, rsp_p)

text = "β. \nτον έλεγχο τήρησης των περί ανάληψης υποχρεώσεων \nδιατάξεων και την παροχή βεβαίωσης"
par_dict = FPRS.find_article_paragraphs(" " + text, "paragraph")
par_dict = FPRS.process_last_split(par_dict)

filepaths = ["fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf",
             "fek-organismoi-upourgeiwn/yp-ergasiaskaikoinwnikhsasfalishs-134-2017.pdf",
             "fek-organismoi-upourgeiwn/yp-ygeias-121-2017.pdf",
             "fek-organismoi-upourgeiwn/yp-psifiakhsdiakuvernhshs-40-2020.pdf",
             "fek-organismoi-upourgeiwn/yp-nautiliaskainhsiwtikhspolitikhs-13-2018.pdf",
             "fek-organismoi-upourgeiwn/yp-ypodomwnkaimetaforwn-123-2017.pdf",
             "fek-organismoi-upourgeiwn/yp-oikonomikwn-142-2017.pdf",
             "fek-organismoi-upourgeiwn/yp-periballontoskaienergeias-132-2017.pdf",
             "fek-organismoi-upourgeiwn/yp-tourismou-127-2017.pdf",
             "fek-organismoi-upourgeiwn/yp-prostasiastoupolith-62-2019.pdf",
             "fek-organismoi-upourgeiwn/yp-politismoukaiathlitismou-4-2018.pdf",
             "fek-organismoi-upourgeiwn/yp-paideiaskaithriskeumatwn-18-2018.pdf",
             "fek-organismoi-upourgeiwn/yp-eswterikwn-141-2017.pdf",
             "fek-organismoi-upourgeiwn/yp-ekswterikwnapodimouellhnismou-4781-2022.pdf",
             "fek-organismoi-upourgeiwn/yp-dikaiosunhs-6-2021.pdf",
             "fek-organismoi-upourgeiwn/yp-anaptiksiskaiependusewn-5-2022.pdf",
             "fek-organismoi-upourgeiwn/yp-agrotikhsanaptukshskaitrofimwn-97-2017.pdf"
             ]


filepaths = ["fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"]


filepaths = ["fek-organismoi-upourgeiwn/yp-psifiakhsdiakuvernhshs-40-2020.pdf"]


for fpath in filepaths:
    from src.fek_parser import PreParser, FekParser
    import re
    text = PreParser().pdf2text(fpath)
    textpath = re.sub(r".pdf$", ".txt", fpath)
    from src.mlrsp import farm
    RSP, FPRS = farm(textpath), FekParser(textpath)
    articles = FPRS.articles
    
    keys = ["Άρθρο 26"]
    filteredarticles = {key: articles[key] for key in keys if key in articles}
    
    respas = RSP.main(filteredarticles)
    print(f"The {fpath} has been processed")

import pandas as pd
results = []
for key, value in respas.items():
    for k, v in value.items():
        results.append((key, k, v))

pdresults = pd.DataFrame(results, columns=["Article", "Unit", "Respas"])
pdresults.to_csv("mlrsp_results_psifiakisdiakuvernhshs.csv", encoding="utf-8")


for fpath in filepaths:
    from src.fek_parser import PreParser, FekParser
    import re
    text = PreParser().pdf2text(fpath)
    textpath = re.sub(r".pdf$", ".txt", fpath)
    from src.rb_respas_tool import respas
    FPRS, RSP = FekParser(textpath), respas(textpath)
    articles = FPRS.articles
    
    
    relations = RSP.main(articles)
    






results = pd.DataFrame(respas)
results = pd.DataFrame.from_dict(respas, orient='index').reset_index()


for fpath in filepaths:
    from src.fek_parser import PreParser, FekParser
    import re
    text = PreParser().pdf2text(fpath)
    textpath = re.sub(r".pdf$", ".txt", fpath)
    from ML.mlre import stuctureML as sml
    STR, FPRS = sml(textpath), FekParser(textpath)
    articles = FPRS.articles
    relations = STR.main(articles)
    print(f"The {fpath} has been processed")
    
    
for fpath in filepaths:
    from src.fek_parser import PreParser, FekParser
    import re
    text = PreParser().pdf2text(fpath)
    textpath = re.sub(r".pdf$", ".txt", fpath)
    from rbner.structure import structure
    FPRS, STR = FekParser(textpath), structure(textpath)
    articles = FPRS.articles
    relations = STR.main(articles)
    
    
    
#ML testing
from src.fek_parser import PreParser, FekParser
import re
filepath = "fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"
text = PreParser().pdf2text(filepath)
textpath = re.sub(r".pdf$", ".txt", filepath)
from ML.mlre import stuctureML as sml
STR, FPRS = sml(textpath), FekParser(textpath)
articles = FPRS.articles
relations = STR.main(articles)





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










