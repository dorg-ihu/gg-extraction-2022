from src import kw_dictionary as kdc
from collections import Counter
from fuzzywuzzy import fuzz
from string import digits
import unicodedata as ud
import pandas as pd
import string
import re


class rbNER():
    
    def __init__(self):
        self.gazpath = "rbner/gazetter_list.xlsx"
        self.data = pd.read_excel(self.gazpath)
        self.gazlist = self.gazlist_preprocess()
        self.threshold = 0.8
        self.unit_keywords = kdc.rbner_kws
        
    
    def hybridNER(self, txt):
        """ combines the main methods within the rbNER class on 3 steps: 
            1. get possible entities from regex that finds words with first letter capitalized,
            2. keep those that contain any of the keywords defined on constructor """
        initial_entities = rbNER.regex_entities(txt)
        initial_clean_entities = [rbNER.remove_intonations(x) for x in initial_entities]
        initial_dict = dict(zip(initial_entities, initial_clean_entities))

        entities = []
        for (k, v) in initial_dict.items():
            for keyword in self.unit_keywords:
                if keyword in v:
                    entities.append(k)
                    break
        return entities 
    
    
    def hybridNER_gazlist(self, txt):
        """ combines the main methods within the rbNER class on 3 steps: 
            1. get possible entities from regex that finds words with first letter capitalized,
            2. keep those that contain any of the keywords defined on constructor,
            3. try to match the remaining with the gazetteer list """
        initial_entities = rbNER.regex_entities(txt)
        initial_entities = [rbNER.remove_intonations(x) for x in initial_entities]

        interim_entities = []
        for ent in initial_entities:
            for keyword in self.unit_keywords:
                if keyword in ent:
                    interim_entities.append(ent)
                    break
        
        final_entities = []
        for ient in interim_entities:
            for gaz in self.gazlist:
                score = fuzz.ratio(gaz, ient)/100
                if score >= self.threshold:
                    final_entities.append(ient)
                    break

        return final_entities 
    
    
    def hybridNER_index(self, txt):
        """ combines the main methods within the rbNER class on 3 steps: 
            1. get possible entities from regex that finds words with first letter capitalized,
            2. keep those that contain any of the keywords defined on constructor,
            3. try to match the remaining with the gazetteer list 
            * different from hybridNER on also returning the index margins for each match"""
        initial_entities = rbNER.regex_entities_index(txt)
        initial_entities = [(rbNER.remove_intonations(x[0]), x[1], x[2]) for x in initial_entities]

        interim_entities = []
        for ent, start, end in initial_entities:
            for keyword in self.unit_keywords:
                if keyword in ent:
                    interim_entities.append((ent, start, end))
                    break

        final_entities = []
        for ient, start, end in interim_entities:
            for gaz in self.gazlist:
                score = fuzz.ratio(gaz, ient)/100
                if score >= self.threshold:
                    final_entities.append((ient, start, end))
                    break

        return final_entities 
    
    
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
    def clean_up_txt(txt):
        txt = re.sub('[\t ]+', ' ', txt)
        txt = re.sub('\-[\s]+', '', txt)
        txt = re.sub('\−[\s]+', '', txt)
        return txt.replace("\f", '')

    
    @staticmethod
    def acronyms(txt, replace=False):
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
    def acronyms_dict(txt):
        # Tries to find all acronyms with the respective descriptive way of referring them in order to create a big dictionary
        pattern = r"([Α-ΩΆ-Ώ][\w-]+[,\s(και)(του)(της)]*)+((?=\s[Α-ΩΆ-Ώ]))(?!\s[\W])(?:\s[Α-ΩΆ-Ώ][\w-]+)\s\(+\b(?:[α-ωά-ώΑ-ΩΆ-Ώ]*\.[Α-Ωα-ω]*){2,}\)+"
        return set(re.findall(pattern, txt))
    
    
    @staticmethod
    def remove_articles(txt):
        tobeRemoved = ["O", "H", "Το", "Τον", "Τη", "Την", "Οι", "Ένας", "Μία", "Ένα"]
        resultwords = [word for word in re.split("\W+", txt) if word not in tobeRemoved]
        return ' '.join(resultwords)
    
    
    @staticmethod
    def regex_entities(txt):
        """ finds the occurences of the following pattern into the text
            Consecutive words starting with capital letter that may also contain in-between "και-του-της-των" or ","
        """
        subpattern = "(και)(του)(της)(των)"
        pattern = rf"([Α-ΩΆ-Ώ][\w-]+[,\s{subpattern}]*)+((?=\s[Α-ΩΆ-Ώ]))(?!\s[\W])(?:\s[Α-ΩΆ-Ώ][\w-]+)"
        results = [x.group() for x in re.finditer(pattern, txt)]
        return [rbNER.remove_articles(x) for x in results]
     
        
    @staticmethod
    def regex_entities_index(txt):
        """ finds the occurences of the following pattern into the text
            Consecutive words starting with capital letter that may also contain in-between "και-του-της-των" or ","
        """
        subpattern = "(και)(του)(της)(των)"
        pattern = rf"([Α-ΩΆ-Ώ][\w-]+[,\s{subpattern}]*)+((?=\s[Α-ΩΆ-Ώ]))(?!\s[\W])(?:\s[Α-ΩΆ-Ώ][\w-]+)"
        #results = [x.group() for x in re.finditer(pattern, txt)]
        
        results = [(x.group(), x.start(0), x.end(0)) for x in re.finditer(pattern, txt, flags=0)]
        return [(rbNER.remove_articles(x[0]), x[1], x[2]) for x in results]
    
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
    
    
    def gazetter_entities_R(self, txt, returnSimilar=True):
        """ finds similar substrings from gazetter list inside the given text after calling -cleaning methods-
            if none of the existing units is similar enough ( higher than threshold ) the 3 most similar are returned instead
        """
        txt = self.remove_intonations(txt)
        txt = self.remove_punct_and_digits(txt).replace("\n", " ").replace("  ", " ")
        
        ents, scored_elems, topN = [], [], 3
        for ele in self.gazlist:
            similarity = fuzz.ratio(txt, ele)/100
            scored_elems.append((ele, similarity))
            if similarity > 0.9:
                ents.append((txt, similarity))
        if not ents and returnSimilar:
            print("Couldn't find entities with similarity higher than the threshold, instead the top {} results are being returned".format(topN))
            return Counter(dict(scored_elems)).most_common(topN)
        else:
            return ents
    



