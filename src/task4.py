
# coding: utf-8

# In[61]:

import random

randlist = list(map(lambda x: random.randint(0,90), range(10)))
randlist.sort()

import math

sin = list(map(math.sin, randlist))
cos = list(map(math.cos, randlist))
import matplotlib.pyplot as plt

plt.plot(randlist,sin, marker='o',color='r',linestyle='-', label="sine")
plt.plot(randlist,cos, marker='o',color='b',linestyle='-', label="cosine")
plt.ylabel('sin, cos values')
plt.xlabel('random numbers')

plt.ylim([-1.2, 1.2])
plt.xlim([0, 120])

plt.legend(loc=1, borderaxespad=0, numpoints=1)
plt.show()


# In[ ]:



