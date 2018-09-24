import os
import glob
import jieba
import re
from collections import defaultdict

ptn = re.compile(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。×》〕:《〈？、~@#￥%……&*（）]+')
en = re.compile('[a-zA-Z0-9]+')

def load_stopwords(filepath):
    with open(filepath, encoding='utf-8') as f:
        stops = set([v.strip() for v in f.readlines()])
    return stops


def remove_sign_and_en(text):
    text = ptn.sub(' ', text)
    return en.sub(' ', text)

def parse(filename, words, table):
    for word in words:
        table[filename][word] = 1

def get_default_dict():
    return defaultdict(int)

def get_boolean_model():
    stops = load_stopwords('./stopwords.txt')
    word_set = set()
    table = defaultdict(get_default_dict)
    files = glob.glob('./page/*.md')
    for file in files:
        with open(file) as f:
            text = remove_sign_and_en(' '.join(f.readlines()))
            words = set(jieba.cut(text)) - stops
            word_set.update(words)
            parse(file.split('/')[-1], words, table)
    return table

