import re
import numpy as np
from gm3.gm3.helpers import *
import string
from collections import Iterable



class Action:

    def __init__(self, name, lemma, derivatives=[], weight_vector=None):
        self.name = name
        self.lemma = lemma
        self.derivatives = derivatives
        self.derivatives.append(name)
        if weight_vector is None:
            self.weight_vector = (1 / (len(self.derivatives))) * \
                np.ones(len(self.derivatives))
        else:
            self.weight_vector = weight_vector

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def score(self, word, _normalize_word=True):
        scores = np.zeros(len(self.derivatives))
        for i, derivative in enumerate(self.derivatives):
            scores[i] = edit_distance(
                word if not _normalize_word else normalize_word(word), derivative)
        return np.dot(scores, self.weight_vector)

    def __eq__(self, q):
        w = q.lower()
        return w == self.name or w in self.derivatives or w == self.name.capitalize(
        ) or w in list(map(lambda s: s.capitalize(), self.derivatives))


# Actions
actions = [
    Action(
        'προστίθεται', 'add', [
            'προσθέτουμε', 'προσθήκη', 'προστίθενται']), Action(
                'διαγράφεται', 'delete', [
                    'διαγράφουμε', 'διαγραφή', 'διαγράφονται', 'καταργείται', 'καταργούνται', 'απαλείφεται', 'απαλείφονται']), Action(
                        'παύεται', 'terminate', [
                            'παύση', 'παύουμε', 'παύονται']), Action(
                                'τροποποιείται', 'amend', [
                                    'τροποποίηση', 'τροποποιούμε', 'τροποποιούνται']), Action(
                                        'αντικαθίσταται', 'replace', [
                                            'αντικαθίσταται', 'αντικατάσταση', 'αντικαθίστανται']), Action(
                                                'αναριθμείται', 'renumber', [
                                                    'αναριθμείται', 'αναριθμούνται'])]

# Entities - Statutes
whats = [
    'φράση',
    'παράγραφος',
    'άρθρο',
    'εδάφιο',
    'φράσεις',
    'άρθρα',
    'εδάφια',
    'παράγραφοι',
    'τίτλος',
    'τίτλοι',
    'περίπτωση',
    'περιπτώσεις',
    'υποπερίπτωση',
    'υποπεριπτώσεις',
    'λέξη',
    'λέξεις'
]

what_stems = [
    'παράγραφ',
    'άρθρ',
    'εδάφι',
    'τίτλ',
    'υποπεριπτώσ',
    'περίπτωσ'
]

wheres = ['Στο', 'στο', 'Στην', 'στην', 'στον', 'Στον']


law_regex = r'(ν.|Ν.) [0-9][0-9][0-9][0-9]/[1-2][0-9][0-9][0-9]'
legislative_decree_regex = r'(ν.δ.|Ν.Δ.) ([0-9]|[0-9][0-9]|[0-9][0-9][0-9])/[1-2][0-9][0-9][0-9]'
presidential_decree_regex = r'(π.δ.|Π.Δ.) ([0-9]|[0-9][0-9]|[0-9][0-9][0-9])/[1-2][0-9][0-9][0-9]'
date_regex = re.compile('(\
([1-9]|0[1-9]|[12][0-9]|3[01])\
[-/.\s+]\
(1[1-2]|0[1-9]|[1-9]|Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Ιουνίου|Ιουλίου|Αυγούστου|Νοεμβρίου|Δεκεμβρίου|Σεπτεμβρίου|Οκτωβρίου|Ιαν|Φεβ|Μαρ|Απρ|Μαϊ|Ιουν|Ιουλ|Αυγ|Σεπτ|Οκτ|Νοε|Δεκ)\
(?:[-/.\s+](1[0-9]\d\d|20[0-9][0-8]))?)')
legislative_act_regex = r'Πράξη(|ς) Νομοθετικού Περιεχομένου ([0-9]|[0-3][0-9]).[0-9][0-9].[1-2][0-9][0-9][0-9]'
article_regex = ['άρθρο \d+', 'άρθρου \d+']
paragraph_regex = [
    'παράγραφος \d+',
    'παραγράφου \d+',
    'παρ. \d+',
    'παράγραφος']

plural_suffixes = [
    'οι',
    'α',
    'εις',
    'οι',
    'ες',
    'ων',
    'ους'
]

conditions = ['Εκτός αν', ' αν ', 'προϋπόθεση', 'κατά περίπτωση', 'εφόσον', 'εάν',
              'ανεξαρτήτως εάν', 'είναι δυνατόν να', 'τις προϋποθέσεις', 'μόνο εφόσον', 'μετά από', 'ενέχει']

constraints = ['εν όλω', 'εν μέρει', 'αρκεί', 'εκτός από',
               'πρέπει να', 'πλην', 'τουλάχιστον', 'μέχρι', 'το πολύ', 'εκτός', 'λιγότερο από']

durations = ['επί', 'μέσα στον μήνα', 'μέσα σε', 'εντός ',
             'μέχρι της ίδιας αυτής ημερομηνίας', 'προθεσμία',  'το αργότερο εντός']


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x

def get_conditions(text):

    # Conditions
    cond = []
    cond.append(re.findall('|'.join(x for x in conditions), text))

    return(list(flatten(cond)))
         
def get_constraints(text):

    # Constrains
    const = []
    const.append(re.findall('|'.join(x for x in constraints), text))

    return(list(flatten(const)))
         
def get_durations(text):

    # Durations
    dur = []
    dur.append(re.findall('|'.join(x for x in durations), text))

    return(list(flatten(dur)))


# URLS
urls = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

# CPC codes
cpc = r'CPC .+[0-9]'

# CPV codes
cpv = r'[0-9]{8}-[0-9]'

# IBAN
ibans = r'[A-Z]{2}[ ]?[0-9]{2}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{3}'

# E-mail adresses
e_mails = r'[\w\.-]+@[\w\.-]+'

# ID numbers
id_numbers = r'Α.?Δ.?Τ.?:? ([Α-Ωα-ω]{0,2}[- ]?[0-9]{6})'

# Military personnel IDs
military_personel_id = r'ΣΑ [0-9]{3}/[0-9]{3}/[0-9]{2}'

# Scales
scales = r'1:[0-9]{1,10}'

# Natura 2000 regions
natura_regions = r'GR[0-9]{7}'

# Wildlife sanctuaries
wildlife_sanctuaries = r'Καταφύγιο Άγριας Ζωής ([Α-ΩA-Z0-9]+)'

# EU directives
directives_eu = r'[Οο]δηγίας? ([0-9]+/[0-9]+/[Α-Ω]{2,4})'

# EU regulations
regulations_eu = r'[Κκ]ανονισμ[όούς]{1, 2}[Α-Ω)(]*[αριθ.] * ([0-9]{1, 5}/[0-9]{4})'

# EU decisions
decisions_eu = r'[Αα]πόφασης?[Α-Ω )(]*[ αριθ.]* ([1-9][0-9]{3}/[0-9]{1,5}/[Α-Ω]{2,3})'

# Academic year
ac_year = r'ακαδημαϊκό έτος ([1-9][0-9]{3}-[1-9][0-9]{3})'

# Greek zip codes
zip_codes = r'ΤΚ: ([0-9]{3} [0-9]{2})'

# Act of deletion from the Public HR registry
del_from_registry = r'Αριθ. βεβ. διαγραφής από το Μητρώο Ανθρώπινου Δυναμικού Ελληνικού Δημοσίου: ([0-9]{10}/[0-9]{2}.[0-9]{2}.[0-9]{4})'

# Act of inscription to the Public HR registry
ins_to_registry = r'Αριθμ. βεβ. εγγραφής στο Μητρώο Ανθρώπινου Δυναμικού Ελληνικού Δημοσίου: ([0-9]{10}/[0-9]{2}.[0-9]{2}.[0-9]{4})'

# ADA numbers for DIAUGEIA
adas = r'Α.?Δ.?Α.?:? ([Α-Ω0-9]{4,10}-[Α-Ω0-9]{3})'

# Ολοκληρωμένο Πληροφοριακό Σύστημα (ΟΠΣ) code
ops = r'Ο.?Π.?Σ.?:? ([0-9]+)'

# ISO and ELOT protocols
protocols = r'πρότυπο ([Α-ΩA-Z]{2,4} [Α-ΩA-Z]{2,4} [0-9:-]+|[Α-ΩA-Z]{2,4} [0-9:-]+)'

# Αριθμός Φορολογικού Μητρώου (Α.Φ.Μ.)- Tax Registry number
afm = r'Α.?Φ.?Μ.?:? ([0-9]{9})'

# NUTS regions
nuts_reg = r'NUTS:? ([A-Z]{2}[0-9]{1,3})'

# Exact times
exact_times = r'[0-9]{2}:[0-9]{2} [πμ].μ.|[0-9]{2}:[0-9]{2}'

# Ship tonnage in register tons
tonnage = r'[-+]?[.]?[\d]+[-+]?[.]?[\d]+(?:,\d\d)* κόρ[οιωv]{2}'

# KAEK Κωδικός Αριθμό Eθνικού Kτηματολογίου
kaek = r'ΚΑΕΚ[- ]?[0-9/]{12}'

# Number regex
number_regex = r'[.\d]?[.]?[\d]+[.]?[\d]+(?:[,.]\d\d)*[ ]?'

# Phone numbers
phone_numbers = r'[+03]{0,4} 2[1-8][0-9][ -]?[0-9]{7}|[+03]{0,4} 2[1-8][0-9]{3}[ -]?[0-9]{6}'

# HULL number - Ship ID
hull = r'HULL No ([A-Z0-9]{1,17}|[A-Z]{1,2}[- ]?[A-Z0-9]{1,17})'

# Ship flag
flag = r'\W σημαία|σημαία \W'




meters = r'm |μ\.?[ \.)]|μέτρ[ωνα]{1,2}'
kilometers = r'km|χλμ.?|χιλι[όο]μ[εέ]τρ[ωνα]'
liters = r'[Λλ]ίτρ[ωνα]{1,2}|[LIl]t|ml'
surface = r'μ2|τετραγωνικών μέτρ[ωνα]{1,2}|τ[.]?μ[.]?|στρ[εέ]μμ[άα]τ[ωνα]{1,2}|στρ.?|τετρ. μέτρ[ωνα]{1,2}'
power = r'[Kk][wW]'
kgr = r'[Kk]g[r]?'

class Unit:
    units = [
         meters,
         kilometers,
         liters,
         surface,
         power,
         kgr
    ]

eur = r'[Εε]υρώ|€|EUR'
dol = r'USD|$|[Δδ]ολ[άα]ρ[ιί][αών]{1,2}'
pnd = r'GPK|£|[Λλ]ίρ[εςών]{2}'
drm = r'[Δδ]ραχμ[ώνές]{2}|δρχ\.'
class Currency:
    currencies = [
         eur,
         dol,
         pnd,
         drm
    ]

def get_metrics(text):
    """
    Extracts all non-monetary amounts using the units class,
    from plain text
    """

    pattern = '|'.join(item for item in Unit.units)
    amounts_regex = re.compile(r'('+number_regex+'('+pattern+'))')
    amounts =  amounts_regex.finditer(text)

    result = []
    for match in amounts:
          if match.group(2) != '':
              result.append(match.group(1))

    return result

def get_monetary_amounts(text):
    """
    Extracts all monetary amounts using the currencies class,
    from plain text
    """
    pattern = '|'.join(item for item in Currency.currencies)
    currency_regex = re.compile(r'('+number_regex+'('+pattern+'))')
    currency =  currency_regex.finditer(text)

    result = []
    for match in currency:
          if match.group(2) != '':
              result.append(match.group(1))

    return result

class LegalEntities:
    entities = [
        law_regex,
        legislative_act_regex,
        presidential_decree_regex
    ]

    ratification = r'(ΝΟΜΟΣ|NOMOΣ|ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ|ΚΟΙΝΗ ΥΠΟΥΡΓΙΚΗ ΑΠΟΦΑΣΗ|ΝΟΜΟΘΕΤΙΚΟ ΔΙΑΤΑΓΜΑ) ΥΠ’ ΑΡΙΘ(|Μ). (\d+)'


class Numerals:

    units = {
        'μόνο': 1,
        'πρώτ': 1,
        'δεύτερ': 2,
        'τρίτ': 3,
        'τέταρτ': 4,
        'πέμπτ': 5,
        'έκτ': 6,
        'έβδομ': 7,
        'όγδο': 8,
        'ένατ': 9
    }

    inv_units = {
        1: 'πρώτ',
        2: 'δεύτερ',
        3: 'τρίτ',
        4: 'τέταρτ',
        5: 'πέμπτ',
        6: 'έκτ',
        7: 'έβδομ',
        8: 'όγδο',
        9: 'ένατ'
    }

    tens = {
        'δέκατ': 10,
        'εικοστ': 20,
        'τριακοστ': 30,
        'τεσσαρακοστ': 40,
        'πεντηκοστ': 50,
        'εξηκοστ': 60,
        'εβδομηκοστ': 70,
        'ογδοηκοστ': 80,
        'ενενηκοστ': 90
    }

    inv_tens = {
        80: 'ογδοηκοστ',
        50: 'πεντηκοστ',
        20: 'εικοστ',
        70: 'εβδομηκοστ',
        40: 'τεσσαρακοστ',
        10: 'δέκατ',
        60: 'εξηκοστ',
        90: 'ενενηκοστ',
        30: 'τριακοστ'
    }

    hundreds = {
        'εκατοστ': 100,
        'διακοσιοστ': 200,
        'τριακοσιοστ': 300,
        'τετρακοσιοστ': 400,
        'πεντακοσιοστ': 500,
        'εξακοσιοστ': 600,
        'εφτακοσιοστ': 700,
        'επτακοστιοστ': 700,
        'οκτακοσιοστ': 800,
        'οχτακοσιοστ': 800,
        'εννιακοστιοστ': 900
    }

    inv_hundreds = {
        100: 'εκατοστ',
        200: 'διακοσιοστ',
        300: 'τριακοσιοστ',
        400: 'τετρακοσιοστ',
        500: 'πεντακοσιοστ',
        600: 'εξακοσιοστ',
        700: 'επτακοστιοστ',
        800: 'οχτακοσιοστ',
        900: 'εννιακοστιοστ'
    }

    greek_nums = {
        'α': 1,
        'β': 2,
        'γ': 3,
        'δ': 4,
        'ε': 5,
        'στ': 6,
        'ζ': 7,
        'η': 8,
        'θ': 9,
        'ι': 10,
        'κ': 20,
        'λ': 30,
        'μ': 40,
        'ν': 50,
        'ξ': 60,
        'ο': 70,
        'π': 80,
        'Ϟ': 90,
        'ρ': 100
    }

    greek_nums_inv = {
        1: 'α',
        2: 'β',
        3: 'γ',
        4: 'δ',
        5: 'ε',
        6: 'στ',
        7: 'ζ',
        8: 'η',
        9: 'θ',
        10: 'ι',
        20: 'κ',
        30: 'λ',
        40: 'μ',
        50: 'ν',
        60: 'ξ',
        70: 'ο',
        80: 'π',
        90: 'Ϟ',
        100: 'ρ'
    }

    GREEK_NUM_MAX = 199

    @staticmethod
    def full_number_to_integer(s):
        result = 0

        for unit, val in Numerals.units.items():
            if re.search(unit, s) is not None:
                result += val
                break
        for ten, val in Numerals.tens.items():
            if re.search(ten, s) is not None:
                result += val
                break

        for hundred, val in Numerals.hundreds.items():
            if re.search(hundred, s) is not None:
                result += val
                break

        return result

    @staticmethod
    def full_numeral_to_integer_from_list(tmp, index):
        k = index - 1
        result = 0
        while k >= 0:
            print(tmp[k])
            number = Numerals.full_number_to_integer(tmp[k])
            if number == 0:
                break
            else:
                result += number
                k -= 1
        return result

    @staticmethod
    def greek_nums_to_int(s):
        r = 0
        for key, val in Numerals.greek_nums.items():
            if key in s:
                r += val

        return r

    @staticmethod
    def int_to_greek_num(n):
        result = []
        n = str(n)[::-1]
        for i, w in enumerate(n):
            if w != '0':
                result.append(str(Numerals.greek_nums_inv[int(w) * 10**(i)]))
        return ''.join(result[::-1])

    @staticmethod
    def greek_num_generator(n=None, suffix=')'):
        if not n:
            n = Numerals.GREEK_NUM_MAX
        else:
            n = min(Numerals.GREEK_NUM_MAX, n)

        for i in range(1, n + 1):
            yield Numerals.int_to_greek_num(i) + suffix

    class GreekNum:
        """Support for greek numerals"""

        def __init__(self, s='α'):
            if isinstance(s, str):
                self._s = s
                self._value = Numerals.greek_nums_to_int(s)
            elif isinstance(s, int):
                self._value = s
                self._s = Numerals.int_to_greek_num(s)

        @property
        def s(self):
            return self._s

        @s.getter
        def s(self):
            return self._s

        @s.setter
        def s(self, v):
            self._s = v
            self._value = Numerals.greek_nums_to_int(v)

        @property
        def value(self):
            return self._value

        @value.getter
        def value(self):
            return self._value

        @value.setter
        def value(self, x):
            self._value = x
            self._s = Numerals.int_to_greek_num(x)

        def __eq__(self, other):
            return self.value == other.value

        def __ne__(self, other):
            return self.value != other.value

        def __gt__(self, other):
            return self.value > other.value

        def __lt__(self, other):
            return self.value < other.value

        def __ge__(self, other):
            return self.value >= other.value

        def __le__(self, other):
            return self.value <= other.value

        def __str__(self):
            return self.s

        def __repr__(self):
            return self.s

        def __add__(self, other):
            x = Numerals.GreekNum()
            x.value = self.value + other.value
            return x

        def __sub__(self, other):
            x = Numerals.GreekNum()
            x.value = self.value - other.value
            return x

        def __mul__(self, other):
            x = Numerals.GreekNum()
            x.value = self.value * other.value
            return x

        def __floordiv__(self, other):
            x = Numerals.GreekNum()
            try:
                x.value = self.value // other.value
            except BaseException:
                raise ValueError
            return x
