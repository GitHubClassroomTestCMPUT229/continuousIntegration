import subprocess

# Use subprocess to invoke the Make process for SPIM.  If successful, we will have spim 
# installed remotely in the Travis build environment each time the student submits their
# code.
def main():
    subprocess.call(["./spim-8.0/spim/make", "spim"])
    subprocess.call(["./spim-8.0/spim/make", "install"])

if __name__ == "__main__":
    main()
