from src.fek_parser import PreParser, FekParser
import argparse
import os
import re


def mainRE(textpath, method):
    FPRS = FekParser(textpath)
    articles = FPRS.articles
    
    #keys = ["Άρθρο 19"] # here read the possible articles that user wants to extract
    #filteredarticles = {key: articles[key] for key in keys if key in articles}
    # relations = STR.main(filteredarticles)
    
    if method == "RB":
        from src.rb_structure_tool import rb_structure
        STR = rb_structure(textpath)
    else:
        from src.ml_structure_tool import ml_structure
        STR = ml_structure(textpath)
        
    return STR.main(articles)

def mainRSP(textpath, method):
    FPRS = FekParser(textpath)
    articles = FPRS.articles
    
    # keys = ["Άρθρο 2", "Άρθρο 3"] # here read the possible articles that user wants to extract
    # filteredarticles = {key: articles[key] for key in keys if key in articles}
    # responsibilities = RSP.main(filteredarticles)
    
    if method == "RB":
        from src.rb_respas_tool import rb_respas
        RSP = rb_respas(textpath)
    else:
        from src.ml_respas_tool import ml_respas
        RSP = ml_respas(textpath)

    return RSP.main(articles)
    

def main():
    parser = argparse.ArgumentParser(description="Retrieve Information from pdf file")
    parser.add_argument("--filepath", type=str, required=True)
    parser.add_argument("--task", choices=["RE", "RSP"], help="The task of interest to be applied")
    parser.add_argument("--method", choices=["RB", "ML"], help="The method to perform the task RuleBased or MachineLearning")
    #TODO consider the following in we desire to add option of specific articles
    # parser.add_argument("--articles", nargs="+", type=int, help="A list of integers if you need specific articles only to be processed")
    args = parser.parse_args()
    
    filepath, task, method = args.filepath, args.task, args.method
    
    pathExists = os.path.exists(filepath)
    if pathExists:
        text = PreParser().pdf2text(filepath)

        #TODO add os-check that file has successfully generated
        textpath = re.sub(r".pdf$", ".txt", filepath)

        if task == "RE":
            results = mainRE(textpath, method)
        else:
            results = mainRSP(textpath, method)
    else:
        print("Invalid filepath")

    print(results, "\n")
    print(f"{len(results)} results found")
    return

if __name__ == '__main__':
    
    main()
    
    
    
