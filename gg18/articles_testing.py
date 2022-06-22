# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:02:55 2022

@author: kostas
"""
import sys
import re
from gm3.gm3 import helpers, tokenizer
import collections

stdin = False
#filename = "fek-organismoi-upourgeiwn/yp-eswterikwn-141-2017.txt"
#filename = "fek-organismoi-upourgeiwn/yp-agrotikhsanaptukshskaitrofimwn-97-2017.txt"
filename = "fek-organismoi-upourgeiwn/yp-dikaiosunhs-6-2021.txt"
lines = []
tmp_lines = []

if not stdin:
    infile = open(filename, 'r', encoding='utf8')


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




  
for j in range(len(article_indices) - 1):

    content = lines[article_indices[j][0] + 1: article_indices[j + 1][0]]

    paragraphs = collections.defaultdict(list)
    current = '0'
    for t in content:
        x = re.search(r'\d+.', t)
        if x and x.span() in [(0, 2), (0, 3)]:
            current = x.group().strip('.')
        paragraphs[current].append(t)
    
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
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  