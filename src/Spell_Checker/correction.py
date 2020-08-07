import re
from collections import Counter
import os

def words(text): return re.findall(r'\w+', text.upper())

WORDS = Counter(words(open(os.getcwd()+'/Spell_Checker/big2.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    if (len(word) >= 2 and (word[-2] == "’" or word[-2] == "'") and word[-1] == 'S'):
        word = word[:-2]
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    # print(known(edits2(word)))
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    letters = letters.upper()
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    # print (splits)
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def spellCheck(text):
    return correction(text)

# def spellCheck(text):
#     crop_folder = '../results/crops_text'
#     for filename in os.listdir(crop_folder):
#         file_path = os.path.join(crop_folder, filename)
#         text = str(open(file_path).read())
#         text = text.split()
#         for i in text:
#             print(correction(i.upper()))

# print(correction("CONSIGNAE'S"))