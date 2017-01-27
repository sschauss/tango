import random
import json
import matplotlib as pl
import matplotlib.pyplot as pp


def gini(sample):
    """
    Calculates the Gini coefficient
    :param sample: The sample to evaluate
    :return: Returns the Gini coefficient
    """
    num = sum(abs(x_i - x_j) for x_i in sample for x_j in sample)
    den = 2 * len(sample) * sum(x_i for x_i in sample)
    return num / den


def generate_chinese_restaurant(customers):
    # First customer always sits at the first table
    tables = [1]
    ginis = [gini([1])]

    # for all other customers do
    for cust in range(2, customers + 1):
        # rand between 0 and 1
        rand = random.random()
        # Total probability to sit at a table
        prob = 0
        # No table found yet
        table_found = False
        # Iterate over tables
        for table, guests in enumerate(tables):
            # calc probability for actual table an add it to
            # total probability
            prob += guests / cust
            # If rand is smaller than the current total prob.,
            # customer will sit down at current table
            if rand < prob:
                # incr. #customers for that table
                tables[table] += 1
                # customer has found table
                table_found = True
                # no more tables need to be iterated, break out
                # for loop
                break
        # If table iteration is over and no table was found, open
        # new table
        if not table_found:
            tables.append(1)

        ginis.append(gini(tables))
    return tables, ginis


restaurants = 1000

network = generate_chinese_restaurant(restaurants)[0]
with open('network_' + str(restaurants) + '.json', 'w') as out:
    json.dump(network, out)

pl.style.use('ggplot')

fig, ax = pp.subplots()
ax.set_xlabel("Run number")
ax.set_ylabel("Gini coefficient")

for run in range(5):
    gini_curve = generate_chinese_restaurant(restaurants)[1]
    xs = range(len(gini_curve))
    ys = gini_curve

    ax.plot(xs, ys, label='Run %d' % run)

ax.legend(loc='lower right')
pp.show()
