from rbner.rbNER import rbNER
from src.fek_parser import FekParser
import networkx as nx
from src import kw_dictionary as kdc
import re


class structure():
    
    def __init__(self, textpath):

        self.rbner = rbNER()
        self.FekP = FekParser(textpath)
        #TODO consider for keywords : [ "έχει", "είναι" , "κατανέμονται στ" , "κατανέμονται μεταξύ" ]
        self.body_keywords = kdc.rbre_kws
        self.irrelevant_keywords = kdc.rbre_ikws
        self.title_keywords = kdc.rbre_tkws
        self.unit_keywords = kdc.rbre_ukws
        self.irrelevant_title = kdc.irrelevant_title
    
    def get_potential_title(self, levels):
        if len(levels) > 1:
            return levels["0"]
        else:
            return ""
    
    
    def find_master_unit(self, paragraphs):
        master_unit = ""
        for key, value in paragraphs.items():
            units = self.rbner.hybridNER(value)
            if units:
                master_unit = units[0]
                break
        return master_unit
    
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
    
    
    def has_structure_kws_title(self, txt):
        return any(str_kw in txt
                   for str_kw in self.title_keywords)
    
    
    def get_structure(self, levels):
        candidates = []
        
        main_unit = self.get_main_unit(levels["1"]) if len(levels) > 1 else ""
        for key, value in levels.items():
            is_structure_related = self.has_structure_kws(value)
            if is_structure_related:
                sublevels = self.FekP.split_all(value)
                lvl_ner = self.rbner.hybridNER(sublevels[0])
                #lvl_ner = self.rbner.hybridNER(value)
                if lvl_ner:
                    candidates.append((main_unit, value))
        return candidates
                
    
    def get_candidate_paragraphs_per_article(self, paragraphs):
        
        master_unit = self.find_master_unit(paragraphs)
        
        relation_paragraphs = []        
        for key, value in paragraphs.items():
            if ":" in value:
                unit_part = value.split(":", 1)[0]
                is_structure_related = self.has_structure_kws(unit_part)
                is_irrelevant = self.has_irrelevant_kws(unit_part)
                if is_structure_related and not is_irrelevant:
                    relation_paragraphs.append(value)
        return master_unit, relation_paragraphs
                    
    
    def get_relations(self, master_unit, paragraphs):
        relations = []
        for idx, paragraph in enumerate(paragraphs):
            parts = paragraph.split(":", 1)

            unit_part, rel_part = parts[0], parts[1]
            try:
                unit = self.rbner.hybridNER(unit_part)[0]
            except:
                unit = master_unit
            
            sublevels = self.FekP.split_all(rel_part)
            if sublevels:
                for lvl in sublevels:
                    has_unit = self.has_unit_kws(lvl)
                    if has_unit:
                        relations.append((unit, self.remove_list_points(lvl)))
        return relations
    
    
    
    def get_relations_graph(self, relations):
        G = nx.DiGraph()
        for relation in relations:
            # for tup in relation:
            #     G.add_edges_from(tup)
            G.add_edges_from(relation)
        print("The created graph has {} nodes and {} edges".format(len(G.nodes), len(G.edges)))
        #print(G.nodes)
        #print(len(set(G.nodes)))

        pos = self.topo_pos(G)
        nx.draw(G, pos=pos, with_labels=False, node_size=20, arrowsize=5)
        
        #pos = nx.spring_layout(G, scale = 3)
        # nx.draw_networkx(G, pos=pos, with_labels=False, node_size=20, arrowsize=5)
        return
    
    
    def topo_pos(self, G):
        """Display in topological order, with simple offsetting for legibility"""
        pos_dict = {}
        for i, node_list in enumerate(nx.topological_generations(G)):
            x_offset = len(node_list) / 2
            y_offset = 0.1
            for j, name in enumerate(node_list):
                pos_dict[name] = (j - x_offset, -i + j * y_offset)
        return pos_dict
    
    
    
    def get_main_unit(self, txt):
        try:
            first_sentence = txt.split('.')[1]
            return self.rbner.hybridNER(first_sentence)[0]
        except:
            return ""
        