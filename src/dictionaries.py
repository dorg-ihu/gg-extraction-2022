from itertools import product


'''
Create fixed lexical resources 
'''

alphabet = ['α','β','γ','δ','ε','στ','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω']
latin_numbers = ['i','ii','iii','iv','v','vi','vii','viii','ix','x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx']
numbers = [str(item) for item in list(range(1,10))]
ab_combs = [''.join(comb) for comb in product(alphabet, repeat=2)]
double_combs = [comb*2 for comb in ab_combs]
t = alphabet.pop(13) # remove ν. due to laws

all_combs = alphabet + ab_combs + double_combs + latin_numbers + numbers
ab_double_combs = ab_combs + double_combs
all_combs_pat = "(" + "|".join(all_combs) + ")"

split_all_pattern = rf"[\n ]\(?{all_combs_pat}[).] *"