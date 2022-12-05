from rbner.rbNER import rbNER
from src.fek_parser import FekParser
from src import kw_dictionary as kdc
from collections import OrderedDict
import re


class respas():
    
    def __init__(self, textpath):
        
        self.rbner = rbNER()
        self.FPRS = FekParser(textpath)
        self.body_keywords = kdc.rbrsp_kws
        self.irrelevant_keywords = kdc.rbrsp_ikws
        self.title_keywords = kdc.rbrsp_tkws
        self.irrelevant_title = kdc.irrelevant_title
        
    
    def main(self, articles):
        responsibilities_dict = OrderedDict()
        for AR_key, AR_value in articles.items():
            try:
                article_paragraphs = self.FPRS.find_article_paragraphs(AR_value)
                if len(article_paragraphs) > 1:
                    possible_title = article_paragraphs["0"]
                    if any(title_kw in possible_title for title_kw in self.irrelevant_title):
                        print("Article {} has been skipped due to irrelevant_title".format(AR_key))
                        continue

                master_unit, responsibility_paragraphs = self.get_candidate_paragraphs_per_article(article_paragraphs) #input article text - output list of candidate paragraphs
                responsibilities = self.get_respas(master_unit, responsibility_paragraphs) # input list of candidate paragraphs - ouput dictionary with unit-respa pairs
                
                if responsibilities:
                    print(f"We found {len(responsibilities)} pairs of responsibilities on Article {AR_key}")
                    responsibilities_dict[AR_key] = responsibilities
            except Exception as e:
                print(f"Article {AR_key} resulted in the following error: {e}")
                pass
        return responsibilities_dict
    
    def remove_first_level(self, txt):
        first_line, rest_lines = txt.split("\n", 1)[0], "\n" + txt.split("\n", 1)[1]
        first_line = re.sub(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", first_line)
        return "\n" + first_line + rest_lines

    def remove_number_level(self, txt):
        first_line, rest_lines = txt.split("\n", 1)[0], "\n" + txt.split("\n", 1)[1]
        first_line = re.sub(r"^[ ]*[0-9]+[\.\)] ", "", first_line)
        return "\n" + first_line + rest_lines

    
    def find_master_unit(self, paragraphs):
        master_unit = ""
        for key, value in paragraphs.items():
            units = self.rbner.hybridNER(value)
            if units:
                master_unit = units[0]
                break
        return master_unit

    
    def has_respa_kws(self, txt):
        return any(str_kw in txt
                   for str_kw in self.body_keywords)
    
    def has_irrelevant_kws(self, txt):
        return any(flag_kw in txt
                   for flag_kw in self.irrelevant_keywords)
            
    
    def get_candidate_paragraphs_per_article(self, paragraphs):
        
        master_unit = self.find_master_unit(paragraphs)
        
        respa_paragraphs = []
        for key, value in paragraphs.items():
            if ":" in value:
                unit_part = value.split(":", 1)[0]
                is_respa_related = self.has_respa_kws(unit_part)
                is_irrelevant = self.has_irrelevant_kws(unit_part)
                if is_respa_related and not is_irrelevant:
                    respa_paragraphs.append(value)
        return master_unit, respa_paragraphs
    
    
    def get_respas(self, master_unit, paragraphs):
        responsibilities = OrderedDict()
        for idx, paragraph in enumerate(paragraphs):
            try:
                new_par = self.remove_number_level(paragraph)
                grouped_info, depth = self.FPRS.find_levels_depth(new_par)
            except Exception as e:
                print("The following paragraph", idx, "caused error", e)
                continue
            
            if depth > 1:
                for group in grouped_info:
                    cand_units = self.rbner.hybridNER(group[0][3])
                    if not cand_units:
                        #TODO also check on the part until ":" before assigning master unit
                        unit = "##"+master_unit
                        respas = [x[3] for x in group]
                    else:
                        unit = cand_units[0]
                        respas = [x[3] for x in group[1:]]
                    if unit in responsibilities:
                        responsibilities[unit].extend(respas)
                    else:
                        responsibilities[unit] = respas
            else:
                unit_part = paragraph.split(":", 1)[0]
                cand_units = self.rbner.hybridNER(unit_part)
                unit = cand_units[0] if cand_units else "##"+master_unit
                
                respas = [x[0] for x in grouped_info]
                respas = [x[3] for x in respas]
                
                if unit in responsibilities:
                    responsibilities[unit].extend(respas)
                else:
                    responsibilities[unit] = respas
        return responsibilities
                    
     
    #TODO consider cleaning the problematic pairs that get_respas method produces
    def postprocess_cleaning_of_problematic_pairs(self):
        return
                    
                    
                    
               
        