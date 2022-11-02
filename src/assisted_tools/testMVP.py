from src.fek_parser import PreParser
from src.respa_extractor import RespExtractor
import re


# filepath = "fek-organismoi-upourgeiwn/yp-dikaiosunhs-6-2021.pdf"
filepath = "fek-organismoi-upourgeiwn/yp-ygeias-121-2017.pdf"
# filepath = "fek-organismoi-upourgeiwn/"

text = PreParser().pdf2text(filepath)
textpath = re.sub(r".pdf$", ".txt", filepath)
RSP = RespExtractor(textpath)

respas = RSP.get_rough_unit_respa_associations(text)

# articles = RSP.fekParser.articles


respas1 = RSP.get_units_and_respas(text) #RespA associations mentioned in single paragraphs. (checking existance of ":")
respas2 = RSP.get_units_followed_by_respas(text) #RespA associations mentioned as a Unit followed by a list of RespAs.
respas3 = RSP.get_units_and_respas_following_respas_decl(text) #RespA associations mentioned as a RespA declaration followed by a Unit-RespAs list.

