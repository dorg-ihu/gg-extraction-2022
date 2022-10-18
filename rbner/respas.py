from rbner.rbNER import rbNER
from src.fek_parser import FekParser
from src import dictionaries as dc
from collections import OrderedDict
import re


class respas():
    
    def __init__(self, textpath):
        
        self.rbner = rbNER()
        self.FPRS = FekParser(textpath)
        
        self.body_keywords = ["αρμοδιότητες", "ΑΡΜΟΔΙΟΤΗΤΕΣ", "αρμόδιο", "ΑΡΜΟΔΙΟ"]
        
        self.irrelevant_keywords = ["σκοπό", "σκοπούς", "στόχο", "στόχους", "επιχειρησιακούς", "στρατηγικούς", "επιχειρησιακό", "στρατηγικό"]
        
        self.title_keywords = ["ΑΡΜΟΔΙΟΤΗΤΕΣ", "Αρμοδιότητες", "ΑΡΜΟΔΙΌΤΗΤΕΣ"]
        
        self.irrelevant_title = ["Προσόντα", "ΠΡΟΣΟΝΤΑ", "Προσωπικό", "Προσωπικού", "Διορισμ", "ΔΙΟΡΙΣΜ", "προσωπικού", 
                                 "Κλάδοι", "Προϊστάμενοι", "Προϊσταμένων", "Περίγραμμα θέσης", "Περιγράμματα θέσεων", "Περίγραμμα Θέσης", "Περιγράμματα Θέσεων",
                                 "Έναρξη ισχύος"]
        

    def remove_first_level(self, txt):
        first_line, rest_lines = txt.split("\n", 1)[0], "\n" + txt.split("\n", 1)[1]
        first_line = re.sub(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", first_line)
        return first_line + rest_lines

    
    def get_paragraph_levels(self, items):
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


    def find_levels_depth(self, txt):
        split_all = self.FPRS.split_all_int(txt)
        split_all = [x for x in split_all if isinstance(x, tuple)]
    
        split_all = {k:v for k,v in split_all}
        pointers_list = list(split_all.keys())
        
        levels = self.get_paragraph_levels(pointers_list)
        depth = 1
        type_of_levels = {levels[0][1]: depth}
        info = [levels[0] + (depth,) + (split_all[levels[0][0]],)]  
        for idx, (key, tag) in enumerate(levels[1:]):
            if tag not in type_of_levels:
                depth += 1
                type_of_levels[tag] = depth
                info.append((key, tag) + (depth,) + (split_all[key],))
            else:
                cur_depth = type_of_levels[tag]
                info.append((key, tag) + (cur_depth,) + (split_all[key],))
        
        # reconstructs the flat list of points into groups under the depth = 1
        split_points = [i for i, (point, typ, dep, text) in enumerate(info) if dep == 1]
        total_split = split_points + [len(info)]
        grouped_info = [info[i:j] for i, j in zip(split_points, total_split[1:])]
    
        return grouped_info, len(type_of_levels)
    
    
    def has_respa_kws(self, txt):
        return any(str_kw in txt
                   for str_kw in self.body_keywords)
    
    def has_irrelevant_kws(self, txt):
        return any(flag_kw in txt
                   for flag_kw in self.irrelevant_keywords)
            
    
    def get_candidate_paragraphs_per_article(self, paragraphs):
        respa_paragraphs = []
        for key, value in paragraphs.items():
            if ":" in value:
                unit_part = value.split(":", 1)[0]
                is_respa_related = self.has_respa_kws(unit_part)
                is_irrelevant = self.has_irrelevant_kws(unit_part)
                if is_respa_related and not is_irrelevant:
                    respa_paragraphs.append(value)
        return respa_paragraphs
    
    def get_respas(self, paragraphs):
        responsibilities = OrderedDict()
        for idx, paragraph in enumerate(paragraphs):
            try:
                new_par = self.remove_first_level(paragraph)
                grouped_info, depth = self.find_levels_depth(new_par)
                # print("The following paragraph", idx, "success")
            except Exception as e:
                print("The following paragraph", idx, "caused error", e)
                continue
            
            if depth > 1:
                for group in grouped_info:
                    cand_units = self.rbner.hybridNER(group[0][3])
                    unit = cand_units[0] if cand_units else ""
                    respas = [x[3] for x in group[1:]]
                    responsibilities[unit] = respas
            else:
                unit_part = paragraph.split(":", 1)[0]
                cand_units = self.rbner.hybridNER(unit_part)
                unit = cand_units[0] if cand_units else ""
                
                respas = [x[0] for x in grouped_info]
                respas = [x[3] for x in respas]
                responsibilities[unit] = respas
        return responsibilities
                    
                    
                    
                    
                    
               
        