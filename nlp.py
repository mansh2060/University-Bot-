import nltk
nltk.download('punkt_tab')

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import numpy as np


def tokenize(sentences):
    return word_tokenize(sentences)

def stem(words):
    stemming=PorterStemmer()
    return stemming.stem(words)


def bag_of_words(existing_words_list,preprocessed_list):
    preprocessed_list=[stem(words.lower()) for words in preprocessed_list]
    vector_np=np.zeros(len(existing_words_list),dtype=np.float32)  # [0 0 0 0 0 0 0 0 0 ......]
    for idx,words in enumerate(existing_words_list):
        if words in preprocessed_list:
            vector_np[idx]=1
    return vector_np