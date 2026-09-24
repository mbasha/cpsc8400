import os, sys, math, random
from functools import cmp_to_key

# This imports from a file that will be present in the
# grading system. No need to alter for local testing -
# if the file isn't present then these lines are skipped
try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass


N = 0 # problem size


def mycomp(p1, p2, v):
    # This function, grader.compare() (which will be
    # present alongside your code when it is submitted
    # to the grading system) takes a value v and compares
    # the cutoff points c1 and c2 for two players. These
    # cutoff points are such that exactly v units of
    # value are in [0,c1] and [0,c2] respectively for
    # for players 1 and 2.  The return value is -1 if
    # if c1<=c2 and +1 otherwise.

    # If your comparisons don't look like you are
    # performing randomized quickselect, this function
    # will notify the grader accordingly and your
    # solution will receive a deduction of -25 points.
    return grader.compare(p1, p2, v)


# For testing on your own system, you can call
# this function instead. Each participant has a
# triangular-shaped value function with uniformly
# spaced peaks, with player 0 having the _last_
# peak and player N-1 having the _first_.
# This makes the ideal ordering of players N-1...0.
#
# Don't forget to switch your code back to calling
# grader.compare() before submitting.
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

    # -----------------------------------------------------
    # Determine the cutoff value used for this split.
    #
    # side == 0:
    #     We are determining the left/prefix group.
    #
    # side == 1:
    #     We are determining the right/suffix group.
    # -----------------------------------------------------
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

    # The value for N is set in the grading system
    # through an environment variable, if present.
    # If not present, feel welcome to set N to
    # any value you want for local testing.
    try:
        N = int(os.environ["N"])
    except:
        N = 30  # Set your own value here for local testing if you want

    # ----------------------------------------
    # This is the part of main() you should modify.
    # (you are welcome to write other functions above
    # and call them here, but all your code should be
    # submitted in this one file).

    P = list(range(N)) # creates a list of integers from 0 to N-1

    # switch 'mycomp' to 'compare_local' for local testing
    compare_fn = mycomp

    P = fair_division(P, 0, compare_fn)

    # ----------------------------------------

    # At the end, you should print out the order of
    # the players for their allocations. Each player
    # is an integer index in the range 0 .. N-1.
    # You should just print these N numbers, separated
    # by whitespace, and nothing else.
    print('\n'.join(str(i) for i in P))


if __name__ == "__main__":
    main()