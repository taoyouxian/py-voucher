#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : rfa.py.py
@Author: taoyx
@Contact : taoyouxian@ruc.edu.cn 
@Date  : 2018/3/19 18:25
@Desc  : 
'''

import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# print(WORDS)
# print(WORDS.values())
# print(sum(WORDS.values()))
word = "speling"
# for w in words:
#     if w in WORDS:
#         print(w, " ", WORDS[w])
# print(known(word))
letters = 'abcdefghijklmnopqrstuvwxyz'
splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
print(splits)
# print(",\t".join(L for L, R in splits if R))
# print(",\t".join(R[1:] for L, R in splits if R))
deletes = [L + R[1:] for L, R in splits if R]
print("deletes", deletes)
transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
print("transposes", transposes)
replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
print("replaces", replaces)
# print(correction('speling'))


