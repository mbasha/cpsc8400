import os, sys, random

# This imports from a file that will be present in the
# grading system. No need to alter for local testing -
# if the file isn't present then these lines are skipped
try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass

# ----------------------------------------
# This function (which will be compiled with our code
# when it is submitted to the grading system) takes
# a list of values of x and returns a list of
# values of f(x) for all of them.

# If you pass it a list of length more than K,
# you'll only get back the first K answers.
# If you call it more than R times, you'll start to
# get back empty lists.
# If you pass any values of x outside [0,1], you'll
# get back corresponding values of -1.

# grader.call_grader(x)
# ----------------------------------------

# For testing on your own system, you can call 
# this function instead. It uses an array of length 100
# with values 0, 100, 200, 8300, 8400, 8300, 8200, ...
# Don't forget to switch your code back to calling 
# grader.call_grader() before submitting. 
def call_grader_local(x):
    result = []
    for i in range(len(x)):
        result.append(1.0 - abs(x[i] - 0.8400))
    return result

def main():
    
    # Values for K and R are set in the grading system
    # through environment variables, if present.
    # If these aren't present, the default values are K = 4, R = 7

    try:
        K = int(os.environ["K"])
        R = int(os.environ["R"])
    except:
        K = 4
        R = 7

    left = 0.0
    right = 1.0
    my_answer = 0.5
    best = -1.0
    
    for round_num in range(R):
        x = []
        for j in range(K):
            x.append(left + (right - left) * (j + 1) / (K + 1))
        
        y = call_grader_local(x)
        
        best_idx = -1
        for j in range(K):
            if y[j] > best:
                best = y[j]
                my_answer = x[j]
                best_idx = j

        if best_idx >= 0:
            margin = (right - left) / (2 * K)
            left = max(0.0, x[best_idx] - margin)
            right = min(1.0, x[best_idx] + margin)

    print(my_answer)

if __name__ == "__main__":
    main()