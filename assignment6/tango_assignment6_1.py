
# coding: utf-8

# In[29]:

file=r"simple-20160801-1-article-per-line"

def readWordsFromWiki (filename):
    f=open(filename,'r',encoding='utf-8')
    allWords=[]
    for line in f:
        line=line[:-1]
        words=line.split()
        allWords.extend(words)
    f.close()
    return len(allWords)

words=readWordsFromWiki(file)


# In[31]:

import re

# Get rid of empty lines
def get_lines_notEmpty (filename): 
    f = open(filename,'r',encoding='utf-8')
    contents = f.readlines()
    f.close()

    file_content = []
    for line in contents:
        # Strip whitespace, should leave nothing if empty line was just "\n"
        if re.match(r'^\s*$', line):
            continue
        # We got something, save it
        else:
            file_content.append(line)
    return file_content

def get_lines (filename):
    f = open(filename,'r',encoding='utf-8')
    contents = f.readlines()
    f.close()
    return contents

Lines = get_lines(file)
Lines_notEmpty = get_lines_notEmpty(file)

count_lines_notEmpty = len(Lines_notEmpty)
count_lines = len(Lines)


# In[32]:

print("Empty lines: ",count_lines - count_lines_notEmpty)


# In[33]:

def calc_ari(numChars,numWords,numSentences):
    ari = 0
    if (numWords != 0 and numSentences != 0):
        ari = 4.71*(float(numChars)/numWords) + 0.5*float(numWords)/numSentences - 21.43
    return ari

count_words=[]
count_sentences=[]
count_characters=[]
count_ari=[]
for line in Lines_notEmpty:
        
        sentences=re.findall('\s*([^.?!]+)[.?!]',line)
        line.split(".")
        numSentences=len(sentences)
        count_sentences.append(numSentences)
        
        words=re.findall('\w+',line)
        numWords=len(words)
        count_words.append(numWords)
        
        numChars=0
        for word in words:
            numChars = numChars + len(word) 
        count_characters.append(numChars)  

        ari=calc_ari(numChars,numWords,numSentences)
        count_ari.append(ari)


# In[80]:

ax = subplot(111)
ax.scatter(df['Characters'], df['Ari'])
ax.set_ylim([0, 14])
ax.set_xscale('log')
show()


# In[ ]:



