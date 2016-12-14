from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def readWords(file):
    f = open(file, 'r', encoding='utf-8')
    allWords = []
    for line in f:
        line = line[:-1]
        words = line.split()
        allWords.extend(words)
    return allWords

if __name__ == '__main__':

    file=r"simple-20160801-1-article-per-line"
    zipf_file=r"zipf2.txt"
    uniform_file=r"uniform2.txt"

    words_original = readWords(file)
    words_zipf = readWords(zipf_file)
    words_uniform = readWords(uniform_file)

    c_original = Counter(words_original)
    c_zipf = Counter(words_zipf)
    c_uniform = Counter(words_uniform)
    words_o, frequencies_o = zip(*c_original.most_common())
    words_z, frequencies_z = zip(*c_zipf.most_common())
    words_u, frequencies_u = zip(*c_uniform.most_common())

    cumsum_o = np.cumsum(frequencies_o)
    normedcumsum_o = [x / float(cumsum_o[-1]) for x in cumsum_o]
    # wrank_o = {words_o[i]:i+1 for i in range(0,len(words_o))}

    cumsum_z = np.cumsum(frequencies_z)
    normedcumsum_z = [x / float(cumsum_z[-1]) for x in cumsum_z]
    # wrank_z = {words_z[i]:i+1 for i in range(0,len(words_z))}

    cumsum_u = np.cumsum(frequencies_u)
    normedcumsum_u = [x / float(cumsum_u[-1]) for x in cumsum_u]
    # wrank_u = {words_u[i]:i+1 for i in range(0,len(words_u))}

    rank_o = [i + 1 for i in range(0, len(words_o))]
    rank_z = [i + 1 for i in range(0, len(words_z))]
    rank_u = [i + 1 for i in range(0, len(words_u))]

    # Word rank - Frequency
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(rank_o, frequencies_o, label='original')
    ax.plot(rank_z, frequencies_z, label='generated zipf')
    ax.plot(rank_u, frequencies_u, label='generated uniform')

    # Now add the legend with some customizations.
    legend = ax.legend(loc='upper right', shadow=True)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylabel(r"Frequency", fontsize=16, color="blue")
    ax.set_xlabel(r"Word rank", fontsize=16, color="blue")

    plt.show()

    # CDF
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(rank_o, normedcumsum_o, label='original')
    ax.plot(rank_z, normedcumsum_z, label='generated zipf')
    ax.plot(rank_u, normedcumsum_u, label='generated uniform')

    # Now add the legend with some customizations.
    legend = ax.legend(loc='lower right', shadow=True)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylabel(r"CDF", fontsize=16, color="blue")
    ax.set_xlabel(r"Word rank", fontsize=16, color="blue")

    plt.show()

    # Max point-wise distance
    d_zipf = max(map(lambda p: abs(p[0] - p[1]), (zip(normedcumsum_o, normedcumsum_z))))
    d_uniform = max(map(lambda p: abs(p[0] - p[1]), (zip(normedcumsum_o, normedcumsum_u))))

    print('Zipf:', d_zipf)
    print('\nUniform', d_uniform)
