from typing import final
import fitz
fitz.restore_aliases()
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

            w = texts[ind:]+texts[:ind]
        
        return w

    
    def remove_headers(self, pages):
        pages = [[text for text in page if not re.search(r"ΕΦΗΜΕΡΙ(Σ|ΔΑ)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ", text)
            ] for page in pages
        ]

        return pages
    
    
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

        # Fix typos with English letters and convert to greek
        pages = [[re.sub(dc.ab_greek_latin_pat, lambda m: dc.alphabet_latin_to_greek.get(m.group(0)), item)
                for item in page] for page in pages]

        # Reorder first page
        pages[0] = self.reorder_first_page(pages[0])
        page_zero = pages[0].copy()
        pages = self.remove_headers(pages[1:])
        pages = [page_zero] + pages

        doc = "".join(block for page in pages for block in page)

        doc = self.fix_article_errors(doc)

        doc = doc.replace("-\n", "")
        doc = doc.replace("−\n", "")
        
        
        current_number_of_lines = len(doc.splitlines())
        doc = self.parenthesis_line_merging(doc)
        doc = self.bracket_line_merging(doc)
        last_number_of_lines = len(doc.splitlines())

        while True:
            if current_number_of_lines == last_number_of_lines:
                break
            else:
                current_number_of_lines = last_number_of_lines
                doc = self.parenthesis_line_merging(doc)
                doc = self.bracket_line_merging(doc)
                last_number_of_lines = len(doc.splitlines())

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
    
    
    def replace_abbreviations(self, text):
        replacements = dc.abbr_replacements
        for k, v in replacements:
            text = text.replace(k, v)
        return text
            
    
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
            elif item in dc.ab_combs:
                levels.append(1)  # ab combinations
            elif item in dc.latin_numbers:
                levels.append(2)  # latin numbers
            elif item in dc.numbers:
                levels.append(3)  #
        return levels


    
    def find_levels_depth(self, txt):
        
        #TODO for testing purposes - remove later  
        txt = self.replace_abbreviations(txt)
        
        def paragraph_levels_alternative(items):
            levels = []
            for i, item in enumerate(items):
                if item in dc.alphabet:
                    levels.append((item, "alphabet"))  # alphabet
                elif item in dc.ab_combs:
                    levels.append((item, "abcombinations"))  # ab combinations
                elif item in dc.latin_numbers:
                    levels.append((item, "latinnumbers"))  # latin numbers
                elif item in dc.numbers:
                    levels.append((item, "therest"))  #
            return levels  
        
        split_all = self.split_all_int(txt)
        split_all = [x for x in split_all if isinstance(x, tuple)]
    
        pointers_list = [x[0] for x in split_all]
        
        levels = paragraph_levels_alternative(pointers_list)
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

    def par_split_ids_with_duplicates(self, text):
        
        # par_pattern = rf"[\n ][^(]?{dc.all_combs_pat}[).] *"

        q = re.findall(dc.par_pattern,text)  # get all listed keys
        # print("q ", q)
        levels = self.get_paragraph_levels(q)
        # print("levels ", levels)
        # get first level indices for numbers
        ak = 0
        level_0 = levels[0]

        ref_list = dc.level_to_list[level_0]

        level_0_inds = []
        is_correct = True
        for i in range(len(q)):
            if (levels[i] == level_0) and is_correct:
                if q[i] == ref_list[ak]:
                    level_0_inds.append(i)
                    ak += 1
                else:
                    qk = 0
                    if q[i] == ref_list[qk]:
                        is_correct = False
                    else:
                        if q[i] == ref_list[ak]:
                            level_0_inds.append(i)
                            ak += 0
                            is_correct = True
        level_0_inds += [len(levels)]

        return level_0_inds
            
        
    def find_article_paragraphs(self, text, split_level='article'):
        '''
        Split article into paragraphs and return them as a dict
        '''
        def prob_func(match):
            thegroup = match.group(0)
            return thegroup[:2] + ". " + thegroup[2:]
        
        def cleanIntosai(match):
            thegroup = match.group(0)
            intodict = dc.intodict
            
            for k,v in intodict.items():
                thegroup = thegroup.replace(k, v)
            if "INTOSAI" in thegroup:
                return "*INTOSAI*"
            else:
                return thegroup
        
        # before anything try to replace common mistakes for the following abbreviations
        text = self.replace_abbreviations(text)
        
        intosai_pattern = r"\(.{4}S.+\)"
        text = re.sub(intosai_pattern, cleanIntosai, text)
        
        # also get rid of the problematic pattern 3α. which will turn into 3. α. 
        problematic_pattern = r"\n(\d{1}α{1})[).]"
        text = re.sub(problematic_pattern, prob_func, text)
        
        par_dict = {}
       
        if split_level == 'article':

            pattern = r"\n(\d{1,2})[).]"  # e.g. \n1. TEXT
            pars = re.split(pattern, text)

            if len(pars) == 1:
                par_dict['0'] = text
                return par_dict

        level_0_inds = self.par_split_ids_with_duplicates(text)

        par_splits = re.split(dc.par_pattern, text)


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
    

    def split_all(self, text):
        
        splits = re.split(dc.split_all_pattern, text)
        if splits[0] in dc.all_combs:
            splits.insert(0, "")
        
        final_splits = [f"{splits[i-1]}) {splits[i]}" for i in range(2, len(splits), 2)]
        final_splits.insert(0, splits[0])
        return final_splits


    def split_all_int(self, text):
        
        splits = re.split(dc.split_all_pattern, text)
        if splits[0] in dc.all_combs:
            splits.insert(0, "")

        final_splits = [(splits[i-1], f"{splits[i-1]}) {splits[i]}") for i in range(2, len(splits), 2)]
        final_splits.insert(0, splits[0])
        return final_splits
    

    def process_last_split(self, par_dict):
        '''
        This function is used for post processing results of MLRespa
        '''
        keys = list(par_dict.keys())
        keys.sort()
        
        last_split = " " + par_dict[keys[-1]]  # added space to be able to get also the initial numbering based on the regex
        
        q = re.findall(dc.par_pattern,last_split)
        w = self.get_paragraph_levels(q)
        
        #par_level = w[0] if w else 0
        par_level = w[0] #INITIAL 
        
        k = 0
        i = 1
        for i in range(1, len(w)):
            if w[i] != par_level:
                if dc.level_to_list[w[i]][k] != q[i]:
                    break
                k += 1
        
        par_splits = re.split(dc.par_pattern, last_split)

        par_splits[1] += "."
        par_dict[keys[-1]] = " ".join(par_splits[1:2*i+1])

        return par_dict
        





        
            
        


