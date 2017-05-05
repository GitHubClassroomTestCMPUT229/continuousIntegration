import subprocess

# Use subprocess to invoke the Make process for SPIM.  If successful, we will have spim 
# installed remotely in the Travis build environment each time the student submits their
# code.

# Resource for altering working directory within Python:
# http://stackoverflow.com/questions/21406887/subprocess-changing-directory
# User: glglgl
def main():
    subprocess.call("test.sh", cwd="./spim/spim/")
    # subprocess.call(["./spim/spim/make", "spim"], cwd="./spim/spim/")
    # subprocess.call(["./spim/spim/make", "install"], cwd="./spim/spim/")

if __name__ == "__main__":
    main()
