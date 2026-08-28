import os, sys

# This imports from a file that will be present in the
# grading system. No need to alter for local testing -
# if the file isn't present then these lines are skipped
try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass

# ----------------------------------------
# This function, grader.call_grader() (which will be
# present with our code when it is submitted to the
# grading system), takes an integer index i and returns
# A[i].

# If you pass an invalid index or call this function
# more than 32 times, you'll get back -1
    
# grader.call_grader(int i)
# ----------------------------------------

# For testing on your own system, you can call 
# this function instead.  It uses an array of length 10 
# with values 1000, 2000, 3000, ..., 10,000. 
# Don't forget to switch your code back to calling 
# grader.call_grader() before submitting. 
def call_grader_local(i):
    A = [1000, 2000, 3000, 4000, 5000,
         6000, 7000, 8000, 9000, 10000]
    return A[i]


def closest_index(N, T):
    values = {}

    def value_at(index):
        if index not in values:
            if "grader" in globals():
                values[index] = grader.call_grader(index)
            else:
                values[index] = call_grader_local(index)
        return values[index]

    low = 0
    high = N
    while low < high:
        middle = (low + high) // 2
        if value_at(middle) < T:
            low = middle + 1
        else:
            high = middle

    candidates = []
    if low < N:
        candidates.append(low)
    if low > 0:
        candidates.append(low - 1)

    return min(candidates, key=lambda index: (abs(value_at(index) - T), index))


def main():
    
    # Values for N and T are set in the grading system 
    # through environment variables, if present. 
    # If these aren't present, the default values are N = 10 
    # and T = 8400.

    try:
        N = int(os.environ["N"])
        T = int(os.environ["T"])
    except:
        N = 10
        T = 8400

    # ---------------------------------------- 
    # This is the part of main() you should modify.
    # (you are welcome to write other functions above 
    # and call them here, but all your code should be 
    # submitted in this one file).
    
    my_answer = closest_index(N, T)
    # ----------------------------------------

    # Afterwards, you should print out the value of
    # an index i for which A[i] is closest to T.
    # You should only print this number on standard output,
    # nothing else.
    print(my_answer)

if __name__ == "__main__":
    main()