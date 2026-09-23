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
allocation_order = []  # Track the order players receive slices

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
# this function instead.  Each participant has a
# triangular-shaped value function with uniformly
# spaced peaks, with player 0 having the _last_
# peak and player N-1 having the _first_.  This
# makes the ideal ordering of players N-1...0.
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
    c1 = math.sqrt(v * peak1) if v <= peak1 else 1 - math.sqrt((1 - v) * (1 - peak1))
    c2 = math.sqrt(v * peak2) if v <= peak2 else 1 - math.sqrt((1 - v) * (1 - peak2))
    return -1 if c1 <= c2 else 1


def quickselect_median(players, value_threshold, compare_fn):
    if len(players) == 1:
        return players[0]
    
    pivot_idx = random.randint(0, len(players) - 1)
    pivot = players[pivot_idx]
    left = []
    right = []

    for p in players:
        if p == pivot:
            continue
        if compare_fn(p, pivot, value_threshold) <= 0:
            left.append(p)
        else:
            right.append(p)
    
    median_pos = len(players) // 2
    if len(left) == median_pos:
        return pivot
    elif len(left) > median_pos:
        return quickselect_median(left, value_threshold, compare_fn)
    else:
        return quickselect_median(right, value_threshold, compare_fn)


def divide_conquer(players, value_threshold, compare_fn):
    global allocation_order
    
    if len(players) == 0:
        return []
    
    if len(players) == 1:
        allocation_order.append(players[0])
        return [players[0]]
    
    median_player = quickselect_median(players, value_threshold, compare_fn)
    left_group = []
    right_group = []
    
    for p in players:
        if p == median_player:
            continue
        if compare_fn(p, median_player, value_threshold) <= 0:
            left_group.append(p)
        else:
            right_group.append(p)
    
    result = []
    result.extend(divide_conquer(left_group, value_threshold, compare_fn))
    result.extend(divide_conquer(right_group, value_threshold, compare_fn))
    
    return result


def main():
    global N, allocation_order
    # The values for N is set in the grading system
    # through an environment variable, if present.
    # If not present, feel welcome to set N to
    # any value you want for local testing
    try:
        N = int(os.environ["N"])
    except:
        N = 30  # Set your own value here for local testing if you want

    allocation_order = []
    P = list(range(N))
    compare_func = mycomp
    if N % 2 == 0:
        first_threshold = 0.5
    else:
        first_threshold = math.floor(N / 2.0) / N
    
    result = divide_conquer(P, first_threshold, compare_func)
    print('\n'.join(str(i) for i in result))

if __name__ == "__main__":
    main()