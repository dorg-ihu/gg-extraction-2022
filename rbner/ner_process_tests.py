from fuzzywuzzy import fuzz
from rbner.rbNER import rbNER

article = """Προσόντα διορισμού ή πρόσληψης στο Τμήμα ΠΕ Χημικών. Ορίζεται πτυχίου Χημικού Α.Ε.Ι. της Διεύθυνσης ημεδαπής ή ισότιμο και αντίστοιχο της αλλοδαπής. Μεταπτυχιακός τίτλος σπουδών ανωτάτων εκπαιδευτικών ιδρυμάτων 
            της ημεδαπής ή ισότιμος της αλλοδαπής ενός Ι.Ε.Κ. τουλάχιστον Επιστημών Υγιεινή Περιβάλλοντος Αθήνας ακαδημαϊκού έτους. Σε θέματα Επιστημών Υγιεινής Περιβάλλοντος ή Περιβαλλοντολογικής ΑΣΔ Περιβαλλοντολογικής Χημείας ή Αναλυτικής Χημείας Περιβάλλοντος. Και η άριστη γνώση μίας 
            τουλάχιστον ξένης γλώσσας."""
            
article2 = "Το Διεθνές, Πανεπιστήμιο της Ελλάδος έχει τμήματα σε πολλές πόλεις της Οικονομίας Μακεδονίας και ΒΟρείου Ελλάδος και αποτελεί Κόσμημα για τους φοιτητές του"

text = '''Η διακαής β) (ΚΕ.Σ.Υ.)  ζ) Έλα Μονάδα Εσωτερικού Ελέγχου, Διάρθρωση Υπηρεσιών του Υπουργείου  Το Υπουργείο Υγείας διαρθρώνεται ως εξής: 1. Πολιτικά Γραφεία Υπουργού και Υφυπουργών και  Γραφεία Γενικών Γραμματέων  2. Υπηρεσίες, Διευθύνσεις και Τμήματα υπαγόμενα απ’  ευθείας στον Υπουργό:  α) Σώμα Επιθεωρητών Υπηρεσιών Υγείας (Σ.Ε.Υ.Υ.)  (ν. 2920/2001 − Α΄ 131)  5. Το π.δ. 89/2014 «Διορισμός Υπουργών, Αναπληρωτών  β) Εθνικό Κέντρο Επιχειρήσεων Υγείας (ν. 3370/2006  Υπουργών και Υφυπουργών» (Α΄ 134).  − Α΄ 176)     γ) Διεύθυνση Ευρωπαϊκής και Διεθνούς Πολιτικής Υγείας δ) Μονάδα Διαμόρφωσης Πολιτικών Υγείας και Τουρισμού Υγείας, η οποία λειτουργεί σε επίπεδο τμήματος ε) Τμήμα Νομοθετικής Πρωτοβουλίας, Κοινοβουλευτικού Ελέγχου και Κωδικοποίησης  στ) Διεύθυνση Επιστημονικής Τεκμηρίωσης, Διοικητικής και Γραμματειακής Υποστήριξης του Κεντρικού Συμβουλίου Υγείας (ΚΕ.Σ.Υ.)  ζ) Μονάδα Εσωτερικού Ελέγχου , η οποία λειτουργεί σε  επίπεδο τμήματος'''

gazlist = ["Χημικό", "Επιστημών Υγιεινή Περιβάλλοντος Θεσσαλονίκης", "Μονάδα Εσωτερικού Ελέγχου", "Διάρθρωση Υπηρεσίας", "ημεδαπής Χημείας"]


rbner = rbNER()

reEntities = rbner.regex_entities(article17)
print(reEntities)

for ent in reEntities:
    print(ent, ' - ', rbner.gazetter_entities(ent))
    print("##"*5)
  

for ent in reEntities:
    print(ent, ' - ', rbner.gazetter_entities_R(ent, False))
    print("##"*5)

    
candidates = rbner.gazetter_entities(a1)
acro = rbner.acronyms(a1)
print(acro)

regex_ents = rbner.regex_entities(article)
print(regex_ents)
for ele in gazlist:
    print(fuzz.partial_ratio(text, ele))
    
    
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


article17 = """ ΔΙΑΡΘΡΩΣΗ-ΑΡΜΟΔΙΟΤΗΤΕΣ
ΔΙΕΥΘΥΝΣΗΣ ΨΥΧΙΚΗΣ ΥΓΕΙΑΣ
1. Η Διεύθυνση Ψυχικής Υγείας έχει ως σκοπό το σχεδιασμό και την εφαρμογή του Προγράμματος Ψυχιατρικής Μεταρρύθμισης «ΨΥΧΑΡΓΩΣ», το οποίο αποτελεί 
το Εθνικό Σχέδιο για την αλλαγή του τρόπου παροχής 
Υπηρεσιών Ψυχικής Υγείας, με μετάθεση του κέντρου 
βάρους από την παρεχόμενη ασυλικού τύπου περίθαλψη, στην κοινοτική φροντίδα.
2. Τη Διεύθυνση (Γ3) συγκροτούν τα ακόλουθα Τμήματα:
α. Τμήμα (Γ3α) Νοσοκομειακής και Κοινοτικής Περίθαλψης
β. Τμήμα (Γ3β) Εξωνοσοκομειακής Προστασίας
3. Οι αρμοδιότητες της Διεύθυνσης είναι οι ακόλουθες 
και κατανέμονται μεταξύ των Τμημάτων της ως εξής:
 α. Τμήμα Νοσοκομειακής και Κοινοτικής Περίθαλψης
1. Ο προγραμματισμός και η εξειδίκευση της εθνικής 
στρατηγικής και του επιχειρησιακού σχεδιασμού στον 
τομέα της ψυχικής υγείας, σε συνεργασία με τη Διεύθυνση Στρατηγικού Σχεδιασμού.
2. Η εφαρμογή προγραμμάτων προαγωγής της ψυχικής υγείας και πρόληψης των ψυχικών διαταραχών.
3. Η προαγωγή και υποστήριξη της κατανομής σε τομείς και η εποπτεία, διασύνδεση και διαβούλευση των 
Μονάδων Ψυχικής Υγείας, που λειτουργούν ως Νομικά 
Πρόσωπα Δημοσίου Δικαίου (Ν.Π.Δ.Δ) με τις Περιφερειακές Διοικήσεις Τομέων Ψυχικής Υγείας (Πε.Δι.Το.Ψ.Υ.).
4. Η μέριμνα για την εναρμόνιση των πολιτικών ψυχικής υγείας και του οικείου νομοθετικού και κανονιστικού πλαισίου, με τις Διεθνείς Συμβάσεις, Κανονισμούς, 
συστάσεις, οδηγίες του Παγκόσμιου Οργανισμού Υγείας 
και της Ευρωπαϊκής Ένωσης και η παρακολούθηση της 
εφαρμογής τους.
5. Η παρακολούθηση της αποασυλοποίησης ασθενών 
με ψυχικές διαταραχές των Ψυχιατρικών Νοσοκομείων 
και των εποπτευομένων από το Τμήμα Μονάδων Ψυχικής Υγείας.
6. Ο προγραμματισμός ίδρυσης και ανάπτυξης Ψυχιατρικών Νοσοκομειακών Ε.Σ.Υ ή τμημάτων αυτών, 
Ψυχιατρικών Τομέων Γενικών Νοσοκομείων Ε.Σ.Υ, σε 
συνεργασία με τις συναρμόδιες Υπηρεσίες και τους 
εποπτευόμενους Φορείς.
7. Η εποπτεία των Ψυχιατρικών Νοσοκομείων του 
Ε.Σ.Υ. και όλων των υπαγομένων σε αυτά Μονάδων Ψυχικής Υγείας, καθώς και των Τομέων και των Μονάδων 
Ψυχικής Υγείας των Γενικών Νοσοκομείων του Ε.Σ.Υ.
8. Η εισήγηση προς την Διεύθυνση Οργάνωσης και 
Λειτουργίας Νοσηλευτικών Μονάδων και Εποπτευόμενων Φορέων για την σύσταση, μεταφορά, κατάργηση, 
συγχώνευση Ψυχιατρικών Νοσοκομείων ή Τμημάτων 
αυτών, καθώς και θέσεων:
i. Ιατρών Ε.Σ.Υ, ii. ειδικευομένων Ιατρών, iii. εξειδικευμένων Ιατρών και iν. επιστημονικού και λοιπού προσωπικού.
9. Η μέριμνα για την έκδοση και εφαρμογή του Ενιαίου Πλαισίου Οργάνωσης και Λειτουργίας των Μονάδων 
Ψυχικής Υγείας που λειτουργούν με τη μορφή ΝΠΔΔ και 
ο προσδιορισμός της λειτουργικής διασύνδεσης τους, 
σε συνεργασία με τις συναρμόδιες Υπηρεσίες και τους 
εποπτευόμενους Φορείς.
10. Η εισήγηση για την έγκριση σύστασης Ιδρυμάτων 
και μετατροπής των καταστατικών τους στο σκοπό των 
οποίων περιλαμβάνεται η παροχή υπηρεσιών ψυχικής 
υγείας.
11. Η εισήγηση για τον καθορισμό και η έκδοση των 
νοσηλίων για τις Μονάδες Ψυχικής Υγείας, που λειτουργούν με τη μορφή Ν.Π.Δ.Δ και η κοστολόγηση των ιατρικών πράξεων και των παρεχόμενων υπηρεσιών ψυχικής 
υγείας.
12. Η εισήγηση για τον καθορισμό των δικαιούχωνατόμων με ψυχικές διαταραχές που τους παρέχεται δωρεάν νοσηλεία και περίθαλψη.
13. Η άσκηση εποπτείας και ελέγχου και η εισήγηση για 
την ρύθμιση των διαδικασιών λειτουργίας των ιδιωτικών 
κλινικών ψυχικής υγείας.
14. Η μέριμνα για την προαγωγή της εργασιακής ένταξης των ατόμων με ψυχικές διαταραχές των Μονάδων 
Ψυχικής Υγείας των Ψυχιατρικών Νοσοκομείων και των 
Ψυχιατρικών Τομέων των Γενικών Νοσοκομείων Ε.Σ.Υ.
β. Τμήμα Εξωνοσοκομειακής Προστασίας
1. Η μέριμνα για τον προγραμματισμό και την εξειδίκευση της εθνικής στρατηγικής και του επιχειρησιακού 
σχεδιασμού στον τομέα της ψυχικής υγείας σε συνεργασία με την Διεύθυνση Στρατηγικού Σχεδιασμού.
2. Η προαγωγή και υποστήριξη της κατανομής σε τομείς και η εποπτεία, διασύνδεση και διαβούλευση των 
Μονάδων Ψυχικής Υγείας, που λειτουργούν ως Νομικά 
Πρόσωπα Ιδιωτικού Δικαίου (Ν.Π.Ι.Δ) με τις Περιφερειακές Διοικήσεις Τομέων Ψυχικής Υγείας (Πε.Δι.Το.Ψ.Υ.).
3. Η μέριμνα για την εναρμόνιση των πολιτικών ψυχικής υγείας και του οικείου νομοθετικού και κανονιστικού πλαισίου, με τις Διεθνείς Συμβάσεις, Κανονισμούς, 
Συστάσεις, Οδηγίες του Παγκόσμιου Οργανισμού Υγείας 
και της Ευρωπαϊκής Ένωσης και η παρακολούθηση της 
εφαρμογής τους.
4. Η άσκηση της εποπτείας και του ελέγχου των Μονάδων Ψυχικής Υγείας του ιδιωτικού μη κερδοσκοπικού 
τομέα.
5. Η επεξεργασία και εφαρμογή εξειδικευμένων προγραμμάτων παροχής υπηρεσιών ψυχικής υγείας σε 
ευπαθείς ομάδες και πληθυσμιακές και διαγνωστικές 
υποομάδες με προβλήματα ψυχικής υγείας.
6. Η μέριμνα για την εκπόνηση και έκδοση Ενιαίου 
Πλαισίου Οργάνωσης και Λειτουργίας των Μονάδων Ψυχικής Υγείας, που λειτουργούν με τη μορφή Ν.Π.Ι.Δ., και 
ο προσδιορισμός της λειτουργικής διασύνδεσής τους, 
σε συνεργασία με τις συναρμόδιες Υπηρεσίες και τους 
εποπτευόμενους Φορείς.
7. Η εισήγηση για τη ρύθμιση των όρων και προϋποθέσεων παροχής ιατροφαρμακευτικής, νοσηλευτικής ή 
νοσοκομειακής περίθαλψης και υπηρεσιών ψυχοκοινωνικής αποκατάστασης.
8. Η εισήγηση για τον καθορισμό και η έκδοση των νοσηλίων για τις Μονάδες Ψυχικής Υγείας που λειτουργούν 
με τη μορφή Ν.Π.Ι.Δ, σε συνεργασία με τις συναρμόδιες 
Υπηρεσίες και Φορείς, και η κοστολόγηση των ιατρικών 
πράξεων και των παρεχόμενων υπηρεσιών.
9. Η μέριμνα για τον προγραμματισμό και την ανάπτυξη Μονάδων Ψυχικής Υγείας του ιδιωτικού μη κερδοσκοπικού τομέα, σε συνεργασία με τη Διεύθυνση 
Στρατηγικού Σχεδιασμού.
10. Η οικονομική αξιολόγηση και ο οικονομικός έλεγχος των Μονάδων Ψυχικής Υγείας του ιδιωτικού μη κερδοσκοπικού τομέα.
11. Η μέριμνα για την προαγωγή της εργασιακής 
ένταξης των ατόμων με ψυχικές διαταραχές, για την 
καταπολέμηση των διακρίσεων και την προώθηση των 
απαραίτητων θεσμικών παρεμβάσεων. """

#%%
from src import dictionaries as dc


def remove_first_level(txt):
    first_line, rest_lines = txt.split("\n", 1)[0], "\n" + txt.split("\n", 1)[1]
    first_line = re.sub(r"^[ ]*[α-ωΑ-Ω0-9]+[\.\)] ", "", first_line)
    return first_line + rest_lines


def get_paragraph_levels(items):
    levels = []
    for i, item in enumerate(items):
        if item in dc.alphabet:
            levels.append((item, "alphabet"))  # alphabet
        elif item in dc.ab_double_combs:
            levels.append((item, "abcombinations"))  # ab combinations
        elif item in dc.latin_numbers:
            levels.append((item, "latinnumbers"))  # latin numbers
        elif item in dc.numbers:
            levels.append((item, "therest"))  #
    return levels


def find_levels_depth(txt):
    split_all = FPRS.split_all_int(txt)
    split_all = [x for x in split_all if isinstance(x, tuple)]

    split_all = {k:v for k,v in split_all}
    pointers_list = list(split_all.keys())
    
    levels = get_paragraph_levels(pointers_list)
    depth = 1
    type_of_levels = {levels[0][1]: depth}
    info = [levels[0] + (depth,) + (split_all[levels[0][0]],)]  
    for idx, (key, tag) in enumerate(levels[1:]):
        if tag not in type_of_levels:
            depth += 1
            type_of_levels[tag] = depth
            info.append((key, tag) + (depth,) + (split_all[key],))
        else:
            cur_depth = type_of_levels[tag]
            info.append((key, tag) + (cur_depth,) + (split_all[key],))
    
    # reconstructs the flat list of points into groups under the depth = 1
    split_points = [i for i, (point, typ, dep, text) in enumerate(info) if dep == 1]
    total_split = split_points + [len(info)]
    grouped_info = [info[i:j] for i, j in zip(split_points, total_split[1:])]

    return grouped_info, len(type_of_levels)


#%% libraries and initialization of objects (common for both tasks)

import time
start_time = time.time()

#from src.respa_extractor import RespExtractor
from rbner.rbNER import rbNER
rbner = rbNER()
#import random

from rbner.respas import respas
from src.fek_parser import PreParser, FekParser
from rbner.structure import structure
import re
from collections import OrderedDict

from src.rb_respas_tool import respas



"""give a filepath (in .pdf form)"""
filepath = "fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"

# filepath = "fek-organismoi-upourgeiwn/yp-ygeias-121-2017.pdf"

#filepath = "fek-organismoi-upourgeiwn/yp-tourismou-127-2017.pdf"
#filepath = "fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf"
#filepath = "fek-organismoi-upourgeiwn/yp-ypodomwnkaimetaforwn-123-2017.pdf"
#filepath = "fek-organismoi-upourgeiwn/yp-oikonomikwn-142-2017.pdf"

"""initialize PreParser that produces a .txt file on working directory"""
text = PreParser().pdf2text(filepath)

"""change the filename extenstion to .txt"""
textpath = re.sub(r".pdf$", ".txt", filepath)
FPRS, RSP = FekParser(textpath), respas(textpath)
"""initialize the objects for relation and responsibilities extraction"""
FPRS, STR, RSP = FekParser(textpath), structure(textpath), respas(textpath)


"""get articles on the given text"""
articles = FPRS.articles

#%% relations extraction
relations_list = []
for AR_key, AR_value in articles.items():
    try:
        article_paragraphs = FPRS.find_article_paragraphs(AR_value)
        if len(article_paragraphs) > 1:
            possible_title = article_paragraphs["0"]
            if any(title_kw in possible_title for title_kw in STR.irrelevant_title):
                print("Article {} has been skipped due to irrelevant_title".format(AR_key))
                continue
        
        master_unit, relation_paragraphs = STR.get_candidate_paragraphs_per_article(article_paragraphs) # returns which paragraphs meet the STRUCTURE requirements
        relations = STR.get_relations(master_unit, relation_paragraphs)
        relations_list.append(relations)
        print("Article {} has been processed".format(AR_key))
    except Exception as e:
        print("Article {} resulted in error".format(AR_key))
        pass

final_list = [x for x in relations_list if x]


"""create a graph given the resulted tuples"""
processed_relations = []
for lst in final_list:
    tuplist = []
    for (x,y) in lst:
        newvalue = rbner.remove_intonations(y).replace("\n", "").strip()
        tuplist.append((x, newvalue))
    processed_relations.append(tuplist)

# for lst in processed_relations:
#     for tup in lst:
#         print(tup)
# processed_relations = [rbner.remove_intonations(t2) for x in final_list for (t1, t2) in x]

graph = STR.get_relations_graph(processed_relations)
# processed_relations.insert(0, [("ΓΕΝΙΚΗ ΔΙΕΥΘΥΝΣΗ ΤΕΣΤΑΡΙΣΜΑΤΟΣ", "ΔΙΕΥΘΥΝΣΗ ΕΥΡΩΠΑΪΚΗΣ ΚΑΙ ΔΙΕΘΝΟΥΣ ΣΥΝΕΡΓΑΣΙΑΣ"), ("ΓΕΝΙΚΗ ΔΙΕΥΘΥΝΣΗ ΤΕΣΤΑΡΙΣΜΑΤΟΣ", "ΔΙΕΥΘΥΝΣΗ ΥΠΟΔΟΜΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΕΠΙΚΟΙΝΩΝΙΩΝ")])

print("Execution time {}".format(time.time() - start_time))

#%% responsibilities extraction
responsibilities_dict = OrderedDict()
for AR_key, AR_value in articles.items():
    try:
        article_paragraphs = FPRS.find_article_paragraphs(AR_value)
        if len(article_paragraphs) > 1:
            possible_title = article_paragraphs["0"]
            if any(title_kw in possible_title for title_kw in RSP.irrelevant_title):
                print("Article {} has been skipped due to irrelevant_title".format(AR_key))
                continue

        master_unit, responsibility_paragraphs = RSP.get_candidate_paragraphs_per_article(article_paragraphs) #input article text - output list of candidate paragraphs

        responsibilities = RSP.get_respas(master_unit, responsibility_paragraphs) # input list of candidate paragraphs - ouput dictionary with unit-respa pairs
        if responsibilities:
            responsibilities_dict[AR_key] = responsibilities
            print("We found {} pairs of responsibilities on Article {} has been processed".format(len(responsibilities), AR_key))
        
    except Exception as e:
        print("Article {} resulted in error".format(AR_key))
        pass

# final_list = [x for x in responsibilities_list if x]

#%%

article17 = articles["Άρθρο 17"]
paragraphs = FPRS.find_article_paragraphs(article17)
paragraphs_list = list(paragraphs.values())
# paragraph3 = paragraphs["3"]
paragraphs_list = [paragraphs_list.pop(-2)]

respas = RSP.get_respas(paragraphs_list)


new_par3 = remove_first_level(paragraph3)

respas = RSP.get_respas(new_par3)

results = find_levels_depth(new_par3)

if len(paragraphs) > 1:
    potential_title = paragraphs["0"]
print(potential_title)
#%%











