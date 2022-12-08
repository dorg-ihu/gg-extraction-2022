from itertools import product


'''
Create fixed lexical resources 
'''

# alphabet = ['α','β','γ','δ','ε','στ','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω']
alphabet = ['α','β','γ','δ','ε','στ','ζ','η','θ','ι','ια','ιβ','ιγ','ιδ','ιε','ιστ','ιζ','ιη','ιθ','ικ','κ','κα','κβ','κγ','κδ','κε','κστ','κζ','κη','κθ','λ','λα','λβ','λγ','λδ','λε','λστ','λη','λθ',
            'μ','μα','μβ','μγ','μδ','με','μστ','μη','μθ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω']
latin_numbers = ['i','ii','iii','iv','v','vi','vii','viii','ix','x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx']
numbers = [str(item) for item in list(range(1,15))]
ab_combs = [''.join(comb) for comb in product(alphabet, repeat=2)]
double_combs = [comb*2 for comb in ab_combs]
t = alphabet.pop(13) # remove ν. due to laws

alphabet_greek_only_latin = ['Α', 'Β', 'Ε','Ζ', 'Η', 'Ι', 'Κ', 'Μ', 'Ν', 'Ο', 'Ρ', 'Τ', 'Υ', 'Χ']
alphabet_latin_only_greek = ['A' ,'B', 'E', 'Z', 'H', 'I', 'K', 'M', 'N', 'O', 'P', 'T', 'Y', 'X']
ab_greek_latin_pat = rf"{'|'.join(alphabet_latin_only_greek)}"
alphabet_latin_to_greek = {latin: greek for latin, greek in zip(alphabet_latin_only_greek, alphabet_greek_only_latin) }

all_combs = alphabet + ab_combs + double_combs + latin_numbers + numbers
ab_double_combs = ab_combs + double_combs
all_combs_pat = "(" + "|".join(all_combs) + ")"

split_all_pattern = rf"[\n ]\(?{all_combs_pat}[).] *"

# added for testing purpose
all_combs_sublvl = alphabet + ab_combs + double_combs + latin_numbers
all_combs_pat_sublvl = "(" + "|".join(all_combs_sublvl) + ")"
split_all_pattern_sublvl = rf"[\n ]\(?{all_combs_pat_sublvl}[).] *"

abbr_replacements = [("κ.λπ", "ΚΛΠ#"),
                        ("π.δ", "ΠΔ#"),
                        ("π.δ.", "ΠΔ#"),
                        ("κ.α", "KA#"),
                        ("κ.ά.", "ΚΑ#"),
                        ("ν.δ.", "ΝΔ#"),
                        (" αρ.", " ΑΡ#"),
                        (" ν.", " N#"),
                        ("\nν.", "\nΝ#")
                        ]

intodict = {"Ι": "I",
            "Ν": "N",
            "Τ": "T",
            "Ο": "O",
            "Α": "A"}