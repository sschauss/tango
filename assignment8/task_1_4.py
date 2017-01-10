from collections import Counter
from functools import partial, reduce
from itertools import combinations
import pandas as pd
import math
import re
import time


def compose(*functions):
    return lambda args: reduce(lambda acc, f: f(acc), reversed(functions), args)


def split(text):
    # split text by words
    return re.split(r'\W+', text)


def calcJaccardSimilarity(wordset1, wordset2):
    intersection = len(wordset1 & wordset2)
    union = len(wordset1 | wordset2)
    # return 0 if set union 0
    return 0 if union is 0 else intersection / union


def calcTermFrequency(text):
    return Counter(split(text))


def calcTfIdf(d_term_frequencies, doc_count, wordset, term_frequencies):
    return {term: term_frequencies[term] * math.log(doc_count / d_term_frequencies[term]) for term in wordset}


def flatten(l):
    # http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    return [item for sublist in l for item in sublist]


def calculateCosineSimilarity(tfIdfDict1, tfIdfDict2):
    # gather all terms
    terms = set(tfIdfDict1.keys()) | set(tfIdfDict2.keys())
    # calculate sparse matrix multiplication
    numerator = sum(tfIdfDict1.get(term, 0) * tfIdfDict2.get(term, 0) for term in terms)
    # calculate vector length
    denominator = math.sqrt(sum([v ** 2 for v in tfIdfDict1.values()])) * math.sqrt(
        sum([v ** 2 for v in tfIdfDict2.values()]))
    return numerator / denominator


with pd.HDFStore('store2.h5', 'r', enconding='utf-8') as store:
    # define sample length
    n = 100

    df2 = store['df2']
    # track rows by name
    df2 = df2.set_index('name')
    # map list of out links to set
    df2['out_links_set'] = df2['out_links'].map(set)

    df1 = store['df1']
    # count articles
    df1_article_count = len(df1)
    # map text to list of words and then to word set
    df1['word_set'] = df1['text'].map(compose(set, split))
    # calculate overall term frequencies
    document_term_frequencies = Counter(flatten(df1['word_set']))
    # map text to term frequency
    df1['term_frequency'] = df1['text'].map(calcTermFrequency)
    # map wordset with term frequency to tf idf
    df1['tf_idf'] = list(map(lambda t: calcTfIdf(document_term_frequencies, df1_article_count, *t),
                             zip(df1['word_set'], df1['term_frequency'])))
    # map text to text length
    df1['text_length'] = df1['text'].map(len)
    # sort by text length descending and track rows by name
    df1 = df1.sort_values('text_length', ascending=False).set_index('name')
    # initialize counter for computations
    df1_count = 0
    # calculate combinations to calculate
    df1_combination_count = n * (n - 1) / 2
    # n first index
    df1_sets_with_index = df1.index.values[:n + 1]
    # initialize similarity dict
    similarities = {}
    # initialize calculation start time
    start_time = time.time()
    # iterate over pairwise combinations of word sets with index
    for left_index, right_index in combinations(df1_sets_with_index, 2):
        # calculate jaccard similarity for text
        text_jaccard = calcJaccardSimilarity(df1['word_set'].loc[left_index],
                                             df1['word_set'].loc[right_index])
        # calculate cosine similarity for terms
        cosine_similarity = calculateCosineSimilarity(df1['tf_idf'].loc[left_index],
                                                      df1['tf_idf'].loc[right_index])
        # calculate jaccard similarity for out links
        link_jaccard = calcJaccardSimilarity(df2['out_links_set'].loc[left_index],
                                             df2['out_links_set'].loc[right_index])
        # store similarity pairs in similarity dictionary
        similarities.update({(left_index, right_index): [text_jaccard, link_jaccard, cosine_similarity]})
        similarities.update({(right_index, left_index): [text_jaccard, link_jaccard, cosine_similarity]})
        # increase computation counter
        df1_count += 1
        # print for feedback for every 100 computations
        if df1_count % 100 is 0:
            print(
                'calculated %i from %i (%f %%)' % (
                    df1_count, df1_combination_count, 100 * df1_count / df1_combination_count))
    print("first %s pairwise similarity calculations: %s seconds" % (n, time.time() - start_time))
