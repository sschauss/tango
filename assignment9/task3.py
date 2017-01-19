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
    result = dict()  # parseMatrix()

    # Initialize the matrix
    for node, row in dataset.iterrows():
        n1 = fwd.get(node)
        result[n1, n1] = 0
        for edge in row.out_links:
            n2 = fwd.get(edge)
            if n2 is not None:
                result[n1, n2] = 1

    return result, fwd, bwd


def all_pairs_shortest_path(matrix, vs, inf=999999999):
    """
    Updates all pairs shortest path using the Floyd-Warshall algorithm
    :param matrix: The matrix of distance values to compute in, assumed
    to contain m(x, x)=0.
    :param vs: The domain of vertices
    :param inf: The value to use for unconnected nodes, needs to be
    greater than every potential path
    :return: Returns None
    """
    from time import sleep, time
    from concurrent.futures import ThreadPoolExecutor

    def probe_hop(mid):
        """
        For a fixed middle mode probes all hops
        :param mid: The middle node to probe
        :return: Returns None
        """
        for source in vs:
            to_mid = matrix.get((source, mid), inf)
            for target in vs:
                direct = matrix.get((source, target), inf)
                from_mid = matrix.get((mid, target), inf)
                if direct > to_mid + from_mid:
                    matrix[source, target] = to_mid + from_mid

    # Use a thread pool executor for independent variables
    with ThreadPoolExecutor() as executor:
        # Submit all vertices to middle hop probe
        futures = [executor.submit(probe_hop, mid) for mid in vs]

        # Wait and print status every some seconds
        dispatched = len(futures)
        completed = 0
        started = time()
        while dispatched > completed:
            # Get some statistics
            completed = sum(1 for x in futures if x.done())
            working = sum(1 for x in futures if x.running())
            percentage = (100. * completed / dispatched)
            duration = time() - started

            # Print data
            print("%d/%d hops probed (%.2f%%), %d working (%.1fs)"
                  % (completed, dispatched, percentage, working, duration))

            # Sleep for 5 seconds
            sleep(5)


def task3():
    """
    Reads link data, calculates all pairs shortest path and selects the longest shortest path
    :return: Returns None
    """

    # Read the data and the mapping
    matrix, fwd, _ = read_input()

    # Find all pairs' shortest path
    all_pairs_shortest_path(matrix, fwd.values())

    # Since all paths are the shortest, the maximum value is the longest shortest path
    diameter = max(matrix.values())

    # Print the output
    print("The diameter is %d" % diameter)


if __name__ == "__main__":
    task3()
