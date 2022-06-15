from gg18.respA import RespExtractor
from src.fek_parser import PreParser
from src.ner import OrgExtractor

textParser = PreParser()
respaParser = RespExtractor()
ner = OrgExtractor()

def isotesting_structure(fekpath):
    text  = textParser.pdf2text(fekpath=fekpath, savefile=False)
    prerequisites = respaParser.get_dec_prereqs(text)
    articles = respaParser.get_articles(text)
    
    paragraph1 = respaParser.get_paragraphs(articles[1])
    paragraph5 = respaParser.get_paragraphs(articles[5])
    paragraph10 = respaParser.get_paragraphs(articles[10])
    paragraph15 = respaParser.get_paragraphs(articles[15])
    
    return text, prerequisites, articles, paragraph1, paragraph5, paragraph10, paragraph15


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



text, prerequisites, articles, paragraph1, paragraph10, paragraph20 = isotesting_structure(fekpaths[0])
respa, respa_decl = isotesting_respa(text)

text, prerequisites, articles, paragraph1, paragraph5, paragraph10, paragraph15 = isotesting_structure(fekpaths[9])
respa, respa_decl = isotesting_respa(text)



