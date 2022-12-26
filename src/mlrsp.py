from haystack.nodes import FARMReader
from haystack.schema import Document

#import torch

from fuzzywuzzy import fuzz
from collections import OrderedDict

from rbner.rbNER import rbNER
from src.fek_parser import FekParser
from src import kw_dictionary as kdc
# from early_stopping import EarlyStopping
# import torch
# torch.cuda.empty_cache()

#reader = FARMReader(model_name_or_path="alexaapo/greek_legal_bert_v2", use_gpu=True, top_k=1, context_window_size=256, max_seq_len=512, batch_size=25, doc_stride=128)
#earlystopper = early_stopping.EarlyStopping(save_dir="haystack/model")

#data_dir = "haystack/data"

# reader.train(data_dir=data_dir, train_filename="answers_short_expanded.json", use_gpu=True, n_epochs=5, batch_size=5, save_dir="haystack/model")
#reader.train(data_dir=data_dir, train_filename="long_paragraphs_answers.json", use_gpu=True, n_epochs=3, batch_size=5, save_dir="haystack/model")


class farm():
    def __init__(self, textpath, model_name_or_path="alexaapo/greek_legal_bert_v2", data_path="haystack/data", train_filename="long_paragraphs_answers.json", use_gpu=True):
        self.rbner = rbNER()
        self.FPRS = FekParser(textpath)
        
        self.reader = FARMReader(model_name_or_path, use_gpu=use_gpu, top_k=3, context_window_size=256, max_seq_len=512, doc_stride=128, batch_size=25)
        self.data_dir = data_path
        self.reader.train(data_dir=self.data_dir, train_filename=train_filename, use_gpu=True, n_epochs=3, batch_size=5, save_dir="haystack/model")
        
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
                responsibilities = self.get_respas(master_unit, responsibility_paragraphs)
                #responsibilities = self.
                
                if responsibilities:
                    print(f"We found {len(responsibilities)} pairs of responsibilities on Article {AR_key}")
                    responsibilities_dict[AR_key] = responsibilities
            except Exception as e:
                print(f"Article {AR_key} resulted in the following error: {e}")
                pass
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
        
        # if paragraphs on the 
        if len(paragraphs) > 1:
            for par in paragraphs:
                entity = self.rbner.hybridNER(par)[0]
                if not entity:
                    entity = master_unit
                query = self.get_query(entity)
                result = self.reader.predict(query=query,
                                             documents=[Document(content=par)],
                                             top_k=3)
                offset_status = self.get_answer_offset(result, entity)
                if offset_status:
                    answer = self.form_the_answer_span(offset_status, par)
                
                if entity in responsibilities:
                    responsibilities[entity].extend(answer)
                else:
                    responsibilities[entity] = answer
        
        return responsibilities
    
    
    
    def get_query(self, entity):
        base_query = "Τι αρμοδιότητες έχει "
        if any(x in entity for x in ["Τμήμα", "ΤΜΗΜΑ"]):
            return base_query + 'το ' + entity + ';'
        elif any(x in entity for x in ["Διεύθυνση", "ΔΙΕΥΘΥΝΣΗ", "Γραμματεία", "ΓΡΑΜΜΑΤΕΙΑ"]):
            return base_query + 'η ' + entity + ';'
        else:
            return base_query + entity + ';'
    
    
    def get_answer_offset(self, result, entity):
        answers = []
        for i in range(len(result['answers'])):
            if fuzz.partial_ratio(entity, result['answers'][i].context) > 80:
                answers.append(result['answers'][i])
          
        if answers:
            max_score = 0
            for i in range(len(answers)):
              if answers[i].score > max_score:
                  answer = answers[i].offsets_in_document
                  max_score = answers[i].score
            return answer
        else:
            return ""

    
    def form_the_answer_span(self, answer, paragraph):
        return paragraph[answer[0].start-1:]





