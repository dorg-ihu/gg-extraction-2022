from fuzzywuzzy import fuzz
from src.fek_parser import PreParser
from src.respa_extractor import RespExtractor
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import re
import string
from string import digits
import unicodedata as ud

stop = stopwords.words('greek')


def remove_punct_and_digits(x):
    return x.translate(str.maketrans("", "", string.punctuation)).translate(str.maketrans("", "", digits))


# read an issue through PreParser and instantiate the RespExtractor to get access to split articles
filepath = "fek-organismoi-upourgeiwn/yp-ygeias-121-2017.pdf"
text = PreParser().pdf2text(filepath)
textpath = re.sub(r".pdf$", ".txt", filepath)
RSP = RespExtractor(textpath)
articles = RSP.fekParser.articles

article = articles['Άρθρο 11']
d = {ord('\N{COMBINING ACUTE ACCENT}'):None}

article = ud.normalize('NFD',article).upper().translate(d)
article = remove_punct_and_digits(article).replace("\n", "").replace("  ", " ")
articlelist = word_tokenize(article)
articlelist = [x for x in articlelist if len(x) > 1]
final_articlelist = [x for x in articlelist if x.lower() not in stop]


# import gazetter list
path = "rb-ner/gazetter_list.xlsx"
data = pd.read_excel(path)
filtered_data = data[(data["descriptions"] != 'ΑΛΛΟ') & (data["descriptions"] != 'ΓΡΑΦΕΙΟ')].drop_duplicates()
gazlist = filtered_data["preferredLabels"].tolist()
gazlist = [remove_punct_and_digits(x) for x in gazlist]
gazlist = [x.strip().replace("  ", " ") for x in gazlist]
final_gazlist = []
for ele in gazlist:
    tokens = word_tokenize(ele)
    inner = []
    for token in tokens:
        if token.lower() not in stop:
            inner.append(token)
    final_gazlist.append(' '.join(inner))
    
gazlist = [x for x in gazlist for y in word_tokenize(x) if y not in stop]

for ele in final_gazlist:
    length = len(word_tokenize(ele))
    for i in range(len(final_articlelist)):
        parts = final_articlelist[i:i+length]
        article_text = ' '.join(parts)
        ratio = fuzz.ratio(ele, article_text)
        if ratio > 80:
            print(article_text, ' - ', ratio, ' - ', ele)
            break
    
# gazlist = word_tokenize(gazlist)

# # Preprocess the gazetter list
# pp_gazlist = []
# for ele in gazlist:
#     to_append = remove_punct_and_digits(ele).strip().lower()
#     pp_gazlist.append(to_append)
# gazlist = [*set(pp_gazlist)]





# extra_stopwords = ["ως", "εν", "ν", "–", "κλπ", "’", "•", "ΥΕ", "ΠΕ", "ή", "τη", "της", "σημ", "όπως", 
#                    "a", "α", "δ", "β", "ε", "καθώς", "γ", "από", "τους", "ζ", "στ", "λς"]

# stop.extend(extra_stopwords)
# stopwords_dict = Counter(stop)

# clean stopwords, puncutation and numbers
#clean_dups = [" ".join([word if word not in stopwords_dict for text in dups for word in text])]

# Choose the article of interest through key and preprocess it

#TODO remove stopwords
# article = ...


# check the actual score between article and each element on the gazlist

# for ele in gazlist:
#     length = len(ele.split(' '))
#     for i in range(len(article)):
#         parts = article[i:i+length]
#         article_text = ' '.join(parts)
#         ratio = fuzz.ratio(ele, article_text)
#         if ratio > 60:
#             print(ele)
#             break



a1 = """ΠΡΟΣΟΝΤΑ ΔΙΟΡΙΣΜΟΥ 1. Τα κατά κλάδο και ειδικότητα τυπικά και πρόσθετα 
        προσόντα διορισμού ή πρόσληψης καθορίζονται από τις 
        ισχύουσες κάθε φορά διατάξεις για τον καθορισμό των 
        προσόντων διορισμού ή πρόσληψης σε θέσεις φορέων 
        του δημοσίου τομέα.
        2. Για τους κλάδους που συγκροτούνται από περισσότερες ειδικότητες, ο αριθμός των θέσεων κατά ειδικότητα καθορίζεται κατά περίπτωση με την προκήρυξη για 
        την πλήρωση των θέσεων του οικείου κλάδου ή με την 
        απόφαση μετάταξης, εάν η τμήμα πληρούται με μετάταξη.
        3. Προσόντα διορισμού ή πρόσληψης στον κλάδο ΠΕ 
        Ιατρών ορίζονται τα προβλεπόμενα στις διατάξεις του 
        π.δ. 50/2001 (ΦΕΚ Α' 39), όπως ισχύει, άδεια άσκησης 
        επαγγέλματος και η εκπλήρωση της υποχρέωσης άσκησης υπηρεσίας υπαίθρου.
        4. Στις θέσεις του κλάδου Π Ε Ιατρών Δημόσιας Υγείας Ε.Σ.Υ., διορίζονται γιατροί που είναι κάτοχοι τίτλου 
        ειδικότητας κοινωνικής ιατρικής ή ιατρικής εργασίας ή 
        γενικής ιατρικής. Μπορούν επίσης να διορίζονται και γιατροί και οδοντίατροι που να διαθέτουν μεταπτυχιακούς 
        τίτλους σπουδών Ανωτάτων Εκπαιδευτικών Ιδρυμάτων 
        της ημεδαπής ή ισότιμων της αλλοδαπής στον τομέα 
        δημόσιας υγείας της Εθνικής Σχολής Δημόσιας Υγείας, 
        καθώς και της Υγειονομικής Σχολής Αθηνών ή ισότιμης 
        τουλάχιστον Σχολής Δημόσιας Υγείας της αλλοδαπής 
        ή αποδεδειγμένη εμπειρία σε θέματα δημόσιας υγείας 
        τουλάχιστον πέντε (5) ετών.
        5. Προσόντα διορισμού ή πρόσληψης στον κλάδο ΠΕ 
        Φαρμακοποιών Δημόσιας Υγείας Ε.Σ.Υ. ορίζονται πτυχίο Φαρμακευτικής Α.Ε.Ι. της ημεδαπής ή ισότιμο και 
        αντίστοιχο της αλλοδαπής και κατά προτεραιότητα μεταπτυχιακός τίτλος σπουδών ανωτάτων εκπαιδευτικών 
        ιδρυμάτων της ημεδαπής ή ισότιμος της αλλοδαπής σε 
        θέματα δημόσιας υγείας ή της Εθνικής Σχολής Δημόσιας Υγείας, καθώς και άδεια άσκησης φαρμακευτικού 
        επαγγέλματος.
        6. Προσόντα διορισμού ή πρόσληψης στον κλάδο 
        ΠΕ Υγιειονολογων Μηχανικών ορίζονται πτυχίο Μηχανικού Α.Ε.Ι. της ημεδαπής ή ισότιμο και αντίστοιχο της 
        αλλοδαπής, μεταπτυχιακός τίτλος σπουδών ανωτάτων 
        εκπαιδευτικών ιδρυμάτων της ημεδαπής ή ισότιμος της 
        αλλοδαπής ενός τουλάχιστον ακαδημαϊκού έτους σε 
        θέματα Υγειονομικής Μηχανικής ή Επιστημών Υγιεινής 
        Περιβάλλοντος ανάλογα με τις ανάγκες της υπηρεσίας, 
        άριστη γνώση μίας τουλάχιστον ξένης γραφείο και άδεια 
        άσκησης επαγγέλματος.
        7. Προσόντα διορισμού ή πρόσληψης στον κλάδο ΠΕ 
        Μηχανικών Βιοϊατρικής Τεχνολογίας ορίζονται πτυχίο 
        Ηλεκτρολόγου Μηχανικού ή Μηχανολόγου Μηχανικού ή 
        Ηλεκτρονικού Μηχανικού ή Φυσικού Α.Ε.Ι. της ημεδαπής 
        ή ισότιμο και αντίστοιχο της αλλοδαπής, καθώς και Μεταπτυχιακός τίτλος σπουδών ανωτάτων εκπαιδευτικών 
        ιδρυμάτων της ημεδαπής ή ισότιμος της αλλοδαπής ενός 
        τουλάχιστον ακαδημαϊκού έτους σε θέματα Μηχανικού 
        Βιοϊατρικής ή κλινικού.
        8. Προσόντα διορισμού ή πρόσληψης στον κλάδο ΠΕ 
        Χημικών ορίζεται πτυχίου Χημικού Α.Ε.Ι. της ημεδαπής 
        ή ισότιμο και αντίστοιχο της αλλοδαπής, μεταπτυχιακός 
        τίτλος σπουδών ανωτάτων εκπαιδευτικών ιδρυμάτων 
        της ημεδαπής ή ισότιμος της αλλοδαπής ενός τουλάχιστον ακαδημαϊκού έτους σε θέματα Επιστημών Υγιεινής 
        Περιβάλλοντος ή Περιβαλλοντολογικής Χημείας ή Αναλυτικής Χημείας Περιβάλλοντος και η άριστη γνώση μίας 
        τουλάχιστον ξένης γλώσσας."""
