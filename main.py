import os
import re
import argparse
from src.fek_parser import PreParser, FekParser


def mainRE(textpath):
    from rbner.structure import structure
    FPRS, STR = FekParser(textpath), structure(textpath)
    articles = FPRS.articles
    
    # keys = ["Άρθρο 2", "Άρθρο 3"] # here read the possible articles that user wants to extract
    # filteredarticles = {key: articles[key] for key in keys if key in articles}
    # relations = STR.main(filteredarticles)
    relations = STR.main(articles)
    return relations

def mainRSP(textpath):
    from rbner.respas import respas
    FPRS, RSP = FekParser(textpath), respas(textpath)
    articles = FPRS.articles
    
    # keys = ["Άρθρο 2", "Άρθρο 3"] # here read the possible articles that user wants to extract
    # filteredarticles = {key: articles[key] for key in keys if key in articles}
    # responsibilities = RSP.main(filteredarticles)
    responsibilities = RSP.main(articles)
    return responsibilities
    

def main():
    parser = argparse.ArgumentParser(description="Retrieve Information from pdf file")
    parser.add_argument("--filepath", type=str, required=True)
    parser.add_argument("--task", choices=["RE", "RSP"], help="The task of interest to be applied")
    #TODO consider the following in we desire to add option of specific articles
    # parser.add_argument("--articles", nargs="+", type=int, help="A list of integers if you need specific articles only to be processed")
    args = parser.parse_args()
    
    filepath, task = args.filepath, args.task
    
    pathExists = os.path.exists(filepath)
    if pathExists:
        text = PreParser().pdf2text(filepath)
        #print(".txt file generated")
        #TODO add os-check that file has successfully generated
        textpath = re.sub(r".pdf$", ".txt", filepath)

        if task == "RE":
            results = mainRE(textpath)
        else:
            results = mainRSP(textpath)
    else:
        print("Invalid filepath")
    #TODO call a future module to create the required output form - graph/rdf/text etc

    print(results, "\n")
    print(f"{len(results)} results found")
    return

if __name__ == '__main__':
    
    main()
    