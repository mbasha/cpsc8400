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
    c1 = math.sqrt(v * peak1) if v <= peak1 else 1 - math.sqrt((1 - v) * (1 - peak1))
    c2 = math.sqrt(v * peak2) if v <= peak2 else 1 - math.sqrt((1 - v) * (1 - peak2))
    return -1 if c1 <= c2 else 1

def quickselect_min(players, value_threshold, compare_fn):
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
    
    if len(left) == 0:
        return pivot
    else:
        return quickselect_min(left, value_threshold, compare_fn)

def fair_division(players, remaining_value, compare_fn):
    if len(players) == 0:
        return []
    
    if len(players) == 1:
        return [players[0]]
    
    value_per_player = remaining_value / len(players)
    min_player = quickselect_min(players, value_per_player, compare_fn)
    
    remaining_players = [p for p in players if p != min_player]
    result = [min_player]
    result.extend(fair_division(remaining_players, remaining_value - value_per_player, compare_fn))
    
    return result

def main():
    global N
    
    try:
        N = int(os.environ["N"])
    except:
        N = 30

    P = list(range(N))
    compare_func = mycomp
    result = fair_division(P, 1.0, compare_func)
    
    print('\n'.join(str(i) for i in result))

if __name__ == "__main__":
    main()