import os, sys, math, random
from functools import cmp_to_key

try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass

N = 0


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

    c1 = math.sqrt(v * peak1) if v <= peak1 \
        else 1 - math.sqrt((1 - v) * (1 - peak1))

    c2 = math.sqrt(v * peak2) if v <= peak2 \
        else 1 - math.sqrt((1 - v) * (1 - peak2))

    return -1 if c1 <= c2 else 1


def quickselect(players, k, v, compare_fn):

    while len(players) > 1:

        pivot = random.choice(players)

        left = []
        right = []

        for p in players:
            if p == pivot:
                continue

            if compare_fn(p, pivot, v) == -1:
                left.append(p)
            else:
                right.append(p)

        if k < len(left):
            players = left

        elif k == len(left):
            return pivot

        else:
            k -= len(left) + 1
            players = right

    return players[0]


def divide_and_conquer(players, start_count, compare_fn):

    m = len(players)

    if m <= 1:
        return players

    left_size = m // 2
    right_size = m - left_size

    split_value = (start_count + left_size) / N

    boundary = quickselect(
        players,
        left_size - 1,
        split_value,
        compare_fn
    )

    left = []
    right = []

    for p in players:
        if p == boundary:
            continue

        if compare_fn(p, boundary, split_value) == -1:
            left.append(p)
        else:
            right.append(p)

    # Boundary belongs to the left group.
    left.append(boundary)

    left_order = divide_and_conquer(
        left,
        start_count,
        compare_fn
    )

    right_order = divide_and_conquer(
        right,
        start_count + left_size,
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

    # For Gradescope:
    compare_fn = mycomp

    # For local testing:
    # compare_fn = compare_local

    P = divide_and_conquer(
        P,
        0,
        compare_fn
    )

    print('\n'.join(str(i) for i in P))


if __name__ == "__main__":
    main()