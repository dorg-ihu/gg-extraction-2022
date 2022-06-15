import urllib
from urllib.request import Request
import shutil
import urllib.parse
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import collections
import datetime
import re
import csv
from json import dumps
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from pickle import dump, load, HIGHEST_PROTOCOL


# Helper class that defines useful formatting and file handling functions
class Helper:

    # Initialize empty dict for saving compiled regex objects
    date_patterns = {}
    camel_case_patteren = re.compile("([α-ωά-ώ])([Α-ΩΆ-Ώ])")
    final_s_pattern = re.compile("(ς)([Α-ΩΆ-Ώα-ωά-ώ])")
    upper_s_pattern = re.compile("(Σ)(ΚΑΙ)")
    u_pattern = re.compile("(ύ)(και)")

    # Converts upper / lowercase text with possible ambiguous latin characters to a fully greek uppercase word with
    # no accents.
    # @todo: Use regex or other way to speed up
    @staticmethod
    def normalize_greek_name(name):
        name = name.replace(",", " ")
        # α, β, γ, δ, ε, ζ, η, θ, ι, κ, λ, μ, ν, ξ, ο, π, ρ, σ, τ, υ, φ, χ, ψ, ω
        name = name.replace("ΐ", "ϊ").upper()

        # Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω
        # A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

        replace_chars = {'Ά': 'Α', 'Έ': 'Ε', 'Ή': 'Η', 'Ί': 'Ι', 'Ϊ': 'Ι', 'Ό': 'Ο', 'Ύ': 'Υ', 'Ϋ': 'Υ', 'Ώ': 'Ω',
                         'A': 'Α', 'B': 'Β', 'E': 'Ε', 'H': 'Η', 'I': 'Ι', 'K': 'Κ', 'M': 'Μ', 'N': 'Ν', 'O': 'Ο',
                         'T': 'Τ', 'X': 'Χ', 'Y': 'Υ', 'Z': 'Ζ'}

        for char in replace_chars:
            name = name.replace(char, replace_chars[char])

        # Remove characters that should not belong in the name
        name = re.sub("[^Α-ΩΆ-ΏΪΫ\s]+", "", name)

        return ' '.join(name.split())

    @staticmethod
    # Performs an http request and returns the response
    def get_url_contents(link, content_type=''):
        try:
            with urllib.request.urlopen(link, data=None, timeout=240) as url:
                response = url.read().decode("utf-8")

                if content_type == 'json':
                    s = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(response)
                    return s
                else:
                    return response

        except urllib.error.HTTPError as e:
            print(e)
            return {}
        except urllib.error.URLError as e:
            print(e)
            return {}

    @staticmethod
    def download(url, file_name= None, folder = os.getcwd()):
        @staticmethod
        def get_file_name(open_request):
            if 'Content-Disposition' in open_request.info():
                # If the response has Content-Disposition, try to get filename from it
                cd = dict(map(
                    lambda x: x.strip().split('=') if '=' in x else (x.strip(), ''),
                    open_request.info()['Content-Disposition'].split(';')))
                if 'filename' in cd:
                    filename = cd['filename'].strip("\"'")
                    if filename:
                        return filename

            # If no filename was found above, parse it out of the final URL.
            return os.path.basename(urllib.parse.urlsplit(open_request.url)[2])

        request = Request(url)
        r = urllib.request.urlopen(request)

        try:
            if not file_name:
                file_name = get_file_name(r)

            file_path = os.path.join(folder, file_name)
            print(file_path)
            with open(file_path, 'wb') as f:
                # print('@@@@@@@@@@@@', file_path, r.status)
                shutil.copyfileobj(r, f)
        finally:
            r.close()
            return True

    @staticmethod
    def write_to_pickle_file(data, pickle_file):
        with open(pickle_file, 'wb') as handle:
                dump(data, handle, protocol=HIGHEST_PROTOCOL)    

    @staticmethod
    def load_pickle_file(pickle_file):
        with open(pickle_file, 'rb') as handle:
            data = load(handle)
        return data

    @staticmethod
    def get_json(data, encoding=''):
        return json.dumps(data) if not encoding else json.dumps(data, indent=4, ensure_ascii=False).encode(encoding)

    @staticmethod
    def get_xml(data):
        return dicttoxml(data)

    @staticmethod
    def export_json(json, jsonfile, encoding=''):
        with open(jsonfile, 'w') as file:
            file.write(json if not encoding else json.decode(encoding))

    @staticmethod
    def export_xml(xml, xmlfile):
        with open(xmlfile, 'w') as file:
            reparsed = parseString(xml)
            file.write(reparsed.toprettyxml())

    # Clears wikipedia annotations from a string
    @staticmethod
    def clear_annotations(text):
        return re.sub('\[[0-9]+\]', '', text)

    @staticmethod
    def clean_up_txt(txt):
        txt = re.sub('[\t ]+', ' ', txt)
        txt = re.sub('\-[\s]+', '', txt)
        txt = re.sub('\−[\s]+', '', txt)
        return txt.replace("\f", '')

    @staticmethod
    def remove_txt_prelims(txt):
        prelim_regex = []
        prelim_regex.append("(?:Τεύχος|ΤΕΥΧΟΣ)\s*[Α-Ω].*\nΕΦΗΜΕΡΙ.*\n[0-9]*\n")
        prelim_regex.append("[0-9]*\s*\nΕΦΗΜΕΡΙ.*\n(?:Τεύχος|ΤΕΥΧΟΣ)\s*[Α-Ω].*\n")
        prelim_regex.append("ΕΦΗΜΕΡΙ.*\s*\n[0-9]*\s*\n")
        prelim_regex.append(".ρθρο\s*[0-9]*\s*\n")
        for regex in prelim_regex:
            pat = re.compile(regex)
            txt = pat.sub('', txt)
        return txt
    
    @staticmethod
    def codify_list_points(txt):
        txt = re.sub(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "Bullet ", txt)
        return re.sub(r"\n[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "Bullet ", txt)

    @staticmethod
    def remove_list_points(txt):
        txt = re.sub(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", txt)
        return re.sub(r"\n[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", txt)

    @staticmethod
    def contains_list_points(txt):
        result = True if re.search(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", txt) else False
        result = True if re.search(r"\n[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", txt) else False
        return result

    @staticmethod
    def clean_up_for_paorgs_getter(txt):
        return txt.replace('−\n', '').replace('-\n', '')\
                  .replace('−', '').replace('-', '').replace('\n', ' ')\
                  .replace(' και ', ' ').replace(' της ', ' ').replace(' του ', ' ').replace(' των ', ' ')\
                  .replace('  ', ' ').replace('   ', ' ')

    @staticmethod
    def append_rows_into_csv(rows, csvfile):
        """ 'rows': list of lists """
        with open(csvfile, "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(rows)

    @staticmethod
    def get_word_n_grams(inpt, n):
        if (type(inpt) is str):
            inpt = inpt.split(' ')
        return [inpt[i:i+n] for i in range(len(inpt) - n + 1)]

    @staticmethod
    def get_clean_words(txt, n=0):
        txt = Helper.clean_up_txt(txt)
        words = re.sub("[^\w]", " ",  txt).split()
        clean_words = Helper.clean_up_word_list(words)
        return clean_words if n<=0 else clean_words[:n]

    @staticmethod
    def get_words(txt, n=0):
        txt = Helper.clean_up_txt(txt)
        words = re.sub("[^\w]", " ",  txt).split()
        return words if n<=0 else words[:n]

    @staticmethod
    def get_greek_stopwords():
        return ["αλλα","αν","αντι","απο","αυτα","αυτεσ","αυτη","αυτο","αυτοι","αυτοσ","αυτουσ","αυτων","αἱ","αἳ","αἵ","αὐτόσ",
                "αὐτὸς","αὖ","γάρ","γα","γα^","γε","για","γοῦν","γὰρ","δ'","δέ","δή","δαί","δαίσ","δαὶ","δαὶς","δε","δεν","δι'",
                "διά","διὰ","δὲ","δὴ","δ’","εαν","ειμαι","ειμαστε","ειναι","εισαι","ειστε","εκεινα","εκεινεσ","εκεινη","εκεινο",
                "εκεινοι","εκεινοσ","εκεινουσ","εκεινων","ενω","επ","επι","εἰ","εἰμί","εἰμὶ","εἰς","εἰσ","εἴ","εἴμι","εἴτε","η",
                "θα","ισωσ","κ","καί","καίτοι","καθ","και","κατ","κατά","κατα","κατὰ","καὶ","κι","κἀν","κἂν","μέν","μή","μήτε",
                "μα","με","μεθ","μετ","μετά","μετα","μετὰ","μη","μην","μἐν","μὲν","μὴ","μὴν","να","ο","οι","ομωσ","οπωσ","οσο",
                "οτι","οἱ","οἳ","οἷς","οὐ","οὐδ","οὐδέ","οὐδείσ","οὐδεὶς","οὐδὲ","οὐδὲν","οὐκ","οὐχ","οὐχὶ","οὓς","οὔτε","οὕτω",
                "οὕτως","οὕτωσ","οὖν","οὗ","οὗτος","οὗτοσ","παρ","παρά","παρα","παρὰ","περί","περὶ","ποια","ποιεσ","ποιο","ποιοι",
                "ποιοσ","ποιουσ","ποιων","ποτε","που","ποῦ","προ","προσ","πρόσ","πρὸ","πρὸς","πως","πωσ","σε","στη","στην","στο",
                "στον","σόσ","σύ","σύν","σὸς","σὺ","σὺν","τά","τήν", "τί","τίς","τίσ","τα","ταῖς","τε","την","τησ","τι","τινα","τις",
                "τισ","το","τοί","τοι","τοιοῦτος","τοιοῦτοσ","τον","τοτε","του","τούσ","τοὺς","τοῖς","τοῦ","των","τό","τόν","τότε",
                "τὰ","τὰς","τὴν","τὸ","τὸν","τῆς","τῆσ","τῇ","τῶν","τῷ","ωσ","ἀλλ'","ἀλλά","ἀλλὰ","ἀλλ’","ἀπ","ἀπό","ἀπὸ","ἀφ","ἂν",
                "ἃ","ἄλλος","ἄλλοσ","ἄν","ἄρα","ἅμα","ἐάν","ἐγώ","ἐγὼ","ἐκ","ἐμόσ","ἐμὸς","ἐν","ἐξ","ἐπί","ἐπεὶ","ἐπὶ","ἐστι","ἐφ",
                "ἐὰν","ἑαυτοῦ","ἔτι","ἡ","ἢ","ἣ","ἤ","ἥ","ἧς","ἵνα","ὁ","ὃ","ὃν","ὃς","ὅ","ὅδε","ὅθεν","ὅπερ","ὅς","ὅσ","ὅστις",
                "ὅστισ","ὅτε","ὅτι","ὑμόσ","ὑπ","ὑπέρ","ὑπό","ὑπὲρ","ὑπὸ","ὡς","ὡσ","ὥς","ὥστε","ὦ","ᾧ", 'στην', 'στη', 'στο', 'στον'
                'στις', 'στους', 'στα', 'υπό', 'από']\
                +\
                [stopwrd.lower() for stopwrd in 
                ["ΑΔΙΑΚΟΠΑ","ΑΙ","ΑΚΟΜΑ","ΑΚΟΜΗ","ΑΚΡΙΒΩΣ","ΑΛΗΘΕΙΑ","ΑΛΗΘΙΝΑ","ΑΛΛΑ","ΑΛΛΑΧΟΥ","ΑΛΛΕΣ","ΑΛΛΗ","ΑΛΛΗΝ","ΑΛΛΗΣ","ΑΛΛΙΩΣ","ΑΛΛΙΩΤΙΚΑ",
                "ΑΛΛΟ","ΑΛΛΟΙ","ΑΛΛΟΙΩΣ","ΑΛΛΟΙΩΤΙΚΑ","ΑΛΛΟΝ","ΑΛΛΟΣ","ΑΛΛΟΤΕ","ΑΛΛΟΥ","ΑΛΛΟΥΣ","ΑΛΛΩΝ","ΑΜΑ","ΑΜΕΣΑ","ΑΜΕΣΩΣ","ΑΝ","ΑΝΑ","ΑΝΑΜΕΣΑ",
                "ΑΝΑΜΕΤΑΞΥ","ΑΝΕΥ","ΑΝΤΙ","ΑΝΤΙΠΕΡΑ","ΑΝΤΙΣ","ΑΝΩ","ΑΝΩΤΕΡΩ","ΑΞΑΦΝΑ","ΑΠ","ΑΠΕΝΑΝΤΙ","ΑΠΟ","ΑΠΟΨΕ","ΑΡΑ","ΑΡΑΓΕ","ΑΡΓΑ","ΑΡΓΟΤΕΡΟ",
                "ΑΡΙΣΤΕΡΑ","ΑΡΚΕΤΑ","ΑΡΧΙΚΑ","ΑΣ","ΑΥΡΙΟ","ΑΥΤΑ","ΑΥΤΕΣ","ΑΥΤΗ","ΑΥΤΗΝ","ΑΥΤΗΣ","ΑΥΤΟ","ΑΥΤΟΙ","ΑΥΤΟΝ","ΑΥΤΟΣ","ΑΥΤΟΥ","ΑΥΤΟΥΣ",
                "ΑΥΤΩΝ","ΑΦΟΤΟΥ","ΑΦΟΥ","ΒΕΒΑΙΑ","ΒΕΒΑΙΟΤΑΤΑ","ΓΙ","ΓΙΑ","ΓΡΗΓΟΡΑ","ΓΥΡΩ","ΔΑ","ΔΕ","ΔΕΙΝΑ","ΔΕΝ","ΔΕΞΙΑ","ΔΗΘΕΝ","ΔΗΛΑΔΗ","ΔΙ",
                "ΔΙΑ","ΔΙΑΡΚΩΣ","ΔΙΚΑ","ΔΙΚΟ","ΔΙΚΟΙ","ΔΙΚΟΣ","ΔΙΚΟΥ","ΔΙΚΟΥΣ","ΔΙΟΛΟΥ","ΔΙΠΛΑ","ΔΙΧΩΣ","ΕΑΝ","ΕΑΥΤΟ","ΕΑΥΤΟΝ","ΕΑΥΤΟΥ","ΕΑΥΤΟΥΣ",
                "ΕΑΥΤΩΝ","ΕΓΚΑΙΡΑ","ΕΓΚΑΙΡΩΣ","ΕΓΩ","ΕΔΩ","ΕΙΔΕΜΗ","ΕΙΘΕ","ΕΙΜΑΙ","ΕΙΜΑΣΤΕ","ΕΙΝΑΙ","ΕΙΣ","ΕΙΣΑΙ","ΕΙΣΑΣΤΕ","ΕΙΣΤΕ","ΕΙΤΕ","ΕΙΧΑ",
                "ΕΙΧΑΜΕ","ΕΙΧΑΝ","ΕΙΧΑΤΕ","ΕΙΧΕ","ΕΙΧΕΣ","ΕΚΑΣΤΑ","ΕΚΑΣΤΕΣ","ΕΚΑΣΤΗ","ΕΚΑΣΤΗΝ","ΕΚΑΣΤΗΣ","ΕΚΑΣΤΟ","ΕΚΑΣΤΟΙ","ΕΚΑΣΤΟΝ","ΕΚΑΣΤΟΣ",
                "ΕΚΑΣΤΟΥ","ΕΚΑΣΤΟΥΣ","ΕΚΑΣΤΩΝ","ΕΚΕΙ","ΕΚΕΙΝΑ","ΕΚΕΙΝΕΣ","ΕΚΕΙΝΗ","ΕΚΕΙΝΗΝ","ΕΚΕΙΝΗΣ","ΕΚΕΙΝΟ","ΕΚΕΙΝΟΙ","ΕΚΕΙΝΟΝ","ΕΚΕΙΝΟΣ",
                "ΕΚΕΙΝΟΥ","ΕΚΕΙΝΟΥΣ","ΕΚΕΙΝΩΝ","ΕΚΤΟΣ","ΕΜΑΣ","ΕΜΕΙΣ","ΕΜΕΝΑ","ΕΜΠΡΟΣ","ΕΝ","ΕΝΑ","ΕΝΑΝ","ΕΝΑΣ","ΕΝΟΣ","ΕΝΤΕΛΩΣ","ΕΝΤΟΣ","ΕΝΤΩΜΕΤΑΞΥ",
                "ΕΝΩ","ΕΞ","ΕΞΑΦΝΑ","ΕΞΗΣ","ΕΞΙΣΟΥ","ΕΞΩ","ΕΠΑΝΩ","ΕΠΕΙΔΗ","ΕΠΕΙΤΑ","ΕΠΙ","ΕΠΙΣΗΣ","ΕΠΟΜΕΝΩΣ","ΕΣΑΣ","ΕΣΕΙΣ","ΕΣΕΝΑ","ΕΣΤΩ","ΕΣΥ",
                "ΕΤΕΡΑ","ΕΤΕΡΑΙ","ΕΤΕΡΑΣ","ΕΤΕΡΕΣ","ΕΤΕΡΗ","ΕΤΕΡΗΣ","ΕΤΕΡΟ","ΕΤΕΡΟΙ","ΕΤΕΡΟΝ","ΕΤΕΡΟΣ","ΕΤΕΡΟΥ","ΕΤΕΡΟΥΣ","ΕΤΕΡΩΝ","ΕΤΟΥΤΑ","ΕΤΟΥΤΕΣ",
                "ΕΤΟΥΤΗ","ΕΤΟΥΤΗΝ","ΕΤΟΥΤΗΣ","ΕΤΟΥΤΟ","ΕΤΟΥΤΟΙ","ΕΤΟΥΤΟΝ","ΕΤΟΥΤΟΣ","ΕΤΟΥΤΟΥ","ΕΤΟΥΤΟΥΣ","ΕΤΟΥΤΩΝ","ΕΤΣΙ","ΕΥΓΕ","ΕΥΘΥΣ","ΕΥΤΥΧΩΣ",
                "ΕΦΕΞΗΣ","ΕΧΕΙ","ΕΧΕΙΣ","ΕΧΕΤΕ","ΕΧΘΕΣ","ΕΧΟΜΕ","ΕΧΟΥΜΕ","ΕΧΟΥΝ","ΕΧΤΕΣ","ΕΧΩ","ΕΩΣ","Η","ΗΔΗ","ΗΜΑΣΤΑΝ","ΗΜΑΣΤΕ","ΗΜΟΥΝ","ΗΣΑΣΤΑΝ",
                "ΗΣΑΣΤΕ","ΗΣΟΥΝ","ΗΤΑΝ","ΗΤΑΝΕ","ΗΤΟΙ","ΗΤΤΟΝ","ΘΑ","Ι","ΙΔΙΑ","ΙΔΙΑΝ","ΙΔΙΑΣ","ΙΔΙΕΣ","ΙΔΙΟ","ΙΔΙΟΙ","ΙΔΙΟΝ","ΙΔΙΟΣ","ΙΔΙΟΥ","ΙΔΙΟΥΣ",
                "ΙΔΙΩΝ","ΙΔΙΩΣ","ΙΙ","ΙΙΙ","ΙΣΑΜΕ","ΙΣΙΑ","ΙΣΩΣ","ΚΑΘΕ","ΚΑΘΕΜΙΑ","ΚΑΘΕΜΙΑΣ","ΚΑΘΕΝΑ","ΚΑΘΕΝΑΣ","ΚΑΘΕΝΟΣ","ΚΑΘΕΤΙ","ΚΑΘΟΛΟΥ","ΚΑΘΩΣ",
                "ΚΑΙ","ΚΑΚΑ","ΚΑΚΩΣ","ΚΑΛΑ","ΚΑΛΩΣ","ΚΑΜΙΑ","ΚΑΜΙΑΝ","ΚΑΜΙΑΣ","ΚΑΜΠΟΣΑ","ΚΑΜΠΟΣΕΣ","ΚΑΜΠΟΣΗ","ΚΑΜΠΟΣΗΝ","ΚΑΜΠΟΣΗΣ","ΚΑΜΠΟΣΟ","ΚΑΜΠΟΣΟΙ",
                "ΚΑΜΠΟΣΟΝ","ΚΑΜΠΟΣΟΣ","ΚΑΜΠΟΣΟΥ","ΚΑΜΠΟΣΟΥΣ","ΚΑΜΠΟΣΩΝ","ΚΑΝΕΙΣ","ΚΑΝΕΝ","ΚΑΝΕΝΑ","ΚΑΝΕΝΑΝ","ΚΑΝΕΝΑΣ","ΚΑΝΕΝΟΣ","ΚΑΠΟΙΑ","ΚΑΠΟΙΑΝ","ΚΑΠΟΙΑΣ",
                "ΚΑΠΟΙΕΣ","ΚΑΠΟΙΟ","ΚΑΠΟΙΟΙ","ΚΑΠΟΙΟΝ","ΚΑΠΟΙΟΣ","ΚΑΠΟΙΟΥ","ΚΑΠΟΙΟΥΣ","ΚΑΠΟΙΩΝ","ΚΑΠΟΤΕ","ΚΑΠΟΥ","ΚΑΠΩΣ","ΚΑΤ","ΚΑΤΑ","ΚΑΤΙ","ΚΑΤΙΤΙ","ΚΑΤΟΠΙΝ",
                "ΚΑΤΩ","ΚΙΟΛΑΣ","ΚΛΠ","ΚΟΝΤΑ","ΚΤΛ","ΚΥΡΙΩΣ","ΛΙΓΑΚΙ","ΛΙΓΟ","ΛΙΓΩΤΕΡΟ","ΛΟΓΩ","ΛΟΙΠΑ","ΛΟΙΠΟΝ","ΜΑ","ΜΑΖΙ","ΜΑΚΑΡΙ","ΜΑΚΡΥΑ","ΜΑΛΙΣΤΑ","ΜΑΛΛΟΝ",
                "ΜΑΣ","ΜΕ","ΜΕΘΑΥΡΙΟ","ΜΕΙΟΝ","ΜΕΛΕΙ","ΜΕΛΛΕΤΑΙ","ΜΕΜΙΑΣ","ΜΕΝ","ΜΕΡΙΚΑ","ΜΕΡΙΚΕΣ","ΜΕΡΙΚΟΙ","ΜΕΡΙΚΟΥΣ","ΜΕΡΙΚΩΝ","ΜΕΣΑ","ΜΕΤ","ΜΕΤΑ","ΜΕΤΑΞΥ",
                "ΜΕΧΡΙ","ΜΗ","ΜΗΔΕ","ΜΗΝ","ΜΗΠΩΣ","ΜΗΤΕ","ΜΙΑ","ΜΙΑΝ","ΜΙΑΣ","ΜΟΛΙΣ","ΜΟΛΟΝΟΤΙ","ΜΟΝΑΧΑ","ΜΟΝΕΣ","ΜΟΝΗ","ΜΟΝΗΝ","ΜΟΝΗΣ","ΜΟΝΟ","ΜΟΝΟΙ","ΜΟΝΟΜΙΑΣ",
                "ΜΟΝΟΣ","ΜΟΝΟΥ","ΜΟΝΟΥΣ","ΜΟΝΩΝ","ΜΟΥ","ΜΠΟΡΕΙ","ΜΠΟΡΟΥΝ","ΜΠΡΑΒΟ","ΜΠΡΟΣ","ΝΑ","ΝΑΙ","ΝΩΡΙΣ","ΞΑΝΑ","ΞΑΦΝΙΚΑ","Ο","ΟΙ","ΟΛΑ","ΟΛΕΣ","ΟΛΗ",
                "ΟΛΗΝ", "ΟΛΗΣ","ΟΛΟ","ΟΛΟΓΥΡΑ","ΟΛΟΙ","ΟΛΟΝ","ΟΛΟΝΕΝ","ΟΛΟΣ","ΟΛΟΤΕΛΑ","ΟΛΟΥ","ΟΛΟΥΣ","ΟΛΩΝ","ΟΛΩΣ","ΟΛΩΣΔΙΟΛΟΥ","ΟΜΩΣ","ΟΠΟΙΑ","ΟΠΟΙΑΔΗΠΟΤΕ",
                "ΟΠΟΙΑΝ","ΟΠΟΙΑΝΔΗΠΟΤΕ", "ΟΠΟΙΑΣ","ΟΠΟΙΑΣΔΗΠΟΤΕ","ΟΠΟΙΔΗΠΟΤΕ","ΟΠΟΙΕΣ","ΟΠΟΙΕΣΔΗΠΟΤΕ","ΟΠΟΙΟ","ΟΠΟΙΟΔΗΠΟΤΕ","ΟΠΟΙΟΙ","ΟΠΟΙΟΝ","ΟΠΟΙΟΝΔΗΠΟΤΕ",
                "ΟΠΟΙΟΣ","ΟΠΟΙΟΣΔΗΠΟΤΕ","ΟΠΟΙΟΥ", "ΟΠΟΙΟΥΔΗΠΟΤΕ","ΟΠΟΙΟΥΣ","ΟΠΟΙΟΥΣΔΗΠΟΤΕ","ΟΠΟΙΩΝ","ΟΠΟΙΩΝΔΗΠΟΤΕ","ΟΠΟΤΕ","ΟΠΟΤΕΔΗΠΟΤΕ","ΟΠΟΥ","ΟΠΟΥΔΗΠΟΤΕ",
                "ΟΠΩΣ","ΟΡΙΣΜΕΝΑ","ΟΡΙΣΜΕΝΕΣ","ΟΡΙΣΜΕΝΩΝ", "ΟΡΙΣΜΕΝΩΣ","ΟΣΑ","ΟΣΑΔΗΠΟΤΕ","ΟΣΕΣ","ΟΣΕΣΔΗΠΟΤΕ","ΟΣΗ","ΟΣΗΔΗΠΟΤΕ","ΟΣΗΝ","ΟΣΗΝΔΗΠΟΤΕ","ΟΣΗΣ",
                "ΟΣΗΣΔΗΠΟΤΕ","ΟΣΟ","ΟΣΟΔΗΠΟΤΕ","ΟΣΟΙ","ΟΣΟΙΔΗΠΟΤΕ","ΟΣΟΝ", "ΟΣΟΝΔΗΠΟΤΕ","ΟΣΟΣ","ΟΣΟΣΔΗΠΟΤΕ","ΟΣΟΥ","ΟΣΟΥΔΗΠΟΤΕ","ΟΣΟΥΣ","ΟΣΟΥΣΔΗΠΟΤΕ","ΟΣΩΝ",
                "ΟΣΩΝΔΗΠΟΤΕ","ΟΤΑΝ","ΟΤΙ","ΟΤΙΔΗΠΟΤΕ","ΟΤΟΥ","ΟΥ","ΟΥΔΕ","ΟΥΤΕ","ΟΧΙ", "ΠΑΛΙ","ΠΑΝΤΟΤΕ","ΠΑΝΤΟΥ","ΠΑΝΤΩΣ","ΠΑΡΑ","ΠΕΡΑ","ΠΕΡΙ","ΠΕΡΙΠΟΥ","ΠΕΡΙΣΣΟΤΕΡΟ",
                "ΠΕΡΣΙ","ΠΕΡΥΣΙ","ΠΙΑ","ΠΙΘΑΝΟΝ","ΠΙΟ","ΠΙΣΩ","ΠΛΑΙ","ΠΛΕΟΝ","ΠΛΗΝ","ΠΟΙΑ", "ΠΟΙΑΝ","ΠΟΙΑΣ","ΠΟΙΕΣ","ΠΟΙΟ","ΠΟΙΟΙ","ΠΟΙΟΝ","ΠΟΙΟΣ","ΠΟΙΟΥ","ΠΟΙΟΥΣ","ΠΟΙΩΝ",
                "ΠΟΛΥ","ΠΟΣΕΣ","ΠΟΣΗ","ΠΟΣΗΝ","ΠΟΣΗΣ","ΠΟΣΟΙ","ΠΟΣΟΣ","ΠΟΣΟΥΣ","ΠΟΤΕ","ΠΟΥ", "ΠΟΥΘΕ","ΠΟΥΘΕΝΑ","ΠΡΕΠΕΙ","ΠΡΙΝ","ΠΡΟ","ΠΡΟΚΕΙΜΕΝΟΥ","ΠΡΟΚΕΙΤΑΙ","ΠΡΟΠΕΡΣΙ",
                "ΠΡΟΣ","ΠΡΟΤΟΥ","ΠΡΟΧΘΕΣ","ΠΡΟΧΤΕΣ","ΠΡΩΤΥΤΕΡΑ","ΠΩΣ","ΣΑΝ","ΣΑΣ","ΣΕ","ΣΕΙΣ","ΣΗΜΕΡΑ", "ΣΙΓΑ","ΣΟΥ","ΣΤΑ","ΣΤΗ","ΣΤΗΝ","ΣΤΗΣ","ΣΤΙΣ","ΣΤΟ","ΣΤΟΝ","ΣΤΟΥ",
                "ΣΤΟΥΣ","ΣΤΩΝ","ΣΥΓΧΡΟΝΩΣ","ΣΥΝ","ΣΥΝΑΜΑ","ΣΥΝΕΠΩΣ","ΣΥΝΗΘΩΣ","ΣΥΧΝΑ","ΣΥΧΝΑΣ","ΣΥΧΝΕΣ","ΣΥΧΝΗ", "ΣΥΧΝΗΝ","ΣΥΧΝΗΣ","ΣΥΧΝΟ","ΣΥΧΝΟΙ","ΣΥΧΝΟΝ","ΣΥΧΝΟΣ","ΣΥΧΝΟΥ",
                "ΣΥΧΝΟΥ","ΣΥΧΝΟΥΣ","ΣΥΧΝΩΝ","ΣΥΧΝΩΣ","ΣΧΕΔΟΝ","ΣΩΣΤΑ","ΤΑ","ΤΑΔΕ","ΤΑΥΤΑ","ΤΑΥΤΕΣ","ΤΑΥΤΗ","ΤΑΥΤΗΝ", "ΤΑΥΤΗΣ","ΤΑΥΤΟ,ΤΑΥΤΟΝ","ΤΑΥΤΟΣ","ΤΑΥΤΟΥ","ΤΑΥΤΩΝ","ΤΑΧΑ",
                "ΤΑΧΑΤΕ","ΤΕΛΙΚΑ","ΤΕΛΙΚΩΣ","ΤΕΣ","ΤΕΤΟΙΑ","ΤΕΤΟΙΑΝ","ΤΕΤΟΙΑΣ","ΤΕΤΟΙΕΣ","ΤΕΤΟΙΟ","ΤΕΤΟΙΟΙ","ΤΕΤΟΙΟΝ", "ΤΕΤΟΙΟΣ","ΤΕΤΟΙΟΥ","ΤΕΤΟΙΟΥΣ","ΤΕΤΟΙΩΝ","ΤΗ","ΤΗΝ","ΤΗΣ",
                "ΤΙ","ΤΙΠΟΤΑ","ΤΙΠΟΤΕ","ΤΙΣ","ΤΟ","ΤΟΙ","ΤΟΝ","ΤΟΣ","ΤΟΣΑ","ΤΟΣΕΣ","ΤΟΣΗ","ΤΟΣΗΝ","ΤΟΣΗΣ","ΤΟΣΟ","ΤΟΣΟΙ", "ΤΟΣΟΝ","ΤΟΣΟΣ","ΤΟΣΟΥ","ΤΟΣΟΥΣ","ΤΟΣΩΝ","ΤΟΤΕ","ΤΟΥ",
                "ΤΟΥΛΑΧΙΣΤΟ","ΤΟΥΛΑΧΙΣΤΟΝ","ΤΟΥΣ","ΤΟΥΤΑ","ΤΟΥΤΕΣ","ΤΟΥΤΗ","ΤΟΥΤΗΝ","ΤΟΥΤΗΣ","ΤΟΥΤΟ","ΤΟΥΤΟΙ","ΤΟΥΤΟΙΣ","ΤΟΥΤΟΝ", "ΤΟΥΤΟΣ","ΤΟΥΤΟΥ","ΤΟΥΤΟΥΣ","ΤΟΥΤΩΝ","ΤΥΧΟΝ",
                "ΤΩΝ","ΤΩΡΑ","ΥΠ","ΥΠΕΡ","ΥΠΟ","ΥΠΟΨΗ","ΥΠΟΨΙΝ","ΥΣΤΕΡΑ","ΦΕΤΟΣ","ΧΑΜΗΛΑ","ΧΘΕΣ","ΧΤΕΣ","ΧΩΡΙΣ","ΧΩΡΙΣΤΑ","ΨΗΛΑ","Ω","ΩΡΑΙΑ", "ΩΣ","ΩΣΑΝ","ΩΣΟΤΟΥ","ΩΣΠΟΥ",
                "ΩΣΤΕ","ΩΣΤΟΣΟ","ΩΧ"] ]
                

    @staticmethod
    def hasNumbers(strng):
        return any(char.isdigit() for char in strng)

    @staticmethod
    def clean_up_word_list(word_list):
        greek_stopwords = Helper.get_greek_stopwords()
        hasNumbers = Helper.hasNumbers
        return [word.lower() for word in word_list 
                                 if not hasNumbers(word) and\
                                    word not in greek_stopwords and\
                                    len(word) > 2]

    @staticmethod
    def get_special_regex_disjunction(key_list):
            regex_disj_str = ''
            for key in key_list:
                key = str(key).replace(' ', '\\s+')
                regex_disj_str += str(key) + '|'
            return regex_disj_str[:-1]

    @staticmethod
    def get_greek_cities():
        return ["Αθήνα", "Πειραιάς", "Θεσσαλονίκη", "Πάτρα", "Ηράκλειο", "Λάρισα", "Βόλος", "Ιωάννινα", "Τρίκαλα", "Χαλκίδα", "Σέρρες", "Αλεξανδρούπολη", 
                "Ξάνθη", "Κατερίνη","Αγρίνιο","Καλαμάτα","Καβάλα","Χανιά","Λαμία","Κομοτηνή","Ρόδος","Δράμα","Βέροια","Κοζάνη","Καρδίτσα","Ρέθυμνο",
                "Πτολεμαΐδα", "Τρίπολη", "Κόρινθος", "Γέρακας", "Γιαννιτσά", "Μυτιλήνη", "Χίος", "Σαλαμίνα", "Ελευσίνα", "Κέρκυρα", "Πύργος", 
                "Μέγαρα", "Κιλκίς", "Θήβα", "Άργος", "Άρτα", "Άρτεμη", "Λούτσα", "Λιβαδειά", "Ωραιόκαστρο", "Αίγιο", "Κως", "Κορωπί", "Πρέβεζα",
                "Σπάρτη", "Νάουσα", "Ορεστιάδα", "Περαία", "Έδεσσα", "Φλώρινα", "Αμαλιάδα", "Παλλήνη", "Θέρμη", "Βάρη", "Νέα Μάκρη", "Αλεξάνδρεια", 
                "Παιανία", "Καλύβια Θορικού", "Ναύπλιο", "Ναύπακτος", "Καστοριά", "Γρεβενά", "Μεσολόγγι", "Γάζι", "Ιεράπετρα", "Κάλυμνος", "Πόθια", 
                "Ραφήνα", "Λουτράκι", "Άγιος Νικόλαος", "Ερμούπολη", "Ιαλυσός", "Μάνδρα", "Τύρναβος", "Γλυκά Νερά", "Άγιος Στέφανος", "Διαβατά", "Κιάτο", 
                "Ανατολή", "Ζάκυνθος", "Αργοστόλι", "Πόρτο Ράφτη", "Μαρκόπουλο", "Νέα Αρτάκη", "Ζεφύρι", "Σητεία", "Νέα Μουδανιά", "Φάρσαλα", "Σίνδος", 
                "Διδυμότειχο", "Σπάτα", "Ηγουμενίτσα", "Επανομή", "Χρυσούπολη", "Νέα Μηχανιώνα", "Λευκάδα", "Νέα Πέραμος", "Καλαμπάκα", "Σάμος", "Αλμυρός", 
                "Κουφάλια", "Γιάννουλη", "Λαγκαδάς", "Μουρνιές", "Κερατέα", "Γαστούνη", "Άργος Ορεστικό", "Ελασσόνα", "Χαλάστρα", "Νέα Καλλικράτεια", "Τρίλοφος", 
                "Δροσιά", "Καρπενήσι", "Μαραθώνας", "Λαύριο", "Νάξος", "Πολύκαστρο", "Λιτόχωρο", "Άμφισσα", "Αίγινα", "Νέο Καρλόβασι", "Κάτω Αχαΐα", "Βασιλικό", 
                "Αριδαία", "Άνοιξη", "Ασβεστοχώρι", "Μοίρες", "Σούδα", "Παραλία Αχαΐας", "Κουνουπιδιανά", "Οβρυά", "Ανάβυσσος", "Θρακομακεδόνες", "Πολύγυρος", 
                "Αμπελώνας", "Αφάντου", "Μεσσήνη", "Νέοι Επιβάτες", "Φιλιατρά", "Λεοντάρι", "Ψαχνά", "Μεγαλόπολη", "Παλαμάς", "Αυλώνας", "Μύρινα", "Διόνυσος", "Σοφάδες", 
                "Νεροκούρος", "Ξυλόκαστρο", "Φίλυρο", "Σιάτιστα", "Φέρες", "Σκύδρα", "Πλαγιάρι", "Αρχάγγελος", "Κρεμαστή", "Βροντάδος", "Τυμπάκι", "Ρίο", "Ορχομενός", 
                "Κρύα Βρύση", "Αγριά", "Μακροχώρι", "Σιδηρόκαστρο", "Νέα Αγχίαλος", "Κυπαρισσία", "Κάρυστος", "Κρυονέρι", "Δροσιά", "Γαργαλιάνοι", "Νιγρίτα",
                "Σκιάθος","Κρέστενα","Ελευθερούπολη","Άγιος Αθανάσιος","Σχηματάρι","Ιτέα","Αμπελάκια","Παροικιά","Βάγια","Γύθειο","Μαραθώνας","Τήνος","Αιτωλικό",
                "Κρανίδι","Αιγίνιο","Σουφλί","Μαλεσίνα","Λεπτοκαρυά","Αλίαρτος","Φιλιππιάδα","Βασιλικά","Πόρος","Γουμένισσα","Νέοι Επιβάτες","Κορινός","Δεσκάτη",
                "Καλοχώρι","Προσοτσάνη","Νεοχώρι","Βόνιτσα","Χαλκηδόνα","Δοξάτο","Ηράκλεια","Μαρκόπουλο","Καλαμπάκι","Κρηνίδες","Σέρβια","Σταυρός","Αξιούπολη","Ορμύλια",
                "Βελεστίνο","Γέφυρα","Λεωνίδιο","Μέτσοβο","Ερέτρια","Νίκαια","Οινόφυτα","Θάσος","Ιερισσός","Βέλο","Ασπροβάλτα","Μολάοι","Κρόκος","Χορτιάτης","Σοχός",
                "Νέα Τρίγλια","Λητή","Κασσάνδρεια","Αλιστράτη","Καλλιθέα","Ανώγεια","Ίασμος","Μεγάλη Παναγία","Λουτρά Αιδηψού","Γαλάτιστα","Χωριστή","Μανιάκοι","Σκούταρι",
                "Ροδολίβος","Ανατολικό","Νέο Σούλι","Νέος Σκοπός","Ύδρα","Δρυμός","Σταμάτα","Νέα Πέραμος","Καναλλάκι","Νικήσιανη","Πρώτη","Παραμυθιά","Νέα Μάλγαρα","Νέα Βρασνά",
                "Νέα Ζίχνη","Νέο Πετρίτσι","Δελφοί","Λαγυνά","Ζαγορά","Κάτω Νευροκόπι","Άγιος Γεώργιος","Δίστομο","Άγιος Βασίλειος","Γυμνό","Χρυσό","Παλαιοκώμη","Αθίκια",
                "Αρχαία Κόρινθος","Ελαιοχώρι" ]

    @staticmethod
    def get_greek_months():
        return {'Ιανουαρίου': 1, 'Φεβρουαρίου': 2, 'Μαρτίου': 3, 'Απριλίου': 4, 'Μαΐου': 5, 'Ιουνίου': 6,
                'Ιουλίου': 7, 'Αυγούστου': 8, 'Σεπτεμβρίου': 9, 'Οκτωβρίου': 10, 'Νοεμβρίου': 11,
                'Δεκεμβρίου': 12, 'Μαίου': 5}

    # @TODO: Add Attica Prefectures
    @staticmethod
    def get_dec_location_and_date_before_signees_regex():
        greek_cities = Helper.get_greek_cities()
        days = range(1,31+1)        
        greek_months = Helper.get_greek_months()
        dec_loc_and_data_pattern = "\s*\n\s*((?:{city}),\s+(?:{day})\s+(?:{month})\s+(?:{year}))\s*\n"\
                                    .format(city=Helper.get_special_regex_disjunction(greek_cities),
                                            day=Helper.get_special_regex_disjunction(days),
                                            month=Helper.get_special_regex_disjunction(greek_months),
                                            year="\d{4}")
        return re.compile(dec_loc_and_data_pattern, flags=re.DOTALL)

    @staticmethod
    def get_greek_intonations():
       return { 'lowercase':{
                                'ά': 'α',
                                'έ': 'ε',
                                'ί': 'ι',
                                'ϊ': 'ι',
                                'ΐ': 'ι',
                                'ό': 'ο',
                                'ύ': 'υ',
                                'ϋ': 'υ',
                                'ΰ': 'υ',
                                'ή': 'η',
                                'ώ': 'ω'
                            },

                'uppercase':{
                                'Ά': 'Α',
                                'Έ': 'Ε',
                                'Ί': 'Ι',
                                'Ϊ': 'Ι',
                                'Ό': 'Ο',
                                'Ύ': 'Υ',
                                'Ϋ': 'Υ',
                                'Ή': 'Η',
                                'Ώ': 'Ω'
                            }
               }       

    @staticmethod
    def make_dir(path, remake_if_exists=False):
        try:
            os.makedirs(path)
        except OSError:
            print(path, ' already exists!')
            if remake_if_exists:
                print('Remaking...')
                shutil.rmtree(path)
                os.makedirs(path)

    @staticmethod
    def deintonate_txt(txt):
        intonations = Helper.get_greek_intonations()
        
        for key, val in intonations['lowercase'].items():
            txt = txt.replace(key, val)

        for key, val in intonations['uppercase'].items():
            txt = txt.replace(key, val)
        
        return txt

    @staticmethod
    def normalize_txt(txt):
        txt = Helper.deintonate_txt(txt)
        return txt.upper()

    # Converts a textual date to a unix timestamp
    @staticmethod
    def date_to_unix_timestamp(date, lang='el'):
        if lang == 'el':
            d = 0
            m = 1
            y = 2
            months = {'Ιανουαρίου': 1, 'Φεβρουαρίου': 2, 'Μαρτίου': 3, 'Απριλίου': 4, 'Μαΐου': 5, 'Ιουνίου': 6,
                      'Ιουλίου': 7, 'Αυγούστου': 8, 'Σεπτεμβρίου': 9, 'Οκτωβρίου': 10, 'Νοεμβρίου': 11,
                      'Δεκεμβρίου': 12, 'Μαίου': 5}
            text_month = False
            separator = " "
            pattern = "Α-ΩΆ-Ώα-ωά-ώ"

        if re.match('[0-9]{1,2} [' + pattern + ']{1,} [0-9]{4,4}', date):
            separator = " "
            text_month = True
        elif re.match('[0-9]{1,2}-[0-9]{1,2}-[0-9]{,4}', date):
            separator = "-"
        elif re.match('[0-9]{1,2}/[0-9]{1,2}/[0-9]{,4}', date):
            separator = "/"
        elif re.match('[0-9]{4,4}', date):
            # Remove non numeric elements from string
            return datetime.datetime(year=int(re.search("^\d{4,4}", date).group(0)), month=1, day=1)
        else:
            return 0
        date = Helper.clear_annotations(date)
        parts = date.split(separator)

        if d < len(parts):
            day = parts[d]
        else:
            day = 1

        if m < len(parts) and text_month:
            month = months[parts[m]]
        elif m < len(parts):
            month = parts[m]
        else:
            month = 1

        if y < len(parts):
            # Remove non numeric elements from string
            year = re.search("^\d{4,4}", parts[y]).group(0)
        else:
            return 0

        return datetime.datetime(year=int(year), month=int(month), day=int(day))

    # Returns a compiled regex object to find dates in text
    @staticmethod
    def date_match(year= 0):

        if not year in Helper.date_patterns:
            operator = str(year) if year != 0 else r"\d{4,4}"
            date_pattern = "\w+,\s?\d{1,2}\s+?\w+\s+" + "{year}".format(year=operator)
            Helper.date_patterns[year] = re.compile(date_pattern)

        return Helper.date_patterns[year]

    # Formats roles extracted from pdfs. Specifically, splits separate words that are stuck together
    @staticmethod
    def format_role(text):
        parts = text.split(" ")

        final_word = ""
        for part in parts:
            split = Helper.camel_case_patteren.sub(r'\1 \2', part).split()

            # If no TitleCase or camelCase was found then we address the possibility of a final s inside a word
            if len(split) == 1:
                split = Helper.final_s_pattern.sub(r'\1 \2', part).split()

            # If no TitleCase or camelCase was found then we address the possibility of a final s inside a word
            if len(split) == 1:
                split = Helper.u_pattern.sub(r'\1 \2', part).split()

            # If no TitleCase or camelCase was found then we address the possibility of a final s inside a word
            if len(split) == 1:
                split = Helper.upper_s_pattern.sub(r'\1 \2', part).split()

            for word in split:
                final_word += word + " "

        # Returns the word without trailing spaces
        return Helper.normalize_greek_name(final_word.strip())

    # Finds all occurences of a substring in a string
    # @return The indexes of all matched substrings.
    @staticmethod
    def find_all(key, string):
        matches = []
        start = 0
        searching = True
        while searching:
            index = string.find(key, start)

            if index == -1:
                searching = False
            else:
                matches.append(index)
                start = index + 1

        return matches

    # Orders a list of dicts by a value inside the dicts
    @staticmethod
    def qsort_by_dict_value(inlist, dict_key):
        if inlist == []:
            return []
        else:
            pivot = inlist[0]
            lesser = Helper.qsort_by_dict_value([x for x in inlist[1:] if x[dict_key] < pivot[dict_key]], dict_key)
            greater = Helper.qsort_by_dict_value([x for x in inlist[1:] if x[dict_key] >= pivot[dict_key]], dict_key)
            return lesser + [pivot] + greater