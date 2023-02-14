from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
from haystack.nodes import FARMReader
from haystack.schema import Document
from collections import OrderedDict
from rapidfuzz import fuzz
import pandas as pd

from rbner.rbNER import rbNER
from src.fek_parser import FekParser
from src import kw_dictionary as kdc
import unicodedata as ud
import re

class ml_respas():
    def __init__(self, textpath, model_name_or_path="alexaapo/greek_legal_bert_v2", data_path="haystack/data", train_filename="long_paragraphs_answers.json", use_gpu=True, reTrain=False):
        
        self.savename = textpath.split("/")[1].split(".")[0]
        self.rbner = rbNER()
        self.FPRS = FekParser(textpath)

        if reTrain:
            self.reader = FARMReader("alexaapo/greek_legal_bert_v2", use_gpu=use_gpu, top_k=3, context_window_size=256, max_seq_len=512, doc_stride=128, batch_size=25)
            self.data_dir = data_path
            self.reader.train(data_dir=self.data_dir, train_filename=train_filename, use_gpu=True, n_epochs=3, batch_size=5, save_dir="haystack/model")
        else:
            self.reader = FARMReader("haystack/model", use_gpu=use_gpu, top_k=3, context_window_size=256, max_seq_len=512, doc_stride=128, batch_size=25)
        
        
        self.ner_model = AutoModelForTokenClassification.from_pretrained("amichailidis/greek_legal_bert_v2-finetuned-ner-V3")
        self.ner_tokenizer = AutoTokenizer.from_pretrained("amichailidis/greek_legal_bert_v2-finetuned-ner-V3", model_max_length=512)
        self.ner_pip = pipeline("ner", model=self.ner_model, tokenizer=self.ner_tokenizer, grouped_entities=True)
        
        
        self.body_keywords = kdc.rbrsp_kws
        self.irrelevant_keywords = kdc.rbrsp_ikws
        #self.title_keywords = kdc.rbrsp_tkws
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

                master_unit, responsibility_paragraphs = self.get_candidate_paragraphs_per_article(article_paragraphs)
                print(f"On {AR_key} - we found {len(responsibility_paragraphs)} respa paragraphs!!")
                responsibilities = self.get_respas(master_unit, responsibility_paragraphs)
                
                if responsibilities:
                    print(f"We found {len(responsibilities)} pairs of responsibilities on Article {AR_key}")
                    responsibilities_dict[AR_key] = responsibilities
            except Exception as e:
                print(f"Article {AR_key} resulted in the following error: {e}")
                pass
            
        results = []
        for key, value in responsibilities_dict.items(): # here key has the AR_key value
            for k, v in value.items():
                if v:
                    respas = ' '.join(map(str, v.values()))
                    results.append((key, k, respas))

        pdresults = pd.DataFrame(results, columns=["Article", "Unit", "Value"])
        pdresults.to_csv("ML_RSP_"+self.savename+".csv", index=False, encoding="utf-8")
        
        return responsibilities_dict
    
    
    def has_respa_kws(self, txt):
        return any(str_kw in txt
                   for str_kw in self.body_keywords)
    
    
    def has_irrelevant_kws(self, txt):
        return any(flag_kw in txt
                   for flag_kw in self.irrelevant_keywords)
    
    
    def find_master_unit(self, paragraphs):
        master_unit = ""
        for key, value in paragraphs.items():
            units = self.rbner.hybridNER(value)
            if units:
                master_unit = units[0]
                break
        return master_unit
    
    
    def process_ner_output(self, output_list):
        entities = []
        for dct in output_list:
            if dct["score"] > 0.9:
                entities.append(dct["word"])
        return entities
    
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
        
        for idx, par in enumerate(paragraphs):

            # Get entities from Ner and remove duplicates
            # We Dont use entities = list(set(initial_entities)) to preserve order
            initial_entities = self.process_ner_output(self.ner_pip(str(par)))
            seen = set()
            entities = []
            for item in initial_entities:
                if item not in seen:
                    seen.add(item)
                    entities.append(item)
            
            
            if not entities:
                #entity = master_unit 
                continue #TODO Think again about that
                
            for entity in entities:
            
                query = self.get_query(entity)
                result = self.reader.predict(query=query,
                                             documents=[Document(content=par)],
                                             top_k=3)
                answer_offset = self.get_answer_offset(result, entity, par)

                if answer_offset:
                    answer = self.form_the_answer_span(answer_offset, par)
                else:
                    continue
           
                if entity in responsibilities:
                    responsibilities[entity].extend(answer)
                else:
                    responsibilities[entity] = answer
        
        return responsibilities
    
    
    def get_query(self, entity):
        base_query = "Τι αρμοδιότητες έχει "
        if any(x in entity for x in ["Τμήμα", "ΤΜΗΜΑ", "τμημα"]):
            return base_query + 'το ' + entity + ';'
        elif any(x in entity for x in ["Διεύθυνση", "ΔΙΕΥΘΥΝΣΗ", "διευθυνση", "Γραμματεία", "ΓΡΑΜΜΑΤΕΙΑ", "γραμματεια"]):
            return base_query + 'η ' + entity + ';'
        else:
            return base_query + entity + ';'
    
    
    def remove_intonations(self, txt):
        """ removes intonation off the text and turns all letters into capitals """
        d = {ord('\N{COMBINING ACUTE ACCENT}'):None}
        return ud.normalize('NFD',txt).lower().translate(d)
    
    
    def get_answer_offset(self, result, entity, par):
        
        answers = []
        for i in range(len(result['answers'])):
            
            itStartsAt = par.find(result['answers'][i].context)
            priorContextString = par[:itStartsAt]
            toAddString = re.split('[.)]', priorContextString)[-1].strip()
            extendedContext = toAddString + result['answers'][i].context

            if fuzz.partial_ratio(entity, self.remove_intonations(extendedContext)) > 80:
                answers.append(result['answers'][i])
          
        if answers:
            max_score = 0
            for i in range(len(answers)):
              if answers[i].score > max_score:
                  final_offset = answers[i].offsets_in_document
                  max_score = answers[i].score
            return final_offset
        else:
            return ""

    
    def form_the_answer_span(self, answer_offset, paragraph):
        answer_to_paragraph_end = paragraph[answer_offset[0].start-1:]
        try:
            par_dict = self.FPRS.find_article_paragraphs(" " + answer_to_paragraph_end, 'paragraph')
            par_dict = self.FPRS.process_last_split(par_dict)
            del par_dict["0"]
            return par_dict
        except:
            return {"#1" : answer_to_paragraph_end}
        



