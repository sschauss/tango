import concurrent.futures
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import Counter

def repeat(n, fn):
    return list(map(lambda _: fn(), range(0, n)))


def cdf(lst):
    numbers, frequencies = zip(*sorted(Counter(lst).items()))
    cumsum = np.cumsum(frequencies)
    normed_cumsum = [x / float(cumsum[-1]) for x in cumsum]
    return numbers, normed_cumsum


class DiceModel:
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


class DiceSumModel:
    def __init__(self, rolls, dices):
        self.rolls = rolls
        self.dices = [DiceModel() for _ in range(0, dices)]

    def evaluate(self):
        results = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_dice = {executor.submit(repeat, self.rolls, dice.roll): dice for dice in self.dices}
            for future in concurrent.futures.as_completed(future_to_dice):
                dice = future_to_dice[future]
                result = future.result()
                results[dice] = result
        return list(map(sum, (zip(*results.values()))))

def task_3_1():
    sums = DiceSumModel(100, 2).evaluate()
    plt.hist(sums, bins=range(2, 14), align='left', color='#F44336')
    plt.title('Two Dice Rolls (n=100) (Task 3.1)')
    plt.xlabel('Sum')
    plt.ylabel('Frequency')
    plt.show()
    return sums


def task_3_2(task_3_1_sums):
    task_3_2_eyes, task_3_2_cdf = cdf(task_3_1_sums)
    plt.bar(task_3_2_eyes, task_3_2_cdf, align='center', alpha=0.5, color='#F44336')
    plt.plot(task_3_2_eyes, task_3_2_cdf, color='#F44336')
    plt.title('Two Dice Rolls (n=100) (Task 3.2)')
    plt.xlabel('Sum')
    plt.ylabel('Cumulative Probability')
    plt.show()


def task_3_3(task_3_1_sums):
    task_3_3_eyes, task_3_3_cdf = cdf(task_3_1_sums)
    median = np.median(task_3_1_sums)
    leq_9_prob = task_3_3_cdf[task_3_3_eyes.index(9)]
    plt.bar(task_3_3_eyes, task_3_3_cdf, align='center', alpha=0.5, color='#F44336')
    plt.plot(task_3_3_eyes, task_3_3_cdf, color='#F44336')
    plt.axvline(x=median, c='#2196F3', label='median', lw=1)
    plt.axhline(y=leq_9_prob, c='#8BC34A', label='P(X <= 9)', lw=1)
    plt.title('Two Dice Rolls (n=100) (Task 3.3)')
    plt.xlabel('Sum')
    plt.ylabel('Cumulative Probability')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    print('Task 3.3 median: %s' % median)
    print('Task 3.3 P(X <= 9): %s' % leq_9_prob)
    plt.show()


def task_3_4(task_3_1_sums):
    task_3_4_sums = DiceSumModel(100, 2).evaluate()
    task_3_1_eyes, task_3_1_cdf = cdf(task_3_1_sums)
    task_3_4_eyes, task_3_4_cdf = cdf(task_3_4_sums)
    task_3_4_max_pwd = max(map(lambda p: abs(p[0] - p[1]), (zip(task_3_1_cdf, task_3_4_cdf))))
    print('Task 3.4 maximum point wise distance: %s' % task_3_4_max_pwd)


def task_3_5():
    task_3_5_1_sums = DiceSumModel(1000, 2).evaluate()
    task_3_5_2_sums = DiceSumModel(1000, 2).evaluate()
    task_3_5_1_eyes, task_3_5_1_cdf = cdf(task_3_5_1_sums)
    task_3_5_2_eyes, task_3_5_2_cdf = cdf(task_3_5_2_sums)
    task_3_4_max_pwd = max(map(lambda p: abs(p[0] - p[1]), (zip(task_3_5_1_cdf, task_3_5_2_cdf))))
    print('Task 3.5 maximum point wise distance: %s' % task_3_4_max_pwd)


if __name__ == "__main__":
    task_3_1_sums = task_3_1()
    task_3_2(task_3_1_sums)
    task_3_3(task_3_1_sums)
    task_3_4(task_3_1_sums)
    task_3_5()

