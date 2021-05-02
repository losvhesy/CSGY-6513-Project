import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
from itertools import product
import string

stop_words = set(stopwords.words('english'))

def reconstruct_text(token):
    text_list = []
    for sub in token.lefts:
        sub_text = reconstruct_text(sub)
        text_list.append(sub_text)
    text_list.append(token.orth_)
    for sub in token.rights:
        sub_text = reconstruct_text(sub)
        text_list.append(sub_text)
    return " ".join(text_list)


def generate_ngrams(words, nums):
    n_grams = []
    for num in nums:
        n_grams.extend(extract_ngrams(words, num))
    return n_grams


def build_ngrams(text):
    text.split()
    words = text.split()
    table = str.maketrans('', '', string.punctuation)
    words = [w.translate(table) for w in words]
    words = list(filter(lambda w: w.lower() not in stop_words, words))
    n_grams = generate_ngrams(words, [1, 2, 3, 4, 5])
    return n_grams


def get_token_text(token):
    text = []
    for sub in token.children:
        if sub.dep_ == "compound":
            text.append(sub.orth_)
    text.append(token.orth_)
    return " ".join(text)


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_

def tokenize_sent(text):
    return text.split()

def extract_ngrams(words, num):
    n_grams = nltk.ngrams(words, num)
    return [' '.join(grams) for grams in n_grams]

