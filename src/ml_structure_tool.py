from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer, AutoModelForSequenceClassification
from flair.embeddings import TransformerWordEmbeddings
from polyfuzz.models import Embeddings
from polyfuzz import PolyFuzz

from src import kw_dictionary as kdc
from src.fek_parser import FekParser
from fuzzywuzzy import fuzz
from string import punctuation
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import time
import re



class ml_structure():
    def __init__(self, textpath):
        
        self.savename = textpath.split("/")[1].split(".")[0]
        
        self.body_keywords = kdc.rbre_kws
        self.irrelevant_keywords = kdc.rbre_ikws
        self.FPRS = FekParser(textpath)
        
        self.ner_model = AutoModelForTokenClassification.from_pretrained("amichailidis/greek_legal_bert_v2-finetuned-ner-V3")
        self.ner_tokenizer = AutoTokenizer.from_pretrained("amichailidis/greek_legal_bert_v2-finetuned-ner-V3")
        self.ner_pip = pipeline("ner", model=self.ner_model, tokenizer=self.ner_tokenizer, grouped_entities=True)
        
        self.re_model = AutoModelForSequenceClassification.from_pretrained("amichailidis/greek_legal_bert_v2-finetuned-re-V2")
        self.re_tokenizer = AutoTokenizer.from_pretrained("amichailidis/greek_legal_bert_v2-finetuned-re-V2")
        self.re_pip = pipeline("text-classification", model=self.re_model, tokenizer=self.re_tokenizer)
        
        self.embeddings = TransformerWordEmbeddings('alexaapo/greek_legal_bert_v2')
        self.bert = Embeddings(self.embeddings)
        self.bert_model = PolyFuzz(self.bert)
        
        self.tokens_limit = 512
        
    
    def main(self, articles):
        START = time.time()
        relation_paragraphs = []
        for AR_key, AR_value in articles.items():
            try:
                article_paragraphs = self.FPRS.find_article_paragraphs(AR_value)
                relation_paragraphs.append(self.get_candidate_paragraphs_per_article(AR_key, article_paragraphs))
            except Exception as e:
                print(e)
        flat_paragraphs = [item for sublist in relation_paragraphs for item in sublist]
        data = {"paragraphs": flat_paragraphs}
        data_df = pd.DataFrame(data)

        tokenizer = AutoTokenizer.from_pretrained("alexaapo/greek_legal_bert_v2")
        data_df["tokens"] = [len(tokenizer.tokenize(x)) for x in data_df["paragraphs"]]
        valid_paragraphs_df = data_df.loc[data_df["tokens"] < self.tokens_limit]
        paragraphs_df = valid_paragraphs_df[["paragraphs"]]
        #paragraphs_df.to_csv("module_testing_paragraphs.csv", index=False)
        #invalid_paragraphs_df = data_df.loc[data_df["tokens"] >= 512]

        relations_df = self.structure_ml(paragraphs_df)
        
        print(f"Execution time: {time.time() - START}")
        g = self.get_rdf(relations_df)
        
        #self.visualize_rdf_graph(g)
        self.visualize_rdf_graph_pydot(g)
        
        return relations_df
    
    def process_ner_output(self, entity_mention, inputs):
        re_input = []
        for idx1 in range(len(entity_mention) - 1):
            for idx2 in range(idx1 + 1, len(entity_mention)):
                ent_1 = entity_mention[idx1]
                ent_2 = entity_mention[idx2]
    
                ent_1_type = ent_1['entity_group']
                ent_2_type = ent_2['entity_group']
                ent_1_s = ent_1['start']
                ent_1_e = ent_1['end']
                ent_2_s = ent_2['start']
                ent_2_e = ent_2['end']
                new_re_input = ""
                for c_idx, c in enumerate(inputs):
                    if c_idx == ent_1_s:
                        new_re_input += "<S:{:s}>".format(ent_1_type)
                    elif c_idx == ent_1_e:
                        new_re_input += "</S:{:s}>".format(ent_1_type)
                    elif c_idx == ent_2_s:
                        new_re_input += "<O:{:s}>".format(ent_2_type)
                    elif c_idx == ent_2_e:
                        new_re_input += "</O:{:s}>".format(ent_2_type)
                    new_re_input += c
                re_input.append({"re_input": new_re_input, "arg1": ent_1, "arg2": ent_2, "input": inputs})
        return re_input
    
    def post_process_re_output(self, re_output, text_input, ner_output, re_input):

        final_output = []
        for idx, out in enumerate(re_output):
            if out["label"] != 'NoRel':
                tmp = re_input[idx]
                tmp['relation_type'] = out
                tmp.pop('re_input', None)
                final_output.append(tmp)
    
        template = {"input": text_input,
                    "entity": ner_output,
                    "relation": final_output}
    
        return template


    def structure_ml(self, paragraphs):
        the_object=[]
        the_subject=[]
        relationship=[]
        
        print(f"The number of detected paragraphs after applying rules is {len(paragraphs)}")
        print("This process might take a while!!")
        
        for (idx, row) in paragraphs.iterrows():

            for string in row:
                row = re.sub("\([Α-Ωα-ω]*.[Α-Ωα-ω.]*\)","",string)
                row = re.sub(' +', ' ',row)
                
            ner_output = self.ner_pip(str(row))
            re_input = self.process_ner_output(ner_output, str(row))
            
            re_output = []
            for idx in range(len(re_input)):
                tmp_re_output = self.re_pip(re_input[idx]["re_input"])
                re_output.append(tmp_re_output[0])

            re_ner_output = self.post_process_re_output(re_output, str(row), ner_output, re_input)
            for rel in re_ner_output["relation"]:
              the_subject.append(rel['arg1']['word'])
              the_object.append(rel['arg2']['word'])
              relationship.append(rel['relation_type']['label'])

   
        kg_df = pd.DataFrame({"subject":the_subject, "object": the_object, "relation": relationship})
        kg_df = kg_df.drop_duplicates()
        
        subj=kg_df['subject'].values.tolist()
        obj=kg_df['object'].values.tolist()
        
        self.bert_model.match(subj,obj)
        self.bert_model.group(self.bert)
        
        matches = self.bert_model.get_matches()
        matches = matches.drop_duplicates()
        
        rslt_df = matches[matches['Similarity'] > 0.9]
        rslt_df=rslt_df.reset_index()
        
        for i in range(len(rslt_df)):
            if rslt_df["From"][i] in kg_df.values:
              kg_df = kg_df.replace(rslt_df["From"][i],rslt_df["Group"][i])
          
            if rslt_df["To"][i] in kg_df.values:
              kg_df = kg_df.replace(rslt_df["From"][i],rslt_df["Group"][i])
        

        kg_df = kg_df[kg_df['subject'] != kg_df['object']]


        initial_answers = list(zip(kg_df.subject, kg_df.object, kg_df.relation))
        unique_answers = self.unique(initial_answers)
        

        
        answers = []
        for ele in unique_answers:
            if fuzz.ratio(ele[0], ele[1]) > 90 or len(ele[1].split())==1:
                continue
            
            if len(ele[1].translate(str.maketrans('', '', punctuation))) > 10:
              answers.append(ele)
        
        return pd.DataFrame(answers, columns=["subject", "object", "relation"])     
    
    
    def has_structure_kws(self, txt):
        return any(str_kw in txt
                   for str_kw in self.body_keywords)
    
    
    def has_irrelevant_kws(self, txt):
        return any(flag_kw in txt
                   for flag_kw in self.irrelevant_keywords)
    
    
    def get_candidate_paragraphs_per_article(self, AR_key, paragraphs):
        relation_paragraphs = []        
        for pkey, value in paragraphs.items():
            if ":" in value:
                unit_part = value.split(":", 1)[0]
                is_structure_related = self.has_structure_kws(unit_part)
                is_irrelevant = self.has_irrelevant_kws(unit_part)
                if is_structure_related and not is_irrelevant:
                    relation_paragraphs.append(value)
        return relation_paragraphs
    
    
    def unique(self, sequence):
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]
    
    
    def visualize_pairs(self, df):
        G=nx.from_pandas_edgelist(df, "subject", "object", 
                          edge_attr=True, create_using=nx.MultiDiGraph())
        plt.figure(figsize=(300,100))
        
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
        nx.draw_networkx(G, with_labels=False, node_shape= "s", node_size=40000, node_color='none', linewidths=150, width=3, arrows=True, pos = pos)
        
        nodenames = {}
        
        for n in G.nodes():
          splittext = n.split(" ")
          for x in range(2, len(splittext), 5):
              splittext[x] = "\n"+splittext[x].lstrip()
          text = " ".join(splittext)
          
          nodenames[n] = text
        
        nx.draw_networkx_labels(G, pos=pos, labels=nodenames, bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.5'), font_size=12)
        
        plt.show()
        
    
    def get_rdf(self, df):
        from rdflib import Graph, Literal
        g = Graph()
        for index, row in df.iterrows():
            g.add((Literal(row['subject']), Literal(row['relation']), Literal(row['object'])))
        
        g.serialize(destination=self.savename+'.rdf', format='turtle')
        
        return g
    
        
    def visualize_rdf_graph(self, g):
        import matplotlib.pyplot as plt
        import networkx as nx
        
        nx_graph = nx.Graph()
        for s, p, o in g:
            nx_graph.add_edge(s, o, attr_dict={p: g.predicates(s, o)})
        
        plt.figure(figsize=(25, 25))
        nx.draw_kamada_kawai(nx_graph, with_labels=True)
        plt.show()    

    def visualize_rdf_graph_pydot(self, g):
        import networkx as nx
        from networkx.drawing.nx_pydot import to_pydot
        
        nx_graph = nx.Graph()
        for s, p, o in g:
            #s_encoded, o_encoded, p_encoded  = s.replace(':', '-'), o.replace(':', '-'), p.replace(':', '-')
            nx_graph.add_edge(s, o)
            
        
        pydot_graph = nx.nx_pydot.to_pydot(nx_graph)
        pydot_graph.set_rankdir('LR')
        
        pydot_graph.write_png("MLRE_"+self.savename+'.png', encoding='UTF-8')
        print("Png file created at your directory")

        
        
