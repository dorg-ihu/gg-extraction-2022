import os
import re
import argparse
from collections import OrderedDict
from src.fek_parser import PreParser, FekParser


def mainRE(textpath):
    
    from rbner.structure import structure
    FPRS, STR = FekParser(textpath), structure(textpath)
    articles = FPRS.articles
    
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
            print("Article {} resulted in error {}".format(AR_key, e))
            pass
    return relations_list

def mainRSP(textpath):
    from rbner.respas import respas
    FPRS, RSP = FekParser(textpath), respas(textpath)
    articles = FPRS.articles
    
    responsibilities_dict = OrderedDict()
    for AR_key, AR_value in articles.items():
        try:
            article_paragraphs = FPRS.find_article_paragraphs(AR_value)
            if len(article_paragraphs) > 1:
                possible_title = article_paragraphs["0"]
                if any(title_kw in possible_title for title_kw in RSP.irrelevant_title):
                    print("Article {} has been skipped due to irrelevant_title".format(AR_key))
                    continue

            master_unit, responsibility_paragraphs = RSP.get_candidate_paragraphs_per_article(article_paragraphs)
            responsibilities = RSP.get_respas(master_unit, responsibility_paragraphs)
            if responsibilities:
                responsibilities_dict[AR_key] = responsibilities
                print("We found {} pairs of responsibilities on Article {} has been processed".format(len(responsibilities), AR_key))
            
        except Exception as e:
            print("Article {} resulted in error {}".format(AR_key, e))
            pass
    
    return responsibilities_dict
    

def main():
    parser = argparse.ArgumentParser(description="Retrieve Information from pdf file")
    parser.add_argument("--filepath", type=str, required=True)
    parser.add_argument("--task", choices=["RE", "RSP"], help="The task of interest to be applied")
    args = parser.parse_args()
    
    filepath, task = args.filepath, args.task
    
    pathExists = os.path.exists(filepath)
    if pathExists:
        text = PreParser().pdf2text(filepath)
        #print(".txt file generated")
        textpath = re.sub(r".pdf$", ".txt", filepath)

        if task == "RE":
            results = mainRE(textpath)
        else:
            results = mainRSP(textpath)
    else:
        print("Invalid filepath")
    print(results)
    return

if __name__ == '__main__':
    
    main()
    