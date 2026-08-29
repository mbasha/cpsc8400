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

    my_answer = 50

    # ---------------------------------------- 
    # This is the part of main() you should modify.
    # (you are welcome to write other functions above 
    # and call them here, but all your code should be 
    # submitted in this one file).

    m = 0.0;
    for i in range(N):
        value = call_grader_local(float(i)) # call_grader_local needs to be switched to grader.call_grader when you submit!!
        if value == -1:
            break
        if value > m :
            my_answer = i
            m = value
    
    # ----------------------------------------

    # Afterwards, you should print out the value of
    # an index i for which A[i] is closest to the maximum.
    # You should only print this number on standard output,
    # nothing else.
    print(my_answer)

if __name__ == "__main__":
    main()