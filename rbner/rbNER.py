from fuzzywuzzy import fuzz
import re
from nltk.corpus import stopwords
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
        self.gazlist = self.dataPreprocess()
        self.stop = stopwords.words('greek')
        self.threshold = 0.95
        self.nlp = Pipeline("pos,ner,dp")

    
    def remove_punct_and_digits(self, x):
        return x.translate(str.maketrans("", "", string.punctuation)).translate(str.maketrans("", "", digits))

    
    def dataPreprocess(self):
        filtered_data = self.data[(self.data["descriptions"] != 'ΑΛΛΟ') & (self.data["descriptions"] != 'ΓΡΑΦΕΙΟ')].drop_duplicates()
        gazlist = filtered_data["preferredLabels"].tolist()
        return [self.remove_punct_and_digits(x).strip().replace("  ", " ") for x in gazlist]

    
    def acronyms(self, txt):
        pattern = r'(?:(?<=\.|\s)[Α-Ω]\.)+'
        return set(re.findall(pattern, txt))

        
    def regex_entities(self, txt):
        pattern = r'([Α-ΩΆ-Ώ][\w-]+[,\s(και)]*)+((?=\s[Α-ΩΆ-Ώ]))(?!\s[\W])(?:\s[Α-Ω][\w-]+)'
        return [x.group() for x in re.finditer(pattern, txt)]

    
    def gazetter_entities(self, txt):
        d = {ord('\N{COMBINING ACUTE ACCENT}'):None}
        txt = ud.normalize('NFD',txt).upper().translate(d)
        txt = self.remove_punct_and_digits(txt).replace("\n", "").replace("  ", " ")
        
        ents, scored_elems, topN = [], [], 3
        for ele in self.gazlist:
            similarity = fuzz.partial_ratio(txt, ele)/100
            scored_elems.append((ele, similarity))
            if similarity > self.threshold:
                ents.append((ele, similarity))
        if not ents:
            print("Couldn't find entities with similarity higher than the threshold, instead the top {} results are being returned".format(topN))
            return Counter(dict(scored_elems)).most_common(topN)
        else:
            return ents
                
    def grnlptoolkit(self, text):
        doc = self.nlp(text)
        return doc
