from rbner.rbNER import rbNER
from src.fek_parser import FekParser
import networkx as nx
import pandas as pd
import re
from src import kw_dictionary as kdc


class rb_structure():

    def __init__(self, textpath):
        
        self.savename = textpath.split("/")[1].split(".")[0]
        self.rbner = rbNER()
        self.FPRS = FekParser(textpath)
        #TODO consider for keywords : [ "έχει", "είναι" , "κατανέμονται στ" , "κατανέμονται μεταξύ", "υπηρεσίες υπαγόμενες" ]
        self.body_keywords = kdc.rbre_kws
        self.irrelevant_keywords = kdc.rbre_ikws
        self.unit_keywords = kdc.rbre_ukws
        
        self.irrelevant_title = kdc.irrelevant_title
        self.upper_structure_kws = kdc.upper_structure_kws
        self.upper_master_unit = "Υπουργείο"
    
    
    def main(self, articles):
        relations_list = []
        for AR_key, AR_value in articles.items():
            try:
                article_paragraphs = self.FPRS.find_article_paragraphs(AR_value)
                if len(article_paragraphs) > 1:
                    possible_title = rbNER.remove_intonations(article_paragraphs["0"])
                    if any(title_kw in possible_title for title_kw in self.irrelevant_title):
                        print(f"Article {AR_key} has been skipped due to irrelevant_title")
                        continue
                else:
                    master_unit, relation_paragraphs = self.get_candidate_paragraphs_per_article(AR_key, article_paragraphs)
                    relations = self.get_relations(master_unit, relation_paragraphs)
                    print(f"Article {AR_key} was processed as unified article (no paragraphs)")
                    relations_list.extend(relations)
                    continue
                    
                    
                # This case aims to cover the articles that have colon on paragraph 0 i.e Article 5 -periballontos
                title_colon_case = self.title_colon_article(possible_title, AR_key, AR_value)
                if title_colon_case:
                    print(f"Article {AR_key} was processed as title_colon_case")
                    relations_list.extend(title_colon_case)
                    continue
                
                # THIS IS FOR UPPER ARTICLES
                # Upper articles are expected to define relations on each paragraph that contains ":"
                upper_case = self.upper_article_case(possible_title, AR_key, article_paragraphs)
                if upper_case:
                    print(f"Article {AR_key} was processed as upper_case")
                    relations_list.extend(upper_case)
                    continue

                # If not on the upper case then go go as usual (normal case)
                # returns which paragraphs meet the STRUCTURE requirements
                master_unit, relation_paragraphs = self.get_candidate_paragraphs_per_article(AR_key, article_paragraphs) 
                relations = self.get_relations(master_unit, relation_paragraphs)
                print(f"Article {AR_key} was processed as normal (contains paragraphs)")
                relations_list.extend(relations)
            except Exception as e:
                print(f"Article {AR_key} resulted in error {e}")
                pass
        
        columns = ["Article", "Paragraph", "subject", "object"]
        pdresults = pd.DataFrame(relations_list, columns=columns)
        pdresults.to_csv("RB_RE_"+self.savename+".csv", index=False, encoding="utf-8")
        # final_list = self.postprocessing(relations_list)
        return relations_list
    
    
    def upper_article_case(self, possible_title, AR_key, article_paragraphs):
        results = []
        if any(title_kw in possible_title for title_kw in self.upper_structure_kws):      
            for pkey, paragraph in article_paragraphs.items():
                identifier = "##"+AR_key+"/"+pkey
                if ":" in paragraph:
                    paragraph_unitpart = paragraph.split(":", 1)[0]
                    cand_units = self.rbner.hybridNER(paragraph_unitpart)
                    paragraph_main_unit = self.upper_master_unit if not cand_units else cand_units[0]
                    try:
                        new_par = self.remove_number_level(paragraph)
                        grouped_info, depth = self.FPRS.find_levels_depth(new_par)
                    except Exception as e:
                        print(f"The following: {identifier}, caused error, {e}")
                        continue
                    if depth > 1:
                        for group in grouped_info:
                            if len(group) > 1:
                                cand_units = self.rbner.hybridNER(group[0][3])
                                unit = identifier if not cand_units else cand_units[0]
                                subunits = [x[3] for x in group[1:]]
                                for sunit in subunits:
                                    results.append((AR_key, pkey, unit, self.remove_list_points(sunit)))
                            else:
                                results.append((AR_key, pkey, paragraph_main_unit, self.remove_list_points(group[0][3])))
                    else:
                        for group in grouped_info:
                            subunits = [x[3] for x in group]
                            for sunit in subunits:
                                results.append((AR_key, pkey, paragraph_main_unit, self.remove_list_points(sunit)))            
        return results
    
    
    def title_colon_article(self, possible_title, AR_key, AR_value):
        results = []
        if ":" in possible_title and self.has_structure_kws(possible_title):
            unit = self.find_master_unit(possible_title)
            if not unit:
                unit = "##"+AR_key
            grouped_info, depth = self.FPRS.find_levels_depth(AR_value)
            
            if depth == 1:
                subunits = [group[0][3] for group in grouped_info]
                subunits = [self.remove_list_points(x) for x in subunits]
                for sunit in subunits:
                    results.append((AR_key, unit, sunit))
            else:
                #This case never found with a proper consistency so its skiped
                pass
        return results
    
    
    def find_master_unit(self, paragraphs):
        master_unit = ""
        for key, value in paragraphs.items():
            if ":" in value:
                unitpart = value.split(":", 1)[0]
                units = self.rbner.hybridNER(unitpart)
            else:
                units = self.rbner.hybridNER(value)
            if units:
                master_unit = units[0]
                break
        return master_unit
                 
    
    def get_candidate_paragraphs_per_article(self, AR_key, paragraphs):

        master_unit = self.find_master_unit(paragraphs)
        
        relation_paragraphs = []        
        for pkey, value in paragraphs.items():
            if ":" in value:
                unit_part = value.split(":", 1)[0]
                is_structure_related = self.has_structure_kws(unit_part)
                is_irrelevant = self.has_irrelevant_kws(unit_part)
                if is_structure_related and not is_irrelevant:
                    relation_paragraphs.append((AR_key, pkey, value))
        return master_unit, relation_paragraphs
                    
    
    def get_relations(self, master_unit, paragraphs):
        relations = []
        for idx, paragraph in enumerate(paragraphs):
            AR_key, pkey = paragraph[0], paragraph[1]
            parts = paragraph[2].split(":", 1)

            unit_part, rel_part = parts[0], parts[1]
            try:
                unit = self.rbner.hybridNER(unit_part)[0]
            except:
                unit = master_unit
            
            sublevels = self.FPRS.split_all(rel_part)
            if sublevels:
                for lvl in sublevels:
                    has_unit = self.has_unit_kws(lvl)
                    if has_unit:
                        relations.append((AR_key, pkey, unit, self.remove_list_points(lvl)))
        return relations
        
    
    def remove_number_level(self, txt):
        first_line, rest_lines = txt.split("\n", 1)[0], "\n" + txt.split("\n", 1)[1]
        first_line = re.sub(r"^[ ]*[0-9]+[\.\)] ", "", first_line)
        return first_line.strip() + rest_lines #TODO check the empty character that exists on result
        
    def remove_list_points(self, txt):
        txt = re.sub(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", txt)
        return re.sub(r"\n[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", txt)
    
    def has_unit_kws(self, txt):
        return any(unit_kw in txt
                   for unit_kw in self.unit_keywords)
    
    def has_structure_kws(self, txt):
        return any(str_kw in txt
                   for str_kw in self.body_keywords)
    
    def has_irrelevant_kws(self, txt):
        return any(flag_kw in txt
                   for flag_kw in self.irrelevant_keywords)
    

    def get_relations_graph(self, relations):

        import pandas as pd
        import matplotlib.pyplot as plt
        
        interim_relations = [t for sublist in relations for l in sublist for t in l]
        final_relations = []
        for i in range(0, len(interim_relations), 2):
            final_relations.append((interim_relations[i], interim_relations[i+1]))
        
        
        the_subject = [x[0] for x in final_relations]
        the_object = [x[1] for x in final_relations]
        
        df = pd.DataFrame({"subject": the_subject,
                           "object": the_object})
        
        G=nx.from_pandas_edgelist(df, "subject", "object", 
                          edge_attr=True, create_using=nx.MultiDiGraph())
        plt.figure(figsize=(30,10))
        pos = nx.spring_layout(G)
        nx.draw(G, with_labels=True, node_color='red', edge_cmap=plt.cm.Blues, pos = pos)
        plt.show()
        
    
    
    def topo_pos(self, G):
        """Display in topological order, with simple offsetting for legibility"""
        pos_dict = {}
        for i, node_list in enumerate(nx.topological_generations(G)):
            x_offset = len(node_list) / 2
            y_offset = 0.1
            for j, name in enumerate(node_list):
                pos_dict[name] = (j - x_offset, -i + j * y_offset)
        return pos_dict
    
    
    def postprocessing(self, relation_list):
        final_list = []
        for rel in relation_list:
            interim_list = []
            for tup in rel:
                unit = tup[0].replace("\n", "")
                subunit = tup[1].replace("\n", "")
                interim_list.append((unit, subunit))
            final_list.append(interim_list)
        return final_list
    
    
    
    
