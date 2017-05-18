'''
SPIM Auto-grader
Owen Stenson
Grades every file in the 'submissions' folder using every test in the 'samples' folder.
Writes to 'results' folder.
'''
import os, time, re
from subprocess import Popen, PIPE, STDOUT


def run(fn, sample_input='\n'):
    #start process and write input
    proc = Popen(["spim"])
    proc.kill()
    proc = Popen(["spim", "-file", "submissions/"+fn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if sample_input[-1:] != '\n':
        print "Warning: last line (of file below) must end with newline char to be submitted. Assuming it should..."
        sample_input = sample_input + '\n'
    proc.stdin.write(sample_input)
    return proc 

def grade(p, f):
    #arg = process running homework file, file to write results to
    print "Writing to ", f
    f = open("results/" + f, 'w')
    time.sleep(.1)
    if p.poll() is None:
        #process is either hanging or being slow
        time.sleep(5)
        if p.poll() is None:
            p.kill()
            f.write("Process hung; no results to report\n")
            f.close()
            return
    output = p.stdout.read()
    #remove output header
    hdrs = []
    hdrs.append(re.compile("SPIM Version .* of .*\n"))
    hdrs.append(re.compile("Copyright .*, James R. Larus.\n"))
    hdrs.append(re.compile("All Rights Reserved.\n"))
    hdrs.append(re.compile("See the file README for a full copyright notice.\n"))
    hdrs.append(re.compile("Loaded: .*/spim/.*\n"))
    for hdr in hdrs:
        output = re.sub(hdr, "", output)
    errors = p.stderr.read()
    if errors == "":
        f.write("\t**PROCESS COMPLETED**\n")
        f.write(output + '\n'*2)
    else:
        f.write("\t**PROCESS FAILED TO COMPILE**\n")
        f.write(output + '\n' + errors + '\n'*2)
    f.close() 

def generate_filename(submission, sample):
    #extract RCS id from submission title
    try:
        rcs_start = submission.index('_') + 1
        rcs_end = min(submission.index('attempt'), submission.index('.')) - 1
        rcs = submission[rcs_start:rcs_end]
    except:
        rcs = submission
    return rcs + '__' + sample

def main():
    print "HERE!"
    #no use in running if content directories aren't present
    assert os.path.isdir("samples")
    assert os.path.isdir("submissions")
    if os.path.isdir("results") is False:
        assert os.path.isfile("results") == False
        os.makedirs("results")
    #cycle through files to grade:
    for submission in os.listdir('submissions'):
        #cycle through samples to test (ignore .example):
        for sample in os.listdir('samples'):
            #ignore example files
            if submission == ".example" or sample == ".example":
                continue
            sample_file = open('samples/'+sample, 'r')
            #read sample input; fix windows EOL char
            sample_input = sample_file.read()
            sample_input = sample_input.replace('\r', '')
            #create process
            p = run(submission, sample_input)
            output_file = generate_filename(submission, sample)
            grade(p, output_file)
    print("SUCCESS!")

if __name__ == "__main__":
    main()

