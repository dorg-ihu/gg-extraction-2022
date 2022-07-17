import fitz
import re
from gm3.gm3.pparser import IssueParser
from src import dictionaries as dc


class PreParser:
    """
    Preprocess FEK issues and convert from PDF to TXT
    """
    def __init__(self) -> None:
        pass


    def reorder_first_page(self, texts):
        """
        There are cases where "ΕΦΗΜΕΡΙΔΑ ΤΗΣ ΚΥΒΕΡΝΗΣΕΩΣ" doesn't appear in the beginning.
        This function detects such cases and reorders them in the beginning.
        """

        w = None
        if not re.search(r"ΕΦΗΜΕΡΙ(Σ|ΔΑ)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ", texts[0]):
            ind = 0
            for i, block in enumerate(texts):
                if re.search(r"ΕΦΗΜΕΡΙ(Σ|ΔΑ)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ", block):
                    ind = i
                    break

            w = texts[i:]+texts[:i]
        
        return w
    
    
    def parenthesis_line_merging(self, doc):
        texts = doc.splitlines()
        new_texts = []
        last_merged = False
        for i, text in enumerate(texts):
            if not last_merged:
                open_par, close_par = text.rfind("("), text.rfind(")")
                if open_par <= close_par:
                    new_texts.append(text)
                else:
                    new_texts.append(texts[i] + texts[i+1])
                    last_merged = True
            else:
                last_merged = False
                continue
        doc = "\n".join(new_texts)
        return doc

    def bracket_line_merging(self, doc):
        texts = doc.splitlines()
        new_texts = []
        last_merged = False
        for i, text in enumerate(texts):
            if not last_merged:
                open_par, close_par = text.rfind("["), text.rfind("]")
                if open_par <= close_par:
                    new_texts.append(text)
                else:
                    new_texts.append(texts[i] + texts[i+1])
                    last_merged = True
            else:
                last_merged = False
                continue
        doc = "\n".join(new_texts)
        return doc  
    
    
    def fix_article_errors(self, doc):
        """
        There are cases where an article appears like "Άρθ ρο".
        The same happens in the next line and same index.
        """

        texts = doc.splitlines()

        for i, text in enumerate(texts):

            pattern = r'^Ά(\s*)ρ(\s*)θ(\s*)ρ(\s*)ο'
            
            q = re.search(pattern, text)
            if q:
                if not all(x == "" for x in q.groups()):
                    for j, item in enumerate(q.groups()):
                        if item:
                            ind = j+1
                            break
                    texts[i] = texts[i][:ind] + texts[i][ind+1:]
                    texts[i+1] = texts[i+1][:ind] + texts[i+1][ind+1:]
        
        doc = "\n".join(texts)
        
        return doc
        

    def pdf2text(self, fekpath, savefile=True):
        """
        Convert PDF file to TXT with some preprocessing
        """
        # Parse PDF file in blocks
        pages = []
        with fitz.open(fekpath,) as doc:
            for page in doc:
                text = page.get_text("blocks")
                pages.append(text)
        
        # Get text of each block and exclude signature information
        pages = [[item[4] for item in page if not re.search(r"(Digitally signed|Signature)", item[4])] for page in pages]

        # Fix problematic Δ representation. Even thought it seems the same, when converted to unicode has different value 
        pages = [[re.sub(r"∆", r"Δ", item) for item in page] for page in pages]

        # Reorder first page
        pages[0] = self.reorder_first_page(pages[0])
        # pages = [self.reorder_first_page(page) for page in pages]

        doc = "".join(block for page in pages for block in page)

        doc = self.fix_article_errors(doc)


        doc = doc.replace("-\n", "")
        doc = doc.replace("−\n", "")
        
        doc = self.parenthesis_line_merging(doc)
        doc = self.bracket_line_merging(doc)

        if savefile:
            savepath = re.sub(r".pdf$", ".txt", fekpath)
            with open(savepath, 'w', encoding='utf-8') as f:
                f.write(doc)
        
        return doc
    

class FekParser(IssueParser):
    """
    Reusing IssueParser from 3gm
    """
    def __init__(self, filename, stdin=False, toTxt=False):
        super().__init__(filename, stdin, toTxt)
    

    def check_duplicate_pars(self, pars):
        '''
        Check if there are duplicates in paragraphs due to cases with same numbering as paragraphs
        '''

        int_pars = [item for item in pars if item.isdigit()]

        return not len(set(int_pars)) == len(int_pars)
    

    def get_paragraph_levels(self, items):
        levels = []
        for i, item in enumerate(items):
            if item in dc.alphabet:
                levels.append(0)  # alphabet
            elif item in dc.ab_double_combs:
                levels.append(1)  # ab combinations
            elif item in dc.latin_numbers:
                levels.append(2)  # latin numbers
            elif item in dc.numbers:
                levels.append(3)  #
        return levels

    
    def par_split_ids_with_duplicates(self, text):
        par_pattern = rf"[\n ]\(?{dc.all_combs_pat}[).] *"

        q = re.findall(par_pattern,text)  # get all listed keys

        levels = self.get_paragraph_levels(q)

        # get first level indices for numbers
        ak = 0
        level_0 = levels[0]
        level_0_inds = []
        is_correct = True
        for i in range(len(q)):
            if (levels[i] == level_0) and is_correct:
                if q[i] == dc.numbers[ak]:
                    level_0_inds.append(i)
                    ak += 1
                else:
                    qk = 0
                    if q[i] == dc.numbers[qk]:
                        # current_level = levels[i]
                        is_correct = False
                    else:
                        if q[i] == dc.numbers[ak]:
                            level_0_inds.append(i)
                            ak += 0
                            is_correct = True
        level_0_inds += [len(levels)]
        return par_pattern, level_0_inds
            
    

    def find_article_paragraphs(self, text):
        '''
        Split article into paragraphs and return them as a dict
        '''
        
        pattern = r"\n(\d{1,2})[).]"  # e.g. \n1. TEXT
        pars = re.split(pattern, text)
        pars = [item.lstrip() for item in pars]

        has_duplicate_num = self.check_duplicate_pars(pars)

        if not has_duplicate_num:
            level_0_inds = [i for i in range(len(pars)) if pars[i].isdigit()] + [len(pars)]
        else:
            par_pattern, level_0_inds = self.par_split_ids_with_duplicates(text)


            par_splits = re.split(par_pattern, text) if has_duplicate_num else pars
            par_dict = {}
            if par_splits[0] in dc.all_combs:
                par_splits.insert(0, "")

            par_dict['0'] = par_splits[0]

            # Split paragraphs based on the ids
            for j in range(len(level_0_inds)-1):
                par_split = par_splits[2*level_0_inds[j]+1:2*level_0_inds[j+1]+1]
                par = ""
                for k in range(0, len(par_split)-1, 2):
                    par += f"\n{par_split[k]}. {par_split[k+1]}"

                par = par.strip()
                par_dict[str(j+1)] = par
            
            return par_dict







