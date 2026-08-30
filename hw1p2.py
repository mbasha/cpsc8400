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
# more than 64 times, you'll get back -1

# grader.call_grader(i)
# ----------------------------------------

# For testing on your own system, you can call 
# this function instead. It uses an array of length 100
# with values 0, 100, 200, 8300, 8400, 8300, 8200, ...
# Don't forget to switch your code back to calling 
# grader.call_grader() before submitting. 
def call_grader_local(i):
    return 8400 - abs(84-i)*100

def main():
    
    # Value for N is set in the grading system
    # through an environment variable, if present.
    # If this isn't present, the default values is N = 100

    try:
        N = int(os.environ["N"])
    except:
        N = 100

    left = 0
    right = N - 1
    
    while right - left > 2:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        
        val1 = grader.call_grader(mid1)
        val2 = grader.call_grader(mid2)
        
        if val1 > val2:
            right = mid2 - 1
        else:
            left = mid1 + 1
    
    # Check remaining elements
    my_answer = left
    max_val = grader.call_grader(left)
    
    for i in range(left + 1, right + 1):
        value = grader.call_grader(i)
        if value > max_val:
            my_answer = i
            max_val = value

    print(my_answer)

if __name__ == "__main__":
    main()