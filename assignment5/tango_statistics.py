import json
import pandas
import numpy as np
from matplotlib import pyplot as plot
from urllib.parse import urlparse

statistics_path = './statistics.json'
url = urlparse('http://141.26.208.82/articles/g/e/r/Germany.html')

def load_statistics():
    with open(statistics_path, 'r') as f:
        return json.load(f)

def filter_accessible_links(stats):
    return {k: [urlparse(i) for i in v] for k, v in stats.items() if isinstance(v, list)}

def filter_dead_links(stats):
    return {k: v for k, v in stats.items() if isinstance(v, str)}

statistics = load_statistics()

accessible_links = filter_accessible_links(statistics)
dead_links = filter_dead_links(statistics)

print('total number of webpages:', len(accessible_links))

links_per_link = [(len(v)) for k, v in accessible_links.items()]

total_links = sum(links_per_link)
print('total number of links', total_links)

average_per_webpage = np.mean(links_per_link)
print('average number of links', average_per_webpage)

median_per_webpage = np.median(links_per_link)
print('average number of links', median_per_webpage)

internal_to_external = [(len([i for i in v if i.netloc == url.netloc]), 
                         len([i for i in v if i.netloc != url.netloc])) for k, v in accessible_links.items()]
internal_urls = [i for i, e in internal_to_external]
external_urls = [e for i, e in internal_to_external]

print(sum(internal_urls))
print(sum(external_urls))

plot.scatter(internal_urls, external_urls)
plot.xlabel("internal URLs")
plot.ylabel("external URLs")
plot.title("Distribution")
plot.xlim((0, max(internal_urls)))
plot.ylim((0, max(external_urls)))
plot.show()
