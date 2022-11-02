import spacy
from spacy import displacy


class OrgExtractor:
    """
    Detect organisations in text using pretrained NER model
    """

    def __init__(self, model='gm3/models/3gm_ner_model') -> None:
        self.nlp  = spacy.load(model)
    
    
    def extract_entities(self, text):
        return self.nlp(text)
    

    def visualise_entities(self, doc) -> None:
        """
        Visualise entities using displacy
        
        Params:
        doc: Object of type spacy.tokens.doc.Doc
        """
        displacy.serve(doc, style="ent")
    




