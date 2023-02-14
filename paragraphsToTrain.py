import pandas as pd
from src.fek_parser import PreParser, FekParser
import re


"""give a filepath (in .pdf form)"""


filepaths = ["fek-organismoi-upourgeiwn/yp-tourismou-127-2017.pdf",
             "fek-organismoi-upourgeiwn/yp-dikaiosunhs-6-2021.pdf",
             "fek-organismoi-upourgeiwn/yp-psifiakhsdiakuvernhshs-40-2020.pdf", 
             "fek-organismoi-upourgeiwn/yp-paideiaskaithriskeumatwn-18-2018.pdf",
             "fek-organismoi-upourgeiwn/yp-periballontoskaienergeias-132-2017.pdf"]


articles_tofilter_per_file = [
        ["Άρθρο 6", "Άρθρο 7", "Άρθρο 8", "Άρθρο 9", "Άρθρο 10",
         "Άρθρο 11", "Άρθρο 15", "Άρθρο 16", "Άρθρο 17", "Άρθρο 18",
         "Άρθρο 19", "Άρθρο 20", "Άρθρο 21", "Άρθρο 22", "Άρθρο 23"],
        ["Άρθρο 3", "Άρθρο 4", "Άρθρο 5", "Άρθρο 6", "Άρθρο 7", "Άρθρο 8",
         "Άρθρο 9", "Άρθρο 10", "Άρθρο 11", "Άρθρο 13", "Άρθρο 14", "Άρθρο 15",
         "Άρθρο 16", "Άρθρο 19", "Άρθρο 20", "Άρθρο 21", "Άρθρο 23", "Άρθρο 24"],
        ["Άρθρο 3", "Άρθρο 4", "Άρθρο 5", "Άρθρο 6", "Άρθρο 7", "Άρθρο 8",
         "Άρθρο 10", "Άρθρο 11", "Άρθρο 12", "Άρθρο 13", "Άρθρο 14", "Άρθρο 16",
         "Άρθρο 18", "Άρθρο 19", "Άρθρο 20", "Άρθρο 22", "Άρθρο 23", "Άρθρο 24",
         "Άρθρο 25", "Άρθρο 26", "Άρθρο 27", "Άρθρο 29", "Άρθρο 30", "Άρθρο 31",
         "Άρθρο 33", "Άρθρο 34", "Άρθρο 35", "Άρθρο 36", "Άρθρο 39", "Άρθρο 40",
         "Άρθρο 41", "Άρθρο 42", "Άρθρο 44", "Άρθρο 45", "Άρθρο 46", "Άρθρο 47", "Άρθρο 48"],
        ["Άρθρο 5","Άρθρο 7","Άρθρο 8","Άρθρο 9","Άρθρο 10","Άρθρο 11","Άρθρο 12","Άρθρο 13",
         "Άρθρο 14","Άρθρο 15","Άρθρο 17","Άρθρο 18","Άρθρο 19","Άρθρο 20","Άρθρο 21","Άρθρο 22",
         "Άρθρο 23","Άρθρο 25","Άρθρο 26","Άρθρο 27","Άρθρο 28","Άρθρο 31","Άρθρο 32","Άρθρο 33",
         "Άρθρο 34","Άρθρο 35","Άρθρο 36","Άρθρο 37","Άρθρο 39","Άρθρο 40","Άρθρο 41","Άρθρο 42",
         "Άρθρο 44","Άρθρο 45","Άρθρο 47","Άρθρο 48","Άρθρο 50","Άρθρο 51","Άρθρο 52","Άρθρο 53",
         "Άρθρο 54","Άρθρο 55","Άρθρο 58","Άρθρο 59","Άρθρο 61","Άρθρο 62","Άρθρο 63","Άρθρο 64",
         "Άρθρο 65","Άρθρο 67","Άρθρο 68","Άρθρο 69"],
        ["Άρθρο 6","Άρθρο 7","Άρθρο 10","Άρθρο 11","Άρθρο 12","Άρθρο 14","Άρθρο 15","Άρθρο 16",
         "Άρθρο 18","Άρθρο 19","Άρθρο 20","Άρθρο 23","Άρθρο 24","Άρθρο 25","Άρθρο 26","Άρθρο 28",
         "Άρθρο 29","Άρθρο 30","Άρθρο 31","Άρθρο 34","Άρθρο 35","Άρθρο 36","Άρθρο 38","Άρθρο 39",
         "Άρθρο 40","Άρθρο 41","Άρθρο 44","Άρθρο 45","Άρθρο 46","Άρθρο 47","Άρθρο 49","Άρθρο 50",
         "Άρθρο 51","Άρθρο 52","Άρθρο 54","Άρθρο 55","Άρθρο 58","Άρθρο 59"]
        ]




# for generating testing
filepaths = ["fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"]
articles_tofilter_per_file = [
    ["Άρθρο 6", "Άρθρο 7", "Άρθρο 8", "Άρθρο 9", "Άρθρο 11", "Άρθρο 12", "Άρθρο 13", "Άρθρο 14",
     "Άρθρο 16", "Άρθρο 17", "Άρθρο 18", "Άρθρο 19", "Άρθρο 22", "Άρθρο 23", "Άρθρο 24", "Άρθρο 26",
     "Άρθρο 27", "Άρθρο 31", "Άρθρο 32"]
    ]



interestedIn = dict(zip(filepaths, articles_tofilter_per_file))

# filteredarticles = {key: articles[key] for key in keys if key in articles}

"""initialize PreParser that produces a .txt file on working directory"""
texts = [PreParser().pdf2text(filepath) for filepath in interestedIn.keys()]

"""change the filename extenstion to .txt"""
textpaths = [re.sub(r".pdf$", ".txt", filepath) for filepath in interestedIn.keys()]

articles_per_file = [FekParser(textpath).articles for textpath in textpaths]


#filter

paragraphs = []
for idx, articles in enumerate(articles_per_file):
    articles_toconsider = articles_tofilter_per_file[idx]
    filteredarticles = {key: articles[key] for key in articles_toconsider if key in articles}
    FPRS = FekParser(textpaths[idx])
    for article in filteredarticles.values():
        article_paragraphs_dict = FPRS.find_article_paragraphs(article)
        for k, v in article_paragraphs_dict.items():
            if k == "0":
                article_paragraphs_dict[k] = "#####" + v
        article_paragraphs_list = list(article_paragraphs_dict.values())
        for par in article_paragraphs_list:
            paragraphs.append(par)
    
    print("##"*10)

data = pd.DataFrame({"paragraphs":paragraphs})
#data.to_csv("HaystackParagraphs_sig.csv", index=False, encoding="utf-8-sig")
# data.to_csv("HaystackParagraphs_MetkaiAsulou.csv", index=False, encoding="utf-8-sig")
# data.to_csv("HaystackParagraphs.csv", index=False, encoding="utf-8")
text = data["paragraphs"][24]

#%%
import pandas as pd
# thedata = pd.read_csv("haystack/HaystackParagraphs_sig_ek.csv", encoding="utf-8-sig")
thedata = pd.read_csv("haystack/HaystackParagraphs_MetkaiAsulou.csv", encoding="utf-8-sig")

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("alexaapo/greek_legal_bert_v2")
special_tokens_dict = {'additional_special_tokens': ['<ΤΠΤ>']}
tokenizer.add_special_tokens(special_tokens_dict)
#model.resize_token_embeddings(len(tokenizer))

def tokenize_texts(text):
    return tokenizer.tokenize(text)


def truncate_brutal(text, limit=512):
    N = 10
    tokenized_length = len(tokenizer.tokenize(text))
    if tokenized_length > limit:
        splitted_text = text.split()
        while tokenized_length > limit:
            splitted_text = splitted_text[:len(splitted_text) - N]
            new_text = " ".join(splitted_text)
            tokenized_length = len(tokenizer.tokenize(new_text))
        return new_text
    else:
        return text


def remove_number_sings(text):
    if text[:5] == "#####":
        return text[5:]
    else:
        return text

thedata["paragraphs"] = [remove_number_sings(x) for x in thedata["paragraphs"]]
thedata["paragraphs"] = ["<ΤΠΤ> " + x for x in thedata["paragraphs"]]
thedata["document_text"] = [truncate_brutal(x) for x in thedata["paragraphs"]]
thedata["len_tokenized_paragraphs"] = [len(tokenize_texts(x)) for x in thedata["document_text"]]

export_dataframe = thedata[["document_text"]]
export_dataframe.to_csv("haystack_tokenized_test_special_token.csv", encoding="utf-8-sig", index=False)










