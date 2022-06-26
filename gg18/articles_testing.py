# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:02:55 2022

@author: kostas
"""
import sys
import re
from gm3.gm3 import helpers, tokenizer
import collections
from copy import copy

stdin = False
#filename = "fek-organismoi-upourgeiwn/yp-eswterikwn-141-2017.txt"
#filename = "fek-organismoi-upourgeiwn/yp-agrotikhsanaptukshskaitrofimwn-97-2017.txt"
filename = "fek-organismoi-upourgeiwn/yp-oikonomikwn-142-2017.txt"
lines = []
tmp_lines = []

if not stdin:
    infile = open(filename, 'r', encoding='utf8')



levels = collections.OrderedDict([(1, ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.']),
                                  (2, ['α)', 'β)', 'γ)', 'δ)', 'ε)', 'στ)', 'ζ)', 'η)', 'θ)', 'ι)', 'ια)', 'ιβ)', 'ιγ)', 'ιδ)', 'ιε)', 'ιστ)', 'ιζ)', 'ιη)', 'ιθ)', 'κ)', 'κα)', 'κβ)', 'κγ)', 'κδ)', 'κε)', 'κστ)', 'κζ)', 'κη)', 'κθ)', 'λ)', 'λα)', 'λβ)', 'λγ)', 'λε)', 'λστ)', 'λζ)', 'λη)', 'λθ)']),
                                  (3, ['(α)', '(β)', '(γ)', '(δ)', '(ε)', '(στ)', '(ζ)', '(η)', '(θ)', '(ι)', '(ια)', '(ιβ)', '(ιγ)', '(ιδ)', '(ιε)', '(ιστ)', '(ιζ)', '(ιη)', '(ιθ)', '(κ)', '(κα)', '(κβ)', '(κγ)', '(κδ)', '(κε)', '(κστ)', '(κζ)', '(κη)', '(κθ)', '(λ)', '(λα)', '(λβ)', '(λγ)', '(λε)', '(λστ)', '(λζ)']),
                                  (4, ['αα)', 'ββ)', 'γγ)', 'δδ)', 'εε)', 'στστ)', 'ζζ)', 'ηη)', 'θθ)', 'ιι)', 'ιαια)', 'ιβιβ)', 'ιγιγ)', 'ιδιδ)', 'ιειε)', 'ιστιστ)', 'ιζιζ)', 'ιηιη)', 'ιθιθ)', 'κκ)', 'κακα)', 'κβκβ)', 'κγκγ)', 'κδκδ)', 'κεκε)', 'κστκστ)', 'κζκζ)', 'κηκη)', 'κθκθ)', 'λλ)', 'λαλα)', 'λβλβ)', 'λγλγ)', 'λελε)', 'λστλστ)', 'λζ)']),                 
                                  (5, ['(αα)', '(ββ)', '(γγ)', '(δδ)', '(εε)', '(στστ)', '(ζζ)', '(ηη)', '(θθ)', '(ιι)', '(ιαια)', '(ιβιβ)', '(ιγιγ)', '(ιδιδ)', '(ιειε)', '(ιστιστ)', '(ιζιζ)', '(ιηιη)', '(ιθιθ)', '(κκ)', '(κακα)', 'κβκβ)', 'κγκγ)', 'κδκδ)', 'κεκε)', 'κστκστ)', 'κζκζ)', 'κηκη)', 'κθκθ)', 'λλ)', 'λαλα)', 'λβλβ)', 'λγλγ)', 'λελε)', 'λστλστ)', 'λζ)'])
                                  ])







while True:
    if not stdin:
        l = infile.readline()
    else:
        l = sys.stdin.readline()
    if not l:
        break
    l = l.replace('−\n', '')
    l = l.replace('\n', ' ')
    l = re.sub(r' +', ' ', l)
    l = helpers.fix_par_abbrev(l)
    tmp_lines.append(l)
    
if not stdin:
    infile.close()
    
 
for line in tmp_lines:
    if line.endswith('ΕΦΗΜΕΡΙ∆Α TΗΣ ΚΥΒΕΡΝΗΣΕΩΣ'): line.replace('ΕΦΗΜΕΡΙ∆Α TΗΣ ΚΥΒΕΡΝΗΣΕΩΣ', '')
    if line.endswith('ΕΦΗΜΕΡΙΣ ΤΗΣ ΚΥΒΕΡΝΗΣΕΩΣ'): line.replace('ΕΦΗΜΕΡΙΣ ΤΗΣ ΚΥΒΕΡΝΗΣΕΩΣ', '')
    
    if line == '':
        continue
    elif line.startswith('Τεύχος') or line.startswith('ΕΦΗΜΕΡΙ∆Α TΗΣ ΚΥΒΕΡΝΗΣΕΩΣ') or line.startswith('ΕΦΗΜΕΡΙΣ ΤΗΣ ΚΥΒΕΡΝΗΣΕΩΣ'):
        continue
    else:
        try:
            n = int(line)
            continue
        except ValueError:
            lines.append(line)
            if line.startswith('Αρ. Φύλλου'):
                for x in line.split(' '):
                    if x.isdigit():
                        issue_number = x
                        break
                    
# articles = {}
# articles_as_paragraphs = {}
# article_indices = []
# for i, line in enumerate(lines):
#     if line.startswith('Άρθρο') or line.startswith(
#             'Ο Πρόεδρος της Δημοκρατίας'):
#         article_indices.append((i, line.strip()))
#         articles[line.strip()] = ''
     
articles = {}
articles_as_paragraphs = {}
article_indices = []
for i, line in enumerate(lines):
    if (line.strip().startswith('Άρθρο') and len(line.strip()) < 10) or line.startswith(
            'Ο Πρόεδρος της Δημοκρατίας') or line.startswith('Η Πρόεδρος της Δημοκρατίας'):
        article_indices.append((i, line.strip()))
        articles[line.strip()] = ''




j = 11
#for j in range(len(article_indices) - 1):
for j in range(24, 25):    
    content = lines[article_indices[j][0] + 1: article_indices[j + 1][0]]

    paragraphs = collections.defaultdict(list)
    current = '0'
    for t in content:
        x = re.search(r'\d+\.', t)
        if x and x.span() in [(0, 2), (0, 3)]:
            current = x.group().strip('.')
        paragraphs[current].append(t)
    
    
    new_paragraphs = copy(paragraphs)
    
    for key, val in paragraphs.items():    
        for idx, line in enumerate(val[1:]):
            y = re.search(r'\d+\.', line)
            if y and y.span() in [(0, 2), (0, 3)]:
                #discard = val[idx:]
                new_paragraphs[key] = val[:idx]
                # discard = line[idx:]
                # line = line[:idx]
                break
        #paragraphs["discard"].append(discard)           
    
    sentences = {}

    for par in paragraphs.keys():
        val = ''.join(paragraphs[par])[0:]
        paragraphs[par] = val
        sentences[par] = list(
            filter(
                lambda x: x.rstrip() != '',
                tokenizer.tokenizer.split(val, False, '. ')))

    articles[article_indices[j][1]] = ''.join(content)
    articles_as_paragraphs[article_indices[j][1]] = paragraphs
  
  
try:
    del articles['Ο Πρόεδρος της Δημοκρατίας']
except BaseException:
    pass
  
  
  
  
  
  
x1 = '3.4, INTOSAI 1.0.39 Ευρωπαϊκή κατευθυντήρια γραμμή '
x2 = '333. του άρθρου 5 του ν. 3943/2011, όπως τροποποιήθηκε, '
x3 = '14 και να καίει'



x = re.search(r'\d+\.', x1)
y = re.search(r'\d+\.', x2)
z = re.search(r'\d+\.', x3)
print(x, x.span())
print(y, y.span())
print(z, z.span())  


if x and x.span() in [(0, 2), (0, 3)]:
    results = x.group().strip('.')
    print(results)

if y and y.span() in [(0, 2), (0, 3), (0, 4)]:
    results = y.group().strip('.')
    print(results)
  
if z and z.span() in [(0, 2), (0, 3)]:
    results = z.group().strip('.')
    print(results)
  
  
  
#% NEW ARTICLE LEVELING
 
levels = collections.OrderedDict(
    [(1, ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.']),
     (2, ['α)', 'β)', 'γ)', 'δ)', 'ε)', 'στ)', 'ζ)', 'η)', 'θ)', 'ι)', 'ια)', 'ιβ)', 'ιγ)', 'ιδ)', 'ιε)', 'ιστ)', 'ιζ)', 'ιη)', 'ιθ)', 'κ)', 'κα)', 'κβ)', 'κγ)', 'κδ)', 'κε)', 'κστ)', 'κζ)', 'κη)', 'κθ)', 'λ)', 'λα)', 'λβ)', 'λγ)', 'λε)', 'λστ)', 'λζ)', 'λη)', 'λθ)']),
     (3, ['(α)', '(β)', '(γ)', '(δ)', '(ε)', '(στ)', '(ζ)', '(η)', '(θ)', '(ι)', '(ια)', '(ιβ)', '(ιγ)', '(ιδ)', '(ιε)', '(ιστ)', '(ιζ)', '(ιη)', '(ιθ)', '(κ)', '(κα)', '(κβ)', '(κγ)', '(κδ)', '(κε)', '(κστ)', '(κζ)', '(κη)', '(κθ)', '(λ)', '(λα)', '(λβ)', '(λγ)', '(λε)', '(λστ)', '(λζ)']),
     (4, ['αα)', 'ββ)', 'γγ)', 'δδ)', 'εε)', 'στστ)', 'ζζ)', 'ηη)', 'θθ)', 'ιι)', 'ιαια)', 'ιβιβ)', 'ιγιγ)', 'ιδιδ)', 'ιειε)', 'ιστιστ)', 'ιζιζ)', 'ιηιη)', 'ιθιθ)', 'κκ)', 'κακα)', 'κβκβ)', 'κγκγ)', 'κδκδ)', 'κεκε)', 'κστκστ)', 'κζκζ)', 'κηκη)', 'κθκθ)', 'λλ)', 'λαλα)', 'λβλβ)', 'λγλγ)', 'λελε)', 'λστλστ)', 'λζ)']),                 
     (5, ['(αα)', '(ββ)', '(γγ)', '(δδ)', '(εε)', '(στστ)', '(ζζ)', '(ηη)', '(θθ)', '(ιι)', '(ιαια)', '(ιβιβ)', '(ιγιγ)', '(ιδιδ)', '(ιειε)', '(ιστιστ)', '(ιζιζ)', '(ιηιη)', '(ιθιθ)', '(κκ)', '(κακα)', 'κβκβ)', 'κγκγ)', 'κδκδ)', 'κεκε)', 'κστκστ)', 'κζκζ)', 'κηκη)', 'κθκθ)', 'λλ)', 'λαλα)', 'λβλβ)', 'λγλγ)', 'λελε)', 'λστλστ)', 'λζ)'])
    ])
  

regexfornumbers = r'\d+\.'
#regexforchar = r'\(??\D[α-ωΑ-ω]+\)' # with parenthesis or not
regexforchars = r'\(??\D[α-ωΑ-ω]+\)' # with parenthesis or not






level = 0
previousParagraph = ''
currentParagraph = ''

for line in content:
    start = line[:7]
    lvl1 = re.search(regexfornumbers, start)
    lvl2 = re.search(regexforchars, start)
    if lvl1:
        matched = lvl1.match()
        break
    if lvl2:
        matched = lvl2.match() 
        break






level1 = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.']
level2 = ['α', 'β', 'γ', 'δ', 'ε', 'στ', 'ζ', 'η', 'θ', 'ι', 'ια', 'ιβ', 'ιγ', 'ιδ', 'ιε', 'ιστ', 'ιζ', 'ιη', 'ιθ', 
          'κ', 'κα', 'κβ', 'κγ', 'κδ', 'κε', 'κστ', 'κζ', 'κη', 'κθ', 'λ', 'λα', 'λβ', 'λγ', 'λε', 'λστ', 'λζ', 'λη', 'λθ']
level3 = ['αα', 'ββ', 'γγ', 'δδ', 'εε', 'στστ', 'ζζ', 'ηη', 'θθ', 'ιι', 'ιαια', 'ιβιβ', 'ιγιγ', 'ιδιδ', 'ιειε', 'ιστιστ', 'ιζιζ', 'ιηιη', 'ιθιθ',
          'κκ', 'κακα', 'κβκβ', 'κγκγ', 'κδκδ', 'κεκε', 'κστκστ', 'κζκζ', 'κηκη', 'κθκθ', 'λλ', 'λαλα', 'λβλβ', 'λγλγ', 'λδλδ', 'λελε', 'λστλστ', 'λζ΄λζ΄', 'ληλη', 'λθλθ']

level = { 'A': ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.'],
          'B': ['α', 'β', 'γ', 'δ', 'ε', 'στ', 'ζ', 'η', 'θ', 'ι', 'ια', 'ιβ', 'ιγ', 'ιδ', 'ιε', 'ιστ', 'ιζ', 'ιη', 'ιθ',
                'κ', 'κα', 'κβ', 'κγ', 'κδ', 'κε', 'κστ', 'κζ', 'κη', 'κθ', 'λ', 'λα', 'λβ', 'λγ', 'λε', 'λστ', 'λζ', 'λη', 'λθ'],
          'C': ['αα', 'ββ', 'γγ', 'δδ', 'εε', 'στστ', 'ζζ', 'ηη', 'θθ', 'ιι', 'ιαια', 'ιβιβ', 'ιγιγ', 'ιδιδ', 'ιειε', 'ιστιστ', 'ιζιζ', 'ιηιη', 'ιθιθ', 
                'κκ', 'κακα', 'κβκβ', 'κγκγ', 'κδκδ', 'κεκε', 'κστκστ', 'κζκζ', 'κηκη', 'κθκθ', 'λλ', 'λαλα', 'λβλβ', 'λγλγ', 'λδλδ', 'λελε', 'λστλστ', 'λζ΄λζ΄', 'ληλη', 'λθλθ']
        }



j = 4
content = lines[article_indices[j][0] + 1: article_indices[j + 1][0]]
regexfornumbers = r'\d+\.'
regexforchars = r'\(??\D[α-ωΑ-ω]+\)'

# να βαλω το 1 Line εκτος for και μετα να ξεκιναω τη λουπα απο τη 2η γραμμη 

paragraphs = collections.defaultdict(list)

lastadded = ""
current = 0
paragraphs[current] = content[0]
for line in content[1:]:
    start = line[:10]
    swNumber = re.search(regexfornumbers, start)
    swChars = re.search(regexforchars, start)
    
    if swNumber:
        current = re.sub("[^0-9]", "", swNumber.group())
        lastadded = next(reversed(paragraphs))
        if int(current) - lastadded == 1:
            current = int(current)
            paragraphs[current].append(line)
        else:
            paragraphs[lastadded].append(line)
        
        break
    
    if swChars:
        current = re.sub('[(.)]', '', swChars.group())
        if current in level['B']:
            currentlevel = "B"
        elif current in level['C']:
            currentlevel = "C"
        
        
        
        break
    paragraphs[1].append(line)
    paragraphs[current]
    
    
    
    
    
    
    if swNumber: hierarchy.append(swNumber.group(0))
    if swChars: hierarchy.append(swChars.group(0))
        







    paragraphs = collections.defaultdict(list)
    current = '0'
    for t in content:
        x = re.search(r'\d+\.', t)
        if x and x.span() in [(0, 2), (0, 3)]:
            current = x.group().strip('.')
        paragraphs[current].append(t)







current = '0'
for t in content:
    x = re.search(r'\d+\.', t)
    if x and x.span() in [(0, 2), (0, 3)]:
        current = x.group().strip('.')
    paragraphs[current].append(t)


new_paragraphs = copy(paragraphs)

for key, val in paragraphs.items():    
    for idx, line in enumerate(val[1:]):
        y = re.search(r'\d+\.', line)
        if y and y.span() in [(0, 2), (0, 3)]:
            #discard = val[idx:]
            new_paragraphs[key] = val[:idx]
            # discard = line[idx:]
            # line = line[:idx]
            break
    #paragraphs["discard"].append(discard)           

sentences = {}

for par in paragraphs.keys():
    val = ''.join(paragraphs[par])[0:]
    paragraphs[par] = val
    sentences[par] = list(
        filter(
            lambda x: x.rstrip() != '',
            tokenizer.tokenizer.split(val, False, '. ')))

articles[article_indices[j][1]] = ''.join(content)
articles_as_paragraphs[article_indices[j][1]] = paragraphs
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  