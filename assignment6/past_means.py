from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


def fst(item):
    """Function to get the first element."""
    return item[0]


def snd(item):
    """Function to get the second element."""
    return item[1]


def prepare_hist(counter):
    """Prepares the histogram by unrolling a counter into domain and the mapped value."""
    ordered = sorted(counter.items(), key=fst)
    return np.fromiter(map(fst, ordered), float), np.fromiter(map(snd, ordered), float)


def flatten_counter(counter):
    """Flattens the counter, repeats in a list the elements as often as mentioned in the counter.
    Counter(xs) == Counter(flatten_counter(Counter(xs))) should hold.
    """
    return [k for k, v in counter.items() for _ in range(0, v)]


if __name__ == '__main__':
    print("The file 'simple-20160801-1-article-per-line' should exist in the working directory.")

    # Set up counters for sentences in the appropriate categories
    past = Counter()
    present = Counter()

    # Count in present and past
    with open("simple-20160801-1-article-per-line", "r") as file:
        for line in file:
            article = line.split('.', maxsplit=1)[0].lower()
            x = max(article.find("was"), article.find("were"))
            y = max(article.find("is"), article.find("are"))

            if x >= 0 and not y >= 0:
                past[line.count(" ")] += 1
            else:
                present[line.count(" ")] += 1

    # Flatten for numpy calculations
    flat_past = flatten_counter(past)
    flat_present = flatten_counter(present)
    flat_all = flat_past + flat_present

    # Prepare histograms
    past_x, past_w = prepare_hist(past)
    present_x, present_w = prepare_hist(present)

    # Calculate mean values
    past_mean = np.mean(flat_past)
    present_mean = np.mean(flat_present)
    all_mean = np.mean(flat_all)

    # Make subranges and labels
    xs = (past_x, present_x)
    ws = (past_w, present_w)
    ls = ("Past", "Present")

    # Plot appropriately
    plt.hist(xs, weights=ws, label=ls, bins=np.arange(0, 500, 5), color="rg")
    plt.axvline(past_mean, color="r", label="mean past")
    plt.axvline(present_mean, color="g", label="mean present")
    plt.axvline(all_mean, color="b", label="mean all")
    plt.legend()
    plt.show()
