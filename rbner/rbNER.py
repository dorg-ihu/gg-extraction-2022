from fuzzywuzzy import fuzz
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import string
from string import digits
import unicodedata as ud
import pandas as pd
from collections import Counter
from gr_nlp_toolkit import Pipeline


class rbNER():
    
    def __init__(self):
        self.gazpath = "rbner/gazetter_list.xlsx"
        self.data = pd.read_excel(self.gazpath)
        self.gazlist = self.gazlist_preprocess()
        self.stop = stopwords.words('greek')
        self.threshold = 0.95
        self.nlp = Pipeline("pos,ner,dp")
        self.unit_keywords = ["ΤΜΗΜΑ", "ΓΡΑΦΕΙΟ ", "ΓΡΑΦΕΙΑ ", "ΑΥΤΟΤΕΛΕΣ ", "ΑΥΤΟΤΕΛΗ ", "ΔΙΕΥΘΥΝΣ", "ΥΠΗΡΕΣΙΑ ", 
							  "ΣΥΜΒΟΥΛΙ", 'ΓΡΑΜΜΑΤΕIA ', "ΥΠΟΥΡΓ", "ΕΙΔΙΚΟΣ ΛΟΓΑΡΙΑΣΜΟΣ", "MONAΔ", "ΠΕΡΙΦΕΡΕΙ", "ΑΡΧΗ", "ΑΡΧΕΣ", "ΣΩΜΑ", "ΓΕΝΙΚΗ", "ΕΠΙΤΡΟΠΗ"]

    
    @staticmethod
    def remove_punct_and_digits(x):
        """ removes punctuation and digits from the given text """
        return x.translate(str.maketrans("", "", string.punctuation)).translate(str.maketrans("", "", digits))
    
    
    @staticmethod
    def remove_list_points(txt):
        """ removes list points from the given text if they exist in the beginning of the line """
        txt = re.sub(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", txt)
        return re.sub(r"\n[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", txt)
    
    
    @staticmethod
    #TODO check if this is already taken into account on PreParser
    def clean_up_txt(txt):
        txt = re.sub('[\t ]+', ' ', txt)
        txt = re.sub('\-[\s]+', '', txt)
        txt = re.sub('\−[\s]+', '', txt)
        return txt.replace("\f", '')

    
    @staticmethod
    def acronyms(txt, replace=False):
        #TODO try to match the case where last character doesn't end with a dot (.) eg "Ε.Σ.Υ" instead of "Ε.Σ.Υ."
        """ finds the acronyms (even if they are presented with more than one character).
            If replace is set to True then the method returns the given text having the acronyms removed
            else returns a dictionary with matches
        """
        #pattern = r'(?:(?<=\.|\s)[Α-Ω]\.)+'
        pattern = r'\b(?:[α-ωά-ώΑ-ΩΆ-Ώ]*\.[Α-Ωα-ω]*){2,}'
        if not replace:
            return set(re.findall(pattern, txt))
        else:
            return re.sub(pattern, "", txt)
    
    
    @staticmethod
    def remove_articles(txt):
        #txt_words = txt.split(" ")
        tobeRemoved = ["O", "H", "Το", "Οι", "Ένας", "Μία", "Ένα"]
        resultwords = [word for word in re.split("\W+", txt) if word not in tobeRemoved]
        return ' '.join(resultwords)
        
    
    @staticmethod
    def regex_entities(txt):
        """ finds the occurences of the following pattern into the text
            Consecutive words starting with capital letter that may also contain in-between "και-του-της-των" or ","
        """
        subpattern = "(και)(του)(της)(των)"
        pattern = rf"([Α-ΩΆ-Ώ][\w-]+[,\s{subpattern}]*)+((?=\s[Α-ΩΆ-Ώ]))(?!\s[\W])(?:\s[Α-Ω][\w-]+)"
        results = [x.group() for x in re.finditer(pattern, txt)]
        return [rbNER.remove_articles(x) for x in results]
        
    
    @staticmethod
    def remove_intonations(txt):
        """ removes intonation off the text and turns all letters into capitals """
        d = {ord('\N{COMBINING ACUTE ACCENT}'):None}
        return ud.normalize('NFD',txt).upper().translate(d)
        
    
    def gazlist_preprocess(self):
        """ upon call removes units from the gazeteer list that seem irrelevant or exist as duplicates 
            and cleans the remaining unit names (remove punctuation and digits)
        """
        filtered_data = self.data[(self.data["descriptions"] != 'ΑΛΛΟ') & (self.data["descriptions"] != 'ΓΡΑΦΕΙΟ')].drop_duplicates()
        gazlist = filtered_data["preferredLabels"].tolist()
        return [self.remove_punct_and_digits(x).strip().replace("  ", " ") for x in gazlist]
    
    
    def gazetter_entities(self, txt, returnSimilar=True):
        """ finds similar substrings from gazetter list inside the given text after calling -cleaning methods-
            if none of the existing units is similar enough ( higher than threshold ) the 3 most similar are returned instead
        """
        txt = self.remove_intonations(txt)
        txt = self.remove_punct_and_digits(txt).replace("\n", " ").replace("  ", " ")
        
        ents, scored_elems, topN = [], [], 3
        for ele in self.gazlist:
            similarity = fuzz.partial_ratio(txt, ele)/100
            scored_elems.append((ele, similarity))
            if similarity > self.threshold:
                ents.append((ele, similarity))
        if not ents and returnSimilar:
            print("Couldn't find entities with similarity higher than the threshold, instead the top {} results are being returned".format(topN))
            return Counter(dict(scored_elems)).most_common(topN)
        else:
            return ents

    
    def sentences_with_keywords(self, txt):
        """ cleans the given text and afterwards splits into sentences. Finally iterates through the sentences and returns those that
            contain any of the unit identifications as they were introduced during the constructor.
        """
        #TODO write a method that performs basic txt cleaning
        txt = self.remove_intonations(txt)
        txt = self.acronyms(txt, replace=True)
        txt = self.clean_up_txt(txt)
        sentences = sent_tokenize(txt, language="Greek")
        sentence_cands = []
        for unit in self.unit_keywords:
            for sentence in sentences:
                if unit in sentence.upper():
                    sentence_cands.append(sentence)
        unique_cands = set(sentence_cands)
        return unique_cands
        
    
    def grnlptoolkit(self, text):
        doc = self.nlp(text)
        return doc





































