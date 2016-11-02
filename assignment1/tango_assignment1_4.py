
# Maps the values of an empty array of length 10 to a random number between 0 and 90.
import random

randlist = list(map(lambda x: random.randint(0,90), [None] * 10))

# Maps the previous generated random numbers to their sine and cosine values.
import math

sin = list(map(math.sin, randlist))
cos = list(map(math.cos, randlist))

# First plot the values of the sin and cos list, set the line type to dots and define the labels. Then the legend for the labels is created. After that the viewport is defined. Finally the plot is rendered.
import matplotlib.pyplot as plt

plt.plot(sin, "o", label="sine")
plt.plot(cos, "o", label="cosine")

plt.legend(loc=1, borderaxespad=0, numpoints=1)
plt.xlim([-1, 14])
plt.ylim([-5/4, 5/4])
plt.show()
