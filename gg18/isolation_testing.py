from respA import RespExtractor

parser = RespExtractor()

txt = parser.get_units_and_respas_following_respas_decl(text)
prerqs = parser.get_dec_prereqs(text)
