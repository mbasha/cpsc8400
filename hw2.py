import os, sys, math, random
from functools import cmp_to_key

try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass


N = 0 # problem size


def mycomp(p1, p2, v):
    return grader.compare(p1, p2, v)

def compare_local(player1, player2, v):
    global N

    if player1 < 0 or player1 >= N:
        print('Invalid value of player1!')
        sys.exit(0)

    if player2 < 0 or player2 >= N:
        print('Invalid value of player2!')
        sys.exit(0)

    if v < 0 or v > 1:
        print('Invalid value of v!')
        sys.exit(0)

    peak1 = 1.0 - (1.0 + player1) / (1.0 + N)
    peak2 = 1.0 - (1.0 + player2) / (1.0 + N)

    c1 = (
        math.sqrt(v * peak1)
        if v <= peak1
        else 1 - math.sqrt((1 - v) * (1 - peak1))
    )

    c2 = (
        math.sqrt(v * peak2)
        if v <= peak2
        else 1 - math.sqrt((1 - v) * (1 - peak2))
    )

    return -1 if c1 <= c2 else 1


# ---------------------------------------------------------
# Randomized quickselect
# ---------------------------------------------------------
def quickselect(players, k, v, compare_fn):

    while len(players) > 1:

        pivot = players[random.randint(0, len(players) - 1)]

        less = []
        greater = []

        for p in players:
            if p == pivot:
                continue

            if compare_fn(p, pivot, v) == -1:
                less.append(p)
            else:
                greater.append(p)

        # The pivot is the k-th element.
        if k == len(less):
            return pivot

        # Desired element is in the left partition.
        elif k < len(less):
            players = less

        # Desired element is in the right partition.
        else:
            k = k - len(less) - 1
            players = greater

    return players[0]


# ---------------------------------------------------------
# Divide-and-conquer fair division
# ---------------------------------------------------------
def fair_division(players, side, compare_fn):

    m = len(players)

    # Base case
    if m <= 1:
        return players

    # Number of players in the left and right groups.
    left_size = m // 2
    right_size = m - left_size

    if side == 0:
        v = left_size / N
    else:
        v = 1.0 - (right_size / N)

    # Find the last player belonging to the left group.
    boundary = quickselect(
        players,
        left_size - 1,
        v,
        compare_fn
    )

    left = []
    right = []

    # Partition around the boundary player.
    for p in players:

        if p == boundary:
            continue

        if compare_fn(p, boundary, v) == -1:
            left.append(p)
        else:
            right.append(p)

    # Boundary belongs to the left group.
    left.append(boundary)

    # Recursively solve both sides.
    left_order = fair_division(
        left,
        0,
        compare_fn
    )

    right_order = fair_division(
        right,
        1,
        compare_fn
    )

    return left_order + right_order


def main():
    global N

    try:
        N = int(os.environ["N"])
    except:
        N = 30

    P = list(range(N))

    # switch 'mycomp' to 'compare_local' for local testing
    compare_fn = mycomp

    P = fair_division(P, 0, compare_fn)

    print('\n'.join(str(i) for i in P))


if __name__ == "__main__":
    main()