#from re import compile, sub, findall, search, escape, DOTALL, match
#from collections import OrderedDict
#from gg18.ggHelper import Helper
#from gg18.respAclassifier import paragraphClf
from gg18.respA import RespExtractor
#from src.fek_parser import FekParser



class respaExtractor(RespExtractor):
    
    """
    Reusing RespExtractor from gg18
    """
    def __init__(self, textpath, text):
        super().__init__(textpath, text)



