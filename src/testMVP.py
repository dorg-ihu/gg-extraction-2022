from src.fek_parser import PreParser
from src.respa_extractor import RespExtractor
import re


filepath = "fek-organismoi-upourgeiwn/yp-dikaiosunhs-6-2021.pdf"



text = PreParser().pdf2text(filepath)
textpath = re.sub(r".pdf$", ".txt", filepath)
respas = RespExtractor(textpath).get_rough_unit_respa_associations(text)
print(len(respas))