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

    left = 0
    right = N - 1
    
    while left < right:
        mid = (left + right) // 2
        mid_value = grader.call_grader(mid)
        
        if mid_value < T:
            left = mid + 1
        else:
            right = mid
    
    my_answer = left
    closest = abs(grader.call_grader(left) - T)
    
    if left > 0:
        left_value = grader.call_grader(left - 1)
        left_distance = abs(left_value - T)
        if left_distance < closest:
            my_answer = left - 1

    print(my_answer)

if __name__ == "__main__":
    main()