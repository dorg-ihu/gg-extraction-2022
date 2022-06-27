#from gg18.respA import RespExtractor
from src.fek_parser import PreParser, FekParser
from src.ner import OrgExtractor
#import collections

textParser = PreParser()
fekParser = FekParser()
fekParser = FekParser('yp-oikonomikwn-142-2017.txt')

ner = OrgExtractor()


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


fekParser = FekParser('fek-organismoi-upourgeiwn/yp-ergasiaskaikoinwnikhsasfalishs-134-2017.txt')
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
txt = 'Διάρθρωση Υπηρεσιών του Υπουργείου\n Το Υπουργείο Υγείας διαρθρώνεται ως εξής: 1. Πολιτικά Γραφεία Υπουργού και Υφυπουργών και  Γραφεία Γενικών Γραμματέων  2. Υπηρεσίες, Διευθύνσεις και Τμήματα υπαγόμενα απ’  ευθείας στον Υπουργό:  α) Σώμα Επιθεωρητών Υπηρεσιών Υγείας (Σ.Ε.Υ.Υ.)  (ν. 2920/2001 − Α΄ 131)  5. Το π.δ. 89/2014 «Διορισμός Υπουργών, Αναπληρωτών  β) Εθνικό Κέντρο Επιχειρήσεων Υγείας (ν. 3370/2006  Υπουργών και Υφυπουργών» (Α΄ 134).  − Α΄ 176)     γ) Διεύθυνση Ευρωπαϊκής και Διεθνούς Πολιτικής Υγείας δ) Μονάδα Διαμόρφωσης Πολιτικών Υγείας και Τουρισμού Υγείας, η οποία λειτουργεί σε επίπεδο τμήματος ε) Τμήμα Νομοθετικής Πρωτοβουλίας, Κοινοβουλευτι κού Ελέγχου και Κωδικοποίησης  στ) Διεύθυνση Επιστημονικής Τεκμηρίωσης, Διοικητικής και Γραμματειακής Υποστήριξης του Κεντρικού Συμβουλίου Υγείας (ΚΕ.Σ.Υ.)  ζ) Μονάδα Εσωτερικού Ελέγχου, η οποία λειτουργεί σε  επίπεδο τμήματος'
results = ner.extract_entities(txt)
print(results.ents)
ner.visualise_entities(results)
