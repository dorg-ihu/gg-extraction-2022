from fuzzywuzzy import fuzz
from rbner.rbNER import rbNER

article = """Προσόντα διορισμού ή πρόσληψης στο Τμήμα ΠΕ Χημικών. Ορίζεται πτυχίου Χημικού Α.Ε.Ι. της Διεύθυνσης ημεδαπής ή ισότιμο και αντίστοιχο της αλλοδαπής. Μεταπτυχιακός τίτλος σπουδών ανωτάτων εκπαιδευτικών ιδρυμάτων 
            της ημεδαπής ή ισότιμος της αλλοδαπής ενός Ι.Ε.Κ. τουλάχιστον ακαδημαϊκού έτους. Σε θέματα Επιστημών Υγιεινής Περιβάλλοντος ή Περιβαλλοντολογικής Χημείας ή Αναλυτικής Χημείας Περιβάλλοντος. Και η άριστη γνώση μίας 
            τουλάχιστον ξένης γλώσσας."""

gazlist = ["Χημικό", "Επιστημών Υγιεινή Περιβάλλοντος", "Περιβαλλοντολογικής Χημείας", "Υγιεινής Χημείας Περιβάλλοντος", "ημεδαπής Χημείας"]


rbner = rbNER()
candidates = rbner.gazetter_entities(a1)
acro = rbner.acronyms(a1)
print(acro)

regex_ents = rbner.regex_entities(article)
print(regex_ents)
for ele in gazlist:
    print(fuzz.partial_ratio(article, ele))
    
    
nere = rbner.grnlptoolkit(article)
for token in nere.tokens:
    print(token.text, ' - ', token.ner)


from difflib import SequenceMatcher
m = SequenceMatcher(None, "Επιστημών Υγιεινή Περιβάλλοντος", "Επιστημών Υγιεινής Περιβάλλοντος")
print(m.ratio())


# Find acronyms
import re
pattern = r'(?:(?<=\.|\s)[Α-Ω]\.)+'
print(re.findall(pattern, article))


sentences = article.split('.')


# Candidates

candidates1 = re.findall('([Α-Ω][\w-]*(\s+[Α-Ω][\w-]*)+)', article)
candidates2 = re.findall('([Α-Ω][α-ω]+(?=\s[Α-Ω])(?:\s[Α-Ω][α-ω]+)+)', article)
candidates3 = re.findall('([Α-Ω][\w-]*(?:\s+[Α-Ω][\w-]*)+)', article)


re.findall('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)', article)



https://regex101.com/r/DGyVd8/1
https://regex101.com/r/AVfmvz/1


#https://regex101.com/r/YSYsK4/1
https://regex101.com/r/dwS3z3/1

#first comma separated effort
https://regex101.com/r/D16jl8/1


import re
#https://regex101.com/r/i96SWr/1
# Τα καλά
https://regex101.com/r/IP4IcP/1
https://regex101.com/r/kE9YRi/1

regex = r"([Α-ΩΆ-Ώ][\w-]+[\s(και)]*[\sΑ-ΩΆ-Ώ]*)+((?=\s[Α-ΩΆ-Ώ]))(?!\s[\W])(?:\s[Α-Ω][\w-]+)"

test_str = ("Το Τμήμα Πολιτισμού και Οργάνωσης Αυτοδιοίκησης Εχει πολλά καλά. Ένα εξ' αυτών είναι η Ομαδική Προσέγγιση Ζητημάτων. Πρόκειται για μια Υπηρεσία.\n\n"
	"Το Τμήμα Τοπικής Αυτοδιοίκησης και Ενέργειας Καβάλας έχει πολλές ιδιαιτερότητες. Αρχικά, ελέγχει τα Υποτμήματα Ρεύματος και Φυσικού Αερίου.\n\n"
	"Οι υπηρεσίες Δημοσίου Δικαίου αφορούν κυρίως το Υπουργείο Δικαιοσύνης και Αμπαλοσύνης")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
        
        
        
def get_words(txt, n=0):
        #txt = Helper.clean_up_txt(txt)
        words = re.sub("[^\w]", " ",  txt).split()
        return words if n<=0 else words[:n]

def clean_up_txt(txt):
        txt = re.sub('[\t ]+', ' ', txt)
        txt = re.sub('\-[\s]+', '', txt)
        txt = re.sub('\−[\s]+', '', txt)
        return txt.replace("\f", '')

import re
a = "ελα ρε-που εισαι και    τι κανεις σημερα ειναι πεμπτη και αυριο παρασκευη"
print(get_words(a, 5))
print(clean_up_txt(a))


article =  """ΠΡΟΣΟΝΤΑ ΔΙΟΡΙΣΜΟΥ Τα κατά κλάδο και ειδικότητα τυπικά και πρόσθετα 
        προσόντα διορισμού ή πρόσληψης καθορίζονται από τις 
        ισχύουσες κάθε φορά διατάξεις για τον καθορισμό των 
        προσόντων διορισμού ή πρόσληψης σε θέσεις φορέων 
        του δημοσίου τομέα.
        Για τους κλάδους που συγκροτούνται από περισσότερες ειδικότητες, ο αριθμός των θέσεων κατά ειδικότητα καθορίζεται κατά περίπτωση με την προκήρυξη για 
        την πλήρωση των θέσεων του οικείου κλάδου ή με την 
        απόφαση μετάταξης, εάν η θέση πληρούται με μετάταξη.
        Προσόντα διορισμού ή πρόσληψης στον κλάδο ΠΕ 
        Ιατρών ορίζονται τα προβλεπόμενα στις διατάξεις του 
        όπως ισχύει, άδεια άσκησης 
        επαγγέλματος και η εκπλήρωση της υποχρέωσης άσκησης υπηρεσίας υπαίθρου.
        Στις θέσεις του κλάδου Π Ε Ιατρών Δημόσιας Υγείας διορίζονται γιατροί που είναι κάτοχοι τίτλου 
        ειδικότητας κοινωνικής ιατρικής ή ιατρικής εργασίας ή 
        γενικής ιατρικής. Μπορούν επίσης να διορίζονται και γιατροί και οδοντίατροι που να διαθέτουν μεταπτυχιακούς 
        τίτλους σπουδών Ανωτάτων Εκπαιδευτικών Ιδρυμάτων 
        της ημεδαπής ή ισότιμων της αλλοδαπής στον τομέα 
        δημόσιας υγείας της Εθνικής Σχολής Δημόσιας Υγείας, 
        καθώς και της Υγειονομικής Σχολής Αθηνών ή ισότιμης 
        τουλάχιστον Σχολής Δημόσιας Υγείας της αλλοδαπής 
        ή αποδεδειγμένη εμπειρία σε θέματα δημόσιας υγείας 
        τουλάχιστον πέντε (5) ετών.
        Προσόντα διορισμού ή πρόσληψης στον κλάδο ΠΕ 
        Φαρμακοποιών Δημόσιας Υγείας ορίζονται πτυχίο Φαρμακευτικής της ημεδαπής ή ισότιμο και 
        αντίστοιχο της αλλοδαπής και κατά προτεραιότητα μεταπτυχιακός τίτλος σπουδών ανωτάτων εκπαιδευτικών 
        ιδρυμάτων της ημεδαπής ή ισότιμος της αλλοδαπής σε 
        θέματα δημόσιας υγείας ή της Εθνικής Σχολής Δημόσιας Υγείας, καθώς και άδεια άσκησης φαρμακευτικού 
        επαγγέλματος.
        Προσόντα διορισμού ή πρόσληψης στον κλάδο 
        ΠΕ Υγιειονολογων Μηχανικών ορίζονται πτυχίο Μηχανικού της ημεδαπής ή ισότιμο και αντίστοιχο της 
        αλλοδαπής, μεταπτυχιακός τίτλος σπουδών ανωτάτων 
        εκπαιδευτικών ιδρυμάτων της ημεδαπής ή ισότιμος της 
        αλλοδαπής ενός τουλάχιστον ακαδημαϊκού έτους σε 
        θέματα Υγειονομικής Μηχανικής ή Επιστημών Υγιεινής 
        Περιβάλλοντος ανάλογα με τις ανάγκες της υπηρεσίας, 
        άριστη γνώση μίας τουλάχιστον ξένης γλώσσας και άδεια 
        άσκησης επαγγέλματος.
        Προσόντα διορισμού ή πρόσληψης στον κλάδο ΠΕ 
        Μηχανικών Βιοϊατρικής Τεχνολογίας ορίζονται πτυχίο 
        Ηλεκτρολόγου Μηχανικού ή Μηχανολόγου Μηχανικού ή 
        Ηλεκτρονικού Μηχανικού ή Φυσικού της ημεδαπής 
        ή ισότιμο και αντίστοιχο της αλλοδαπής, καθώς και Μεταπτυχιακός τίτλος σπουδών ανωτάτων εκπαιδευτικών 
        ιδρυμάτων της ημεδαπής ή ισότιμος της αλλοδαπής ενός 
        τουλάχιστον ακαδημαϊκού έτους σε θέματα Μηχανικού 
        Βιοϊατρικής ή κλινικού.
        Προσόντα διορισμού ή πρόσληψης στον κλάδο ΠΕ 
        Χημικών ορίζεται πτυχίου Χημικού της ημεδαπής 
        ή ισότιμο και αντίστοιχο της αλλοδαπής, μεταπτυχιακός 
        τίτλος σπουδών ανωτάτων εκπαιδευτικών ιδρυμάτων 
        της ημεδαπής ή ισότιμος της αλλοδαπής ενός τουλάχιστον ακαδημαϊκού έτους σε θέματα Επιστημών Υγιεινής 
        Περιβάλλοντος ή Περιβαλλοντολογικής Χημείας ή Αναλυτικής Χημείας Περιβάλλοντος και η άριστη γνώση μίας 
        τουλάχιστον ξένης γλώσσας."""


unit_keywords = ["ΤΜΗΜΑ", "ΓΡΑΦΕΙΟ ", "ΓΡΑΦΕΙΑ ", "ΑΥΤΟΤΕΛΕΣ ", "ΑΥΤΟΤΕΛΗ ", "ΔΙΕΥΘΥΝΣ", "ΥΠΗΡΕΣΙΑ ", "ΣΥΜΒΟΥΛΙ", "ΓΡΑΜΜΑΤΕIA ", "ΥΠΟΥΡΓ", "ΕΙΔΙΚΟΣ ΛΟΓΑΡΙΑΣΜΟΣ", "MONAΔ", "ΠΕΡΙΦΕΡΕΙ"]


results = rbner.sentences_with_keywords(a1)

for ele in unit_keywords:
    














