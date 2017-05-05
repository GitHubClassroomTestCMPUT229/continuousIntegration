import spimgrader
import subprocess
import os

def main():
    # Call spimgrader to apply files to student submissions
    spimgrader.main()
    # After call, results are in ./results
    # Do whatever we need to with the results files
    # eg: Compare them with expected results
    # eg: Send the results to the student
    # eg: Send the results to the teaching team
    files = os.listdir("./results")
    for f in files:
        f = open("./results/" + f, "r")
        print(f.read())

if __name__ == "__main__":
    main()
