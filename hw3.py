import os, sys
from functools import cmp_to_key

# This imports from a file that will be present in the
# grading system. No need to alter for local testing -
# if the file isn't present then these lines are skipped

grader = None

try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass


N = 0   # number of points
D = 0   # dimensionality of space
K = 0   # number of nearest neighbors to find for each point


# ----------------------------------------
# LOCAL TESTING FUNCTIONS
# ----------------------------------------

def get_class_local(index):
    if index < 0 or index >= 8:
        print('get_class_local: Invalid point index!')
        sys.exit(0)

    return 1 if index < 4 else -1


def get_coord_local(i, j):
    pts = [[0.0,0.0], [4.0,0.0], [4.0,3.0], [0.0,3.0],
           [3.0,1.0], [8.0,1.0], [8.0,4.0], [3.0,4.0]]
    if i < 0 or i >= 8:
        print('get_coord_local: Invalid point index!')
        sys.exit(0)

    if j < 0 or j >= 2:
        print('get_coord_local: Invalid coordinate index!')
        sys.exit(0)

    return pts[i][j]


# ----------------------------------------
# DATA ACCESS FUNCTIONS
# ----------------------------------------

def read_class(index):
    if grader is not None:
        return grader.get_class(index)

    return get_class_local(index)


def read_coord(i, j):
    if grader is not None:
        return grader.get_coord(i, j)

    return get_coord_local(i, j)


# ----------------------------------------
# DISTANCE CALCULATION
# ----------------------------------------

def squared_distance(point_a, point_b):
    """
    Calculate squared Euclidean distance between two points.

    We do not calculate the square root because it does
    not affect which point is closer.
    """

    total = 0.0

    for j in range(D):
        difference = point_a[j] - point_b[j]
        total += difference * difference

    return total


# ----------------------------------------
# KD-TREE CONSTRUCTION
# ----------------------------------------

def build_kd_tree(points):
    global N, D

    left = [-1] * N
    right = [-1] * N
    axes = [0] * N

    def build(indices):
        # Empty collection produces an empty subtree.
        if not indices:
            return -1

        # Find the minimum and maximum coordinate in every dimension for this subtree.
        mins = [float("inf")] * D
        maxs = [float("-inf")] * D

        for idx in indices:
            point = points[idx]

            for dimension in range(D):
                value = point[dimension]

                if value < mins[dimension]:
                    mins[dimension] = value

                if value > maxs[dimension]:
                    maxs[dimension] = value

        # Split along the dimension with the greatest spread.
        axis = max(
            range(D),
            key=lambda dimension: (
                maxs[dimension] - mins[dimension]
            )
        )

        # Sort by the selected coordinate.
        indices.sort(
            key=lambda idx: (points[idx][axis], idx)
        )

        # Select the median point as the current node.
        middle = len(indices) // 2
        node = indices[middle]

        axes[node] = axis

        # Recursively construct the two subtrees.
        left[node] = build(indices[:middle])
        right[node] = build(indices[middle + 1:])

        return node

    root = build(list(range(N)))

    return root, left, right, axes


# ----------------------------------------
# K-NEAREST-NEIGHBOR SEARCH
# ----------------------------------------

def find_k_nearest(
    query_index,
    points,
    root,
    left,
    right,
    axes
):

    query = points[query_index]

    # The list contains at most K candidates.
    # It is maintained in ascending order: (squared distance, original index).

    best = []

    def consider_candidate(node):
        # Do not count the query point as its own neighbor.
        if node == query_index:
            return

        distance = squared_distance(query, points[node])

        candidate = (distance, node)

        if len(best) < K:
            best.append(candidate)
            best.sort()

        elif candidate < best[-1]:
            best[-1] = candidate
            best.sort()

    def search(node):
        # -1 represents an empty subtree.
        if node == -1:
            return

        axis = axes[node]
        split_value = points[node][axis]

        # Determine which side contains the query point. Search that side first.

        if query[axis] < split_value:
            near = left[node]
            far = right[node]

        else:
            near = right[node]
            far = left[node]

        # First, explore the side that is likely to contain closer points.
        search(near)

        # Consider the current node as a neighbor.
        consider_candidate(node)

        # Calculate the squared distance from the query point to the splitting plane.

        difference = query[axis] - split_value
        plane_distance_squared = difference * difference

        if (
            len(best) < K
            or plane_distance_squared <= best[-1][0]
        ):
            search(far)

    search(root)

    return best


# ----------------------------------------
# CLASSIFICATION
# ----------------------------------------

def classify_point(
    query_index,
    points,
    labels,
    root,
    left,
    right,
    axes
):
    neighbors = find_k_nearest(
        query_index,
        points,
        root,
        left,
        right,
        axes
    )

    # Count neighbors belonging to class +1.
    positive_votes = 0

    for distance, neighbor_index in neighbors:
        if labels[neighbor_index] == 1:
            positive_votes += 1

    # K is odd, so the majority class is unambiguous.

    if positive_votes > K // 2:
        return 1

    return -1


# ----------------------------------------
# MAIN
# ----------------------------------------

def main():
    global N, D, K
    try:
        N = int(os.environ["N"])
        D = int(os.environ["D"])
        K = int(os.environ["K"])

    except:
        N = 8
        D = 2
        K = 3

    # ----------------------------------------
    # LOAD THE DATA
    # ----------------------------------------

    # Store the coordinates of every point.
    points = [
        [read_coord(i, j) for j in range(D)]
        for i in range(N)
    ]

    # Store the class of every point.
    labels = [
        read_class(i)
        for i in range(N)
    ]

    # ----------------------------------------
    # BUILD THE KD-TREE
    # ----------------------------------------

    root, left, right, axes = build_kd_tree(points)

    # ----------------------------------------
    # INITIALIZE THE CONFUSION MATRIX
    # ----------------------------------------

    # Row 1: Actual class +1
    # Row 2: Actual class -1
    #
    # Column 1: Predicted class +1
    # Column 2: Predicted class -1

    tp = 0
    fn = 0
    fp = 0
    tn = 0

    # ----------------------------------------
    # CLASSIFY EVERY POINT
    # ----------------------------------------

    for i in range(N):

        # Predict the class using the K nearest
        # neighbors, excluding point i itself.

        predicted = classify_point(
            i,
            points,
            labels,
            root,
            left,
            right,
            axes
        )

        actual = labels[i]

        # Update the appropriate confusion-matrix entry.
        if actual == 1 and predicted == 1:
            tp += 1

        elif actual == 1 and predicted == -1:
            fn += 1

        elif actual == -1 and predicted == 1:
            fp += 1

        else:
            tn += 1

    # ----------------------------------------
    # PRINT THE CONFUSION MATRIX
    # ----------------------------------------

    print(tp, fn)
    print(fp, tn)


if __name__ == "__main__":
    main()