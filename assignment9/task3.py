from tqdm import tqdm

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


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


def dijkstra(matrix, s):
    """
    Calculates Dijkstra and reports to a common progress bar.
    :param matrix: The matrix representation of the graph
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

    return {k: v for k, v in res.items() if v != inf}


def uow(matrix, n):
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print('progress: %.3f' % (n / len(matrix)))
    return max(dijkstra(matrix, n).values())


def diameter(matrix):
    """
    The diameter is the longest shortest path in the graph. Dijkstra returns a
    map from node to distance. The maximum value is the longest shortest path
    for one node. The maximum off this value over all nodes returns the diameter
    of the graph.
    :param matrix: The matrix representing the graph.
    :return: Returns the diameter as an integer.
    """

    from concurrent.futures import ProcessPoolExecutor
    from functools import partial

    # Execute on a process pool
    with ProcessPoolExecutor(max_workers=8) as executor:
        # Bind the unit of work: for a node, Dijkstra's algorithm is
        # executed to find all shortest paths; then, the maximum from the
        # values is taken. Pulling this into the unit of work allows to free
        # the memory of the distance dictionary. This should keep the memory
        # overhead low.
        return max(executor.map(partial(uow, matrix), matrix.keys()))


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
