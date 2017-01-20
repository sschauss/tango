from tqdm import tqdm


def read_input():
    """
    Reads the input data and returns a matrix representing
    the graph, as well as node->index and index->node mapping.
    :return: Returns a matrix and two mappings
    """
    from pandas import read_hdf

    # Read the data set, remove some duplicate rows, and set index.
    dataset = read_hdf("store.h5", "df2")
    dataset.drop_duplicates("name", inplace=True)
    dataset.set_index("name", inplace=True, verify_integrity=True)

    # Make forward and backward node mapping dicts
    bwd = dict()
    fwd = dict()

    index = 0
    for n in dataset.index:
        bwd[index] = n
        fwd[n] = index
        index += 1

    # Create the matrix
    result = dict()

    # Initialize the matrix
    for node, row in tqdm(dataset.iterrows(),
                          total=dataset.size,
                          desc="Preparing matrix",
                          unit="row"):
        # Map first node
        n1 = fwd.get(node)
        for edge in row.out_links:
            # Map second node
            n2 = fwd.get(edge)
            if n2 is not None:

                # Add a connection, create a new row if not present
                row = result.get(n1)
                if row is None:
                    row = {n2: 1}
                    result[n1] = row
                else:
                    row[n2] = 1

    # Return the matrix and the node mapping rules
    return result, fwd, bwd


def dijkstra(matrix, progress, allocated, s):
    """
    Calculates Dijkstra and reports to a common progress bar.
    :param matrix: The matrix representation of the graph
    :param progress: The Progress to report to
    :param allocated: The allocated maximum units of work
    :param s: The node to start from
    :return: Returns the distance dictionary for node s
    """
    from heapq import heappush, heappop

    # Value greater than everything else, not necessarily infinity
    inf = len(matrix) + 1

    # Initialize result vector and queue
    res = {}
    queue = []

    # Set initial distances
    for v in matrix:
        res[v] = inf
    res[s] = 0

    heappush(queue, (res[s], s))

    # Maximum units of work
    while queue:
        d, u = heappop(queue)

        if d < res[u]:
            res[u] = d

        for v in matrix[u]:
            x = res[u] + matrix[u][v]
            if res[v] > x:
                res[v] = x
                heappush(queue, (x, v))

        # Update one, we might finish earlier
        progress.update()
        allocated -= 1

    # Update the remaining ticks
    progress.update(allocated)

    return res


def diameter(matrix):
    """
    The diameter is the longest shortest path in the graph. Dijkstra returns a
    map from node to distance. The maximum value is the longest shortest path
    for one node. The maximum off this value over all nodes returns the diameter
    of the graph.
    :param matrix: The matrix representing the graph.
    :return: Returns the diameter as an integer.
    """

    from concurrent.futures import ThreadPoolExecutor
    from math import log

    capital_e = sum(len(v) for v in matrix.values())
    capital_v = len(matrix)
    units = int(capital_e + capital_v * log(capital_v))

    # Execute on a thread pool
    with ThreadPoolExecutor(max_workers=8) as executor:
        # Report using TQDM
        with tqdm(
                desc="APSP calculation",
                smoothing=.01,
                total=len(matrix) * units) as progress:
            # Bind the unit of work: for a node, Dijkstra's algorithm is
            # executed to find all shortest paths; then, the maximum from the
            # values is taken. Pulling this into the unit of work allows to free
            # the memory of the distance dictionary. This should keep the memory
            # overhead low.
            def uow(n):
                return max(dijkstra(matrix, progress, units, n).values())

            return max(executor.map(uow, matrix.keys()))


def task3():
    """
    Reads link data, calculates all pairs shortest path and selects the longest
    shortest path.
    :return: Returns None
    """

    # Read the data and the mapping
    matrix, _, _ = read_input()
    print(diameter(matrix))


if __name__ == "__main__":
    task3()
