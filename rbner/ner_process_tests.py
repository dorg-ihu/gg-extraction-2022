from fuzzywuzzy import fuzz
from rbner.rbNER import rbNER

article = """Προσόντα διορισμού ή πρόσληψης στο Τμήμα ΠΕ Χημικών. Ορίζεται πτυχίου Χημικού Α.Ε.Ι. της Διεύθυνσης ημεδαπής ή ισότιμο και αντίστοιχο της αλλοδαπής. Μεταπτυχιακός τίτλος σπουδών ανωτάτων εκπαιδευτικών ιδρυμάτων 
            της ημεδαπής ή ισότιμος της αλλοδαπής ενός Ι.Ε.Κ. τουλάχιστον ακαδημαϊκού έτους. Σε θέματα Επιστημών Υγιεινής Περιβάλλοντος ή Περιβαλλοντολογικής Χημείας ή Αναλυτικής Χημείας Περιβάλλοντος. Και η άριστη γνώση μίας 
            τουλάχιστον ξένης γλώσσας."""

gazlist = ["Χημικό", "Επιστημών Υγιεινή Περιβάλλοντος", "Περιβαλλοντολογικής Χημείας", "Υγιεινής Χημείας Περιβάλλοντος", "ημεδαπής Χημείας"]


rbner = rbNER()
candidates = rbner.gazetter_entities(article)
acro = rbner.acronyms(article)

regex_ents = rbner.regex_entities(article)
print(regex_ents)
for ele in gazlist:
    print(fuzz.partial_ratio(article, ele))
    

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
        
        
        
        
