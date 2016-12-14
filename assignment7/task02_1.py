
# coding: utf-8

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sortedcontainers as c
import random

def convert_dict(d):
    s = pd.Series(d)
    s.index.name='Char'
    s.reset_index()
    df = pd.DataFrame({'Char':s.index, 'P':s.values})
    df['S'] = np.cumsum(df['P'])
    return df

def generate_chars(file, distribution, n):
    d = convert_dict(distribution)
    sd = c.SortedDict((key, value) for key, value in zip(d['S'],d['Char']))
    str=[]
    for i in range(1,n+1):
        index = sd.bisect(random.random())
        key = sd.iloc[index]
        str.append(sd[key])
        if (i % 1000000 == 0 or i==n):
            text=''.join(str)
            print(i)
            append_to_file(file, text)
            str=[]  

# Create a new file
def write_file(file):
    with open(file, 'w') as f:
        f.write('')

# Add data onto an existing file
def append_to_file(file, data):
    with open(file, 'a') as file:
        file.write(data)



if __name__ == '__main__':

    zipf_probabilities = {' ': 0.17840450037213465, '1': 0.004478392057619917, '0': 0.003671824660673643, '3': 0.0011831834225755678, '2': 0.0026051307175779174, '5': 0.0011916662329062454, '4': 0.0011108979455528355, '7': 0.001079651630435706, '6': 0.0010859164582487295, '9': 0.0026071152282516083, '8': 0.0012921888323905763, '_': 2.3580656240324293e-05, 'a': 0.07264712490903191, 'c': 0.02563767289222365, 'b': 0.013368688579962115, 'e': 0.09688273452496411, 'd': 0.029857183586861923, 'g': 0.015076820473031856, 'f': 0.017232219565845877, 'i': 0.06007894642873102, 'h': 0.03934894249122837, 'k': 0.006067466280926215, 'j': 0.0018537015877810488, 'm': 0.022165129421030945, 'l': 0.03389465109649857, 'o': 0.05792847618595622, 'n': 0.058519445305660105, 'q': 0.0006185966212395744, 'p': 0.016245321110753712, 's': 0.055506530071283755, 'r': 0.05221605572640867, 'u': 0.020582942617121572, 't': 0.06805204881206219, 'w': 0.013964469813783246, 'v': 0.007927199224676324, 'y': 0.013084644140464391, 'x': 0.0014600810295164054, 'z': 0.001048859288348506}
    uniform_probabilities = {' ': 0.1875, 'a': 0.03125, 'c': 0.03125, 'b': 0.03125, 'e': 0.03125, 'd': 0.03125, 'g': 0.03125, 'f': 0.03125, 'i': 0.03125, 'h': 0.03125, 'k': 0.03125, 'j': 0.03125, 'm': 0.03125, 'l': 0.03125, 'o': 0.03125, 'n': 0.03125, 'q': 0.03125, 'p': 0.03125, 's': 0.03125, 'r': 0.03125, 'u': 0.03125, 't': 0.03125, 'w': 0.03125, 'v': 0.03125, 'y': 0.03125, 'x': 0.03125, 'z': 0.03125}

    file=r"simple-20160801-1-article-per-line"
    zipf_file=r"zipf2.txt"
    uniform_file=r"uniform2.txt"

    text = open(file, 'r', encoding='utf-8').read()
    n = len(text)

    write_file(zipf_file)
    write_file(uniform_file)

    generate_chars(zipf_file,zipf_probabilities, n)
    generate_chars(uniform_file,uniform_probabilities, n)



