
# coding: utf-8

import pandas as pd
import string
import math

store = pd.HDFStore('store2.h5')
df1=store['df1'] 
df2=store['df2']
word_dict = dict()
tf_dict = dict()
df_dict = dict()
tfidf_dict = dict()
euclead_dict = dict()
ARTICLES = len(df1)

def create_set(text):
    words = text.lower().split()
    words_pure = set(w.strip(string.punctuation) for w in words)
    return words_pure

def create_dict(index):
    try:
        word_dict[index] = create_set(df1.text.loc[index])
    except:
        print (article_name)
        print (df1[df1.name==article_name].text)


# 1.1.1. 2) Implementation of the function calcJaccardSimilarity

def calcJaccardSimilarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection)/len(union)

def getId(article):
    idx = df1[df1.name==article].index.tolist()[0]
    return idx

def calc_tf_df(index): 
    a_tf_dict = dict()
    text = df1.text.loc[index]
    a_unique_words = word_dict[index]
    for term in a_unique_words:        
        tf = text.count(str(term))
        a_tf_dict[term] = tf
        if term in df_dict:
            df_dict[term] += 1
        else:
            df_dict[term] = 1
    tf_dict[index] = a_tf_dict

def calc_tfidf(index):
    a_tfidf = dict()
    a_unique_words = word_dict[index]
    sum_tfidf = 0
    for term in a_unique_words:
        a_tf = tf_dict[index]
        tfidf = a_tf[term] * math.log(ARTICLES/df_dict[term])
        sum_tfidf = sum_tfidf + tfidf * tfidf
        a_tfidf[term] = tfidf
    tfidf_dict[index] = a_tfidf
    euclead_dict[index] = math.sqrt(sum_tfidf)

def calc_scalar(tfIdfDict1, tfIdfDict2): 
    wordset1 = set(tfIdfDict1.keys())
    wordset2 = set(tfIdfDict2.keys())
    common_words = wordset1.intersection(wordset2)
    sum_products = 0
    for term in common_words:
        try:
            sum_products = sum_products + tfIdfDict1[term] * tfIdfDict2[term] 
        except:
            print (term)
    return sum_products

def calc_Euclead(tfIdfDict): 
    coords = list(tfIdfDict.values())
    sum_coords = 0
    for value in coords:        
        sum_coords = sum_coords + value * value    
    return math.sqrt(sum_coords)


# 1.1.2 4) Implementation of the fuction calculateCosineSimilarity

def calculateCosineSimilarity(tfIdfDict1, tfIdfDict2):
    return calc_scalar(tfIdfDict1, tfIdfDict2) / (calc_Euclead(tfIdfDict1) * calc_Euclead(tfIdfDict2))   


if __name__ == '__main__':

    # 1.1.1. 1) create dictionary that contains set of unique words (value) for each article id (key)
    
    for index in df1.index.tolist():
        create_dict(index)
        

    # 1.1.1. 3) Jaccard Similarity for articles Germany, Europe

    Jaccard_sim = calcJaccardSimilarity(word_dict[getId('Germany')], word_dict[getId('Europe')])
    print ('Jaccard Similarity coefficient: ', Jaccard_sim)
    

    # 1.1.2. 1), 2) populate dictionaries tf_dict and df_dict:
    # tf_dict has article id as a key and a dictionary (term (key) - term frequency (value)) as a value 
    # df_dict contains unique terms in all articles as keys and a number of document in which this term is occured as value

    for article_index in df1.index.tolist():
        calc_tf_df(article_index)       
        

    # 1.1.2. 3) populate dictionary tfidf_dict that has article id as a key and a dictionary (term (key) - tfidf (value)) as a value

    for article_index in df1.index.tolist():
        calc_tfidf(article_index)
        

    # 1.1.2. 5) Cosine Similarity for articles Germany, Europe

    cosine_sim = calculateCosineSimilarity(tfidf_dict[getId('Germany')], tfidf_dict[getId('Europe')])
    print ('Cosine Similarity coefficient: ', cosine_sim)
    

    # 1.2. Cosine Similarity for out_links of the articles Germany, Europe

    Jaccard_sim_graph = calcJaccardSimilarity(set(df2.loc[getId('Germany')].out_links), set(df2.loc[getId('Europe')].out_links))
    print ('Jaccard Similarity coefficient for outlinks: ', Jaccard_sim_graph)





