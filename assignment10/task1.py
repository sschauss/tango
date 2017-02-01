from collections import Counter
from math import log2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

data = pd.read_csv('onlyhash.data', sep='\t', names=['user', 'date', 'tags'])


def entropy(vector):
    size = vector.size
    frequencies = Counter(vector).values()
    probabilities = list(map(lambda frequency: frequency / size, frequencies))
    return - sum(map(lambda p: log2(p) * p, probabilities))


date_to_tweets = dict(list(data.groupby('date')))
date_to_user_to_tweets = {date: dict(list(tweets.groupby('user'))) for date, tweets in date_to_tweets.items()}

date_to_system_entropy = {date: entropy(tweets['tags']) for date, tweets in date_to_tweets.items()}

date_to_mean_user_entropy = {date: np.mean([entropy(tweets['tags']) for user, tweets in user_to_tweets.items()]) for
                             date, user_to_tweets in date_to_user_to_tweets.items()}

dates = list(sorted(date_to_tweets.keys()))[46:-3]
years = YearLocator()
months = MonthLocator()
yearsFmt = DateFormatter('%Y')
fig, ax = plt.subplots()
fig.suptitle('system entropy and average user entropy over time')
ax.plot_date(dates, [date_to_system_entropy[date] for date in dates], '-', label='system entropy', color='#F44336')
ax.plot_date(dates, [date_to_mean_user_entropy[date] for date in dates], '-', label='average user entropy',
             color='#3F51B5')
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(months)
ax.autoscale_view()
ax.fmt_xdata = DateFormatter('%Y-%m-%d')
ax.set_xlabel('Time')
ax.set_ylabel('Entropy')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
