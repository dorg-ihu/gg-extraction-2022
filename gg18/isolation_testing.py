#from gg18.respA import RespExtractor
from src.fek_parser import PreParser, FekParser

#import collections

textParser = PreParser()
fekParser = FekParser()
fekParser = FekParser('yp-oikonomikwn-142-2017.txt')

text = textParser.pdf2text()


#%% articles - paragraphs - lines 3gm


fekpaths = [
    'fek-organismoi-upourgeiwn/yp-oikonomikwn-142-2017.pdf',
    'fek-organismoi-upourgeiwn/yp-agrotikhsanaptukshskaitrofimwn-97-2017.pdf',
    'fek-organismoi-upourgeiwn/yp-anaptiksiskaiependusewn-5-2022.pdf', # starts with Άρθρο τάδε + characters + προβλημα με τον πινακα στο τελος
    'fek-organismoi-upourgeiwn/yp-dikaiosunhs-6-2021.pdf', # τελευταίο άρθρο κενό
    'fek-organismoi-upourgeiwn/yp-ekswterikwnapodimouellhnismou-4781-2022.pdf', # το κουλό
    'fek-organismoi-upourgeiwn/yp-ergasiaskaikoinwnikhsasfalishs-134-2017.pdf',
    'fek-organismoi-upourgeiwn/yp-eswterikwn-141-2017.pdf',
    'fek-organismoi-upourgeiwn/yp-ethnikisaminas-2292-1995.pdf', # NO
    'fek-organismoi-upourgeiwn/yp-klimatikhskrishskaipolitikhsprostasias-151-2004.pdf', # NO
    'fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf', # τελευταίο άρθρο κενό
    'fek-organismoi-upourgeiwn/yp-nautiliaskainhsiwtikhspolitikhs-13-2018.pdf',
    'fek-organismoi-upourgeiwn/yp-paideiaskaithriskeumatwn-18-2018.pdf',
    'fek-organismoi-upourgeiwn/yp-periballontoskaienergeias-132-2017.pdf',
    'fek-organismoi-upourgeiwn/yp-politismoukaiathlitismou-4-2018.pdf',
    'fek-organismoi-upourgeiwn/yp-prostasiastoupolith-62-2019.pdf',
    'fek-organismoi-upourgeiwn/yp-psifiakhsdiakuvernhshs-40-2020.pdf',
    'fek-organismoi-upourgeiwn/yp-tourismou-127-2017.pdf',
    'fek-organismoi-upourgeiwn/yp-ygeias-121-2017.pdf',
    'fek-organismoi-upourgeiwn/yp-ypodomwnkaimetaforwn-123-2017.pdf'
    ]

# for path in fekpaths:
#     textParser.pdf2text(path, savefile=True)


fekParser = FekParser('fek-organismoi-upourgeiwn/yp-tourismou-127-2017.txt')
articless = fekParser.articles
paragraphss = fekParser.articles_as_paragraphs
lines = fekParser.lines
digitmatches = fekParser.digitmatches
unique_digitmatches = set(digitmatches)





#%% get Respa based on articles and paragraphs of 3gm
#from src.fek_parser import PreParser, FekParser


from gg18.gm3respA import RespaExtractor
respaParser = RespaExtractor('fek-organismoi-upourgeiwn/yp-tourismou-127-2017.txt')
allrespas = respaParser.get_rough_unit_respa_associations()


from src.fek_parser import PreParser
from gg18.respA import RespExtractor
respParser = RespExtractor()
textparser = PreParser()
text = textparser.pdf2text("fek-organismoi-upourgeiwn/yp-tourismou-127-2017.pdf")
allrespasgg18 = respParser.get_rough_unit_respa_associations(text)












#%% test digit regex
#λαλακκκκ
import re

string = ' 2. H Διεύθυνση Εκπαιδευτικής Τεχνολ'
x = re.search(r'\d+.', string)

""" maybe more elegant """
# ^\d+\.    ==> 1. or 11.
# ^\d+\D+\) ==> 1α) or 11aa)
# ^\d+\)    ==> 1) or 11)
# ^\d+\D+\. ==> 1a. or 11aa. 

# ^\d+\D*[.)]
string = '7 ΠΕ. 18.08 Οδοντοτεχνικής, 1 ΠΕ. 18.09 Κοινωνικής Ερ-'
y = re.match(r'^\d+\.|^\d+\D+\)|^\d+\)|^\d+\D+\.', string.lstrip()[:6])

z = re.match(r'^\d+\D*[.)]', string.lstrip())

j = re.match(r'\d{1,3}\S{1,3}(\)|\.)', string.lstrip())



#%%
from src.ner import OrgExtractor
ner = OrgExtractor()



#txt = 'Διάρθρωση Υπηρεσιών του Υπουργείου\n Το Υπουργείο Υγείας διαρθρώνεται ως εξής: 1. Πολιτικά Γραφεία Υπουργού και Υφυπουργών και  Γραφεία Γενικών Γραμματέων  2. Υπηρεσίες, Διευθύνσεις και Τμήματα υπαγόμενα απ’  ευθείας στον Υπουργό:  α) Σώμα Επιθεωρητών Υπηρεσιών Υγείας (Σ.Ε.Υ.Υ.)  (ν. 2920/2001 − Α΄ 131)  5. Το π.δ. 89/2014 «Διορισμός Υπουργών, Αναπληρωτών  β) Εθνικό Κέντρο Επιχειρήσεων Υγείας (ν. 3370/2006  Υπουργών και Υφυπουργών» (Α΄ 134).  − Α΄ 176)     γ) Διεύθυνση Ευρωπαϊκής και Διεθνούς Πολιτικής Υγείας δ) Μονάδα Διαμόρφωσης Πολιτικών Υγείας και Τουρισμού Υγείας, η οποία λειτουργεί σε επίπεδο τμήματος ε) Τμήμα Νομοθετικής Πρωτοβουλίας, Κοινοβουλευτι κού Ελέγχου και Κωδικοποίησης  στ) Διεύθυνση Επιστημονικής Τεκμηρίωσης, Διοικητικής και Γραμματειακής Υποστήριξης του Κεντρικού Συμβουλίου Υγείας (ΚΕ.Σ.Υ.)  ζ) Μονάδα Εσωτερικού Ελέγχου, η οποία λειτουργεί σε  επίπεδο τμήματος'
#txt = articless["Άρθρο 1"]
#partxt = paragraphss["Άρθρο 1"].value()

import pandas as pd
output = 'ner_yp_tourismou_127-2017'
#df = pd.DataFrame(columns=["text", "ner"])

paragraph = []
results = []
for article in paragraphss.values():
    for par in article.values():
        paragraph.append(par)

for par in paragraph:
    r = ner.extract_entities(par)
    ents = r.ents
    results.append(ents)

data = pd.DataFrame(zip(paragraph, results))
data.to_excel("NER-yp-oikonomikwn-142-2017.xlsx", index=False, encoding='utf-8')

paragraph[0]
r = ner.extract_entities(paragraph[0])
r.ents


export = pd.DataFrame([])














exampletext = 'Το Τμήμα Χωροταξίας και το Τμήμα Ψυχαγωγίας είναι στον ίδιο όροφο του'
exampleresult = ner.extract_entities(exampletext)
print(exampleresult.ents)
ner.visualise_entities(exampleresult)




exampletext2 = 'Γενική Διεύθυνση Οικονομικών και Διοικητικών Υπηρεσιών και Κάτι Ακόμα'
exampleresult2 = ner.extract_entities(exampletext2)
print(exampleresult2.ents)
ner.visualise_entities(exampleresult)


txt = '2.α. Γενική Γραμματεία Υπουργείου Οικονομικών (α) Υπηρεσίες που υπάγονται στο Διοικητικό Γραμματέα (αα) Αυτοτελές Τμήμα Πολιτικής Σχεδίασης Εκτάκτου Ανάγκης (Π.Σ.Ε.Α.) (ββ) Αυτοτελές Τμήμα Κοινοβουλευτικού Ελέγχου (γγ) Αυτοτελές Τμήμα Νομοθετικής Πρωτοβουλίας (δδ) Αυτοτελή Διεύθυνση Ανθρώπινου Δυναμικού και Οργάνωσης ΕΦΗΜΕΡΙΔΑ TΗΣ ΚΥΒΕΡΝΗΣΕΩΣ (β) Γενικές Διευθύνσεις (αα) Γενική Διεύθυνση Οικονομικών Υπηρεσιών β. Γενική Γραμματεία Πληροφοριακών Συστημάτων (α) Υπηρεσίες που υπάγονται στον Τομεακό Γραμματέα (αα) Αυτοτελές Τμήμα Στρατηγικής, Προγραμματισμού και Διαχείρισης Έργων (ββ) Αυτοτελές Τμήμα Ασφάλειας (β) Γενικές Διευθύνσεις (αα) Γενική Διεύθυνση Υποδομών Πληροφορικής και Επικοινωνιών (ββ) Γενική Διεύθυνση Ανάπτυξης και Παραγωγικής Λειτουργίας Πληροφοριακών Συστημάτων γ. Γενική Γραμματεία Οικονομικής Πολιτικής (α) Υπηρεσίες που υπάγονται στον Τομεακό Γραμματέα (αα) Κεντρική Μονάδα Κρατικών Ενισχύσεων (ββ) Μονάδα Αποκρατικοποιήσεων, Διαχείρισης Κινητών Αξιών και Επιχειρησιακού Σχεδιασμού (β) Γενικές Διευθύνσεις (αα) Γενική Διεύθυνση Οικονομικής Πολιτικής δ. Γενική Γραμματεία Δημοσιονομικής Πολιτικής (α) Υπηρεσίες που υπάγονται στον Τομεακό Γραμματέα (αα) Αυτοτελές Τμήμα Επιχειρησιακής Ανάλυσης και Υποστήριξης (β) Γενικές Διευθύνσεις (αα) Γενική Διεύθυνση Δημοσιονομικής Πολιτικής και Προϋπολογισμού (ββ) Γενική Διεύθυνση Θησαυροφυλακίου και Δημοσιονομικών Κανόνων (γγ) Γενική Διεύθυνση Δημοσιονομικών Ελέγχων (δδ) Γενική Διεύθυνση Ελέγχων Συγχρηματοδοτούμενων Προγραμμάτων (εε) Γενική Διεύθυνση Χορήγησης Συντάξεων Δημοσίου Τομέα ε. Γενική Γραμματεία Δημόσιας Περιουσίας (α) Υπηρεσίες που υπάγονται στον Τομεακό Γραμματέα (αα) Αυτοτελές Γραφείο Ελληνικού (ββ) Αυτοτελές Τμήμα Μητρώου Ακίνητης Περιουσίας (β) Γενικές Διευθύνσεις (αα) Γενική Διεύθυνση Δημόσιας Περιουσίας και Κοινωφελών Περιουσιών στ. Ειδική Γραμματεία Σώματος Δίωξης Οικονομικού Εγκλήματος (α) Κεντρική Υπηρεσία (αα) Διεύθυνση Στρατηγικού Σχεδιασμού και Προγραμματισμού Ερευνών (ββ) Διεύθυνση Επιχειρησιακής Υποστήριξης (β) Επιχειρησιακή Διεύθυνση Σώματος Δίωξης Οικονομικού Εγκλήματος (Σ.Δ.Ο.Ε.) Αττικής (γ) Επιχειρησιακή Διεύθυνση Σ.Δ.Ο.Ε. Μακεδονίας '
exampleresult2 = ner.extract_entities(txt)
print(exampleresult2.ents)
ner.visualise_entities(exampleresult2)




import re
def remove_list_points(txt):
    txt = re.sub(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", txt)
    return re.sub(r"\n[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", txt)


x = 'α) Πότε θα πας στο σχολείο'
y = remove_list_points(x)
print(y[0].isdigit())
print(y[0].isupper())


sum(1 for c in x[:5] if c.isupper())





import fitz

def reorder_first_page(self, texts):
    """
    There are cases where "ΕΦΗΜΕΡΙΔΑ ΤΗΣ ΚΥΒΕΡΝΗΣΕΩΣ" doesn't appear in the beginning.
    This function detects such cases and reorders them in the beginning.
    """

    w = None
    if not re.search(r"ΕΦΗΜΕΡΙ(Σ|ΔΑ)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ", texts[0]):
        ind = 0
        for i, block in enumerate(texts):
            if re.search(r"ΕΦΗΜΕΡΙ(Σ|ΔΑ)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ", block):
                ind = i
                break

        w = texts[i:]+texts[:i]
    
    return w


def fix_article_errors(self, doc):
    """
    There are cases where an article appears like "Άρθ ρο".
    The same happens in the next line and same index.
    """

    texts = doc.splitlines()

    for i, text in enumerate(texts):

        pattern = r'^Ά(\s*)ρ(\s*)θ(\s*)ρ(\s*)ο'
        
        q = re.search(pattern, text)
        if q:
            if not all(x == "" for x in q.groups()):
                for j, item in enumerate(q.groups()):
                    if item:
                        ind = j+1
                        break
                texts[i] = texts[i][:ind] + texts[i][ind+1:]
                texts[i+1] = texts[i+1][:ind] + texts[i+1][ind+1:]
    
    doc = "\n".join(texts)
    
    return doc


def pdf2text(self, fekpath, savefile=True):
    """
    Convert PDF file to TXT with some preprocessing
    """
    # Parse PDF file in blocks
    pages = []
    with fitz.open(fekpath,) as doc:
        for page in doc:
            text = page.get_text("blocks")
            pages.append(text)
    
    # Get text of each block and exclude signature information
    pages = [[item[4] for item in page if not re.search(r"(Digitally signed|Signature)", item[4])] for page in pages]

    # Fix problematic Δ representation. Even thought it seems the same, when converted to unicode has different value 
    pages = [[re.sub(r"∆", r"Δ", item) for item in page] for page in pages]

    # Reorder first page
    pages[0] = self.reorder_first_page(pages[0])
    # pages = [self.reorder_first_page(page) for page in pages]

    doc = "".join(block for page in pages for block in page)

    doc = self.fix_article_errors(doc)


    doc = doc.replace("-\n", "")
    doc = doc.replace("−\n", "")
    


    if savefile:
        savepath = re.sub(r".pdf$", ".txt", fekpath)
        with open(savepath, 'w', encoding='utf-8') as f:
            f.write(doc)
    
    return doc




span_list = []
for block in page.getText("dict", flags=0)["blocks"]:  # a list of text block dictionaries
    for line in block["lines"]:
        for span in line["spans"]:
            span_rect = fitz.Rect(span["bbox"])  # rect of span text
            if span_rect not in table_rect:  # ensure outside table area
                span_list.append((span_rect, span["text"]))
# the span_list can now be processed as desired.



pages = []
fekpath = 'C:/Users/kostas/GitHub/edyte/gg-extraction-2022/fek-organismoi-upourgeiwn/yp-oikonomikwn-142-2017.pdf'
with fitz.open(fekpath,) as doc:
    for page in doc:
        span_list = []
        for block in page.getText("dict", flags=0)["blocks"]:  # a list of text block dictionaries
            for line in block["lines"]:
                for span in line["spans"]:
                    span_rect = fitz.Rect(span["bbox"])  # rect of span text
                    if span_rect not in table_rect:  # ensure outside table area
                        span_list.append((span_rect, span["text"]))



doc = fitz.open("C:/Users/kostas/GitHub/edyte/gg-extraction-2022/fek-organismoi-upourgeiwn/yp-oikonomikwn-142-2017.pdf")
page = doc[86]
hor_lines = []
paths = page.getDrawings()
for p in paths:
    for item in p["items"]:
        if item[0] == "l":  # this is a line item
            p1 = item[1]  # start point
            p2 = item[2]  # stop point
            if p1.y == p2.y:  # line horizontal?
                hor_lines.append(p1.y)

doc.close()


table_captions = []  # rectangles of table captions
image_captions = []  # rectangles of image captions
blocks = page.get_text("dict", flags=0)["blocks"]
for b in blocks:
    for l in b["lines"]:
        if len(l["spans"]) != 1:
            continue
        for s in l["spans"]:
            text = s["text"]
            if text.startswith("Figure ") and ": " in text:
                image_captions.append(fitz.Rect(s["bbox"]))
            elif text.startswith("Table ") and ": " in text:
                table_captions.append(fitz.Rect(s["bbox"]))









s = 'Κα) λημερα που λέει ο λόγος ελπίζω να είστε καλά'


def parenthesis_checking(s):
    open_par, close_par = s.rfind("("), s.rfind(")")
    print(open_par, close_par)
    if open_par <= close_par:
        return s
    else:
        return s + "TODO"


print(parenthesis_checking(s))


def reorder_first_page(texts):
    """
    There are cases where "ΕΦΗΜΕΡΙΔΑ ΤΗΣ ΚΥΒΕΡΝΗΣΕΩΣ" doesn't appear in the beginning.
    This function detects such cases and reorders them in the beginning.
    """

    w = None
    if not re.search(r"ΕΦΗΜΕΡΙ(Σ|ΔΑ)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ", texts[0]):
        ind = 0
        for i, block in enumerate(texts):
            if re.search(r"ΕΦΗΜΕΡΙ(Σ|ΔΑ)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ", block):
                ind = i
                break

        w = texts[i:]+texts[:i]
    
    return w


def fix_article_errors(doc):
    """
    There are cases where an article appears like "Άρθ ρο".
    The same happens in the next line and same index.
    """

    texts = doc.splitlines()

    for i, text in enumerate(texts):

        pattern = r'^Ά(\s*)ρ(\s*)θ(\s*)ρ(\s*)ο'
        
        q = re.search(pattern, text)
        if q:
            if not all(x == "" for x in q.groups()):
                for j, item in enumerate(q.groups()):
                    if item:
                        ind = j+1
                        break
                texts[i] = texts[i][:ind] + texts[i][ind+1:]
                texts[i+1] = texts[i+1][:ind] + texts[i+1][ind+1:]
    
    doc = "\n".join(texts)
    
    return doc

def parenthesis_line_merging(doc):
    texts = doc.splitlines()
    new_texts = []
    last_merged = False
    for i, text in enumerate(texts):
        if not last_merged:
            open_par, close_par = text.rfind("("), text.rfind(")")
            if open_par <= close_par:
                new_texts.append(text)
            else:
                new_texts.append(texts[i] + texts[i+1])
                last_merged = True
        else:
            last_merged = False
            continue
    doc = "\n".join(new_texts)
    return doc

def bracket_line_merging(doc):
    texts = doc.splitlines()
    new_texts = []
    last_merged = False
    for i, text in enumerate(texts):
        if not last_merged:
            open_par, close_par = text.rfind("["), text.rfind("]")
            if open_par <= close_par:
                new_texts.append(text)
            else:
                new_texts.append(texts[i] + texts[i+1])
                last_merged = True
        else:
            last_merged = False
            continue
    doc = "\n".join(new_texts)
    return doc      



fekpath = 'fek-organismoi-upourgeiwn/yp-tourismou-127-2017.pdf'
#def pdf2text(self, fekpath, savefile=True):
"""
Convert PDF file to TXT with some preprocessing
"""
import fitz
import re
# Parse PDF file in blocks
pages = []
with fitz.open(fekpath,) as doc:
    for page in doc:
        text = page.get_text("blocks")
        pages.append(text)

# Get text of each block and exclude signature information
pages = [[item[4] for item in page if not re.search(r"(Digitally signed|Signature)", item[4])] for page in pages]

# Fix problematic Δ representation. Even thought it seems the same, when converted to unicode has different value 
pages = [[re.sub(r"∆", r"Δ", item) for item in page] for page in pages]

# Reorder first page
pages[0] = reorder_first_page(pages[0])
# pages = [self.reorder_first_page(page) for page in pages]

doc = "".join(block for page in pages for block in page)

print(len(doc.splitlines()))
doc = fix_article_errors(doc)


doc = doc.replace("-\n", "")
doc = doc.replace("−\n", "")
print(len(doc.splitlines()))

doc = parenthesis_line_merging(doc)
print(len(doc.splitlines()))

doc = bracket_line_merging(doc)
print(len(doc.splitlines()))





