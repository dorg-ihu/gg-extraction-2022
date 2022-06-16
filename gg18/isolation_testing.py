from gg18.respA import RespExtractor
from src.fek_parser import PreParser, FekParser
from src.ner import OrgExtractor

textParser = PreParser()
fekParser = FekParser()
fekParser = FekParser('yp-oikonomikwn-142-2017.txt')
respaParser = RespExtractor()
ner = OrgExtractor()

#%%

text = textParser.pdf2text(fekpath='yp-oikonomikwn-142-2017.pdf', savefile=True)
filename = 'yp-oikonomikwn-142-2017.pdf'
articles = FekParser.find_articles(filename)


text = textParser.pdf2text(fekpath='yp-oikonomikwn-142-2017.pdf', savefile=False)
responsibilities_extraction = respaParser.get_rough_unit_respa_associations(text)



def isotesting_structure(fekpath):
    text  = textParser.pdf2text(fekpath=fekpath, savefile=False)
    prerequisites = respaParser.get_dec_prereqs(text)
    articles = respaParser.get_articles(text)
    
    paragraphsofArt1 = respaParser.get_paragraphs(articles[1])
    paragraphsofArt5 = respaParser.get_paragraphs(articles[5])
    paragraphsofArt10 = respaParser.get_paragraphs(articles[10])
    paragraphsofArt15 = respaParser.get_paragraphs(articles[15])
    
    return text, prerequisites, articles, paragraphsofArt1, paragraphsofArt5, paragraphsofArt10, paragraphsofArt15


def isotesting_respa(text):
    responsibilities = respaParser.get_units_followed_by_respas(text)
    responsibilities_decl = respaParser.get_units_and_respas_following_respas_decl(text)
    return responsibilities, responsibilities_decl




fekpaths = [
    'C:/Users/kostas/GitHub/edyte/gg-extraction-2022/yp-oikonomikwn-142-2017.pdf',
    'C:/Users/kostas/Documents/EDYTE/papers/fek-organismoi-upourgeiwn/yp-agrotikhsanaptukshskaitrofimwn-97-2017.pdf',
    'C:/Users/kostas/Documents/EDYTE/papers/fek-organismoi-upourgeiwn/yp-anaptiksiskaiependusewn-5-2022.pdf',
    'C:/Users/kostas/Documents/EDYTE/papers/fek-organismoi-upourgeiwn/yp-dikaiosunhs-6-2021.pdf',
    'C:/Users/kostas/Documents/EDYTE/papers/fek-organismoi-upourgeiwn/yp-ekswterikwnapodimouellhnismou-4781-2022.pdf',
    'C:/Users/kostas/Documents/EDYTE/papers/fek-organismoi-upourgeiwn/yp-ergasiaskaikoinwnikhsasfalishs-134-2017.pdf',
    'C:/Users/kostas/Documents/EDYTE/papers/fek-organismoi-upourgeiwn/yp-eswterikwn-141-2017.pdf',
    'C:/Users/kostas/Documents/EDYTE/papers/fek-organismoi-upourgeiwn/yp-ethnikisaminas-2292-1995.pdf',
    'C:/Users/kostas/Documents/EDYTE/papers/fek-organismoi-upourgeiwn/yp-klimatikhskrishskaipolitikhsprostasias-151-2004.pdf',
    'C:/Users/kostas/Documents/EDYTE/papers/fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf'
    ]


text, prerequisites, articles, paragraphsofArt1, paragraphsofArt5, paragraphsofArt10, paragraphsofArt15 = isotesting_structure(fekpaths[4])
respa, respa_decl = isotesting_respa(text)



txt = respaParser.get_paragraphs(articles[15])
print(respaParser.get_units_followed_by_respas(txt))

articles = fekParser.articles
print(fekParser.articles.keys())



#%%

fekParser = FekParser('yp-oikonomikwn-142-2017.txt')

dates = fekParser.dates
articles = fekParser.articles
articles_as_paragraphs = fekParser.articles_as_paragraphs

statutes = fekParser.statutes







#%%
txt = 'Διάρθρωση Υπηρεσιών του Υπουργείου\n Το Υπουργείο Υγείας διαρθρώνεται ως εξής: 1. Πολιτικά Γραφεία Υπουργού και Υφυπουργών και  Γραφεία Γενικών Γραμματέων  2. Υπηρεσίες, Διευθύνσεις και Τμήματα υπαγόμενα απ’  ευθείας στον Υπουργό:  α) Σώμα Επιθεωρητών Υπηρεσιών Υγείας (Σ.Ε.Υ.Υ.)  (ν. 2920/2001 − Α΄ 131)  5. Το π.δ. 89/2014 «Διορισμός Υπουργών, Αναπληρωτών  β) Εθνικό Κέντρο Επιχειρήσεων Υγείας (ν. 3370/2006  Υπουργών και Υφυπουργών» (Α΄ 134).  − Α΄ 176)     γ) Διεύθυνση Ευρωπαϊκής και Διεθνούς Πολιτικής Υγείας δ) Μονάδα Διαμόρφωσης Πολιτικών Υγείας και Τουρισμού Υγείας, η οποία λειτουργεί σε επίπεδο τμήματος ε) Τμήμα Νομοθετικής Πρωτοβουλίας, Κοινοβουλευτι κού Ελέγχου και Κωδικοποίησης  στ) Διεύθυνση Επιστημονικής Τεκμηρίωσης, Διοικητικής και Γραμματειακής Υποστήριξης του Κεντρικού Συμβουλίου Υγείας (ΚΕ.Σ.Υ.)  ζ) Μονάδα Εσωτερικού Ελέγχου, η οποία λειτουργεί σε  επίπεδο τμήματος'
results = ner.extract_entities(txt)
print(results.ents)
ner.visualise_entities(results)
