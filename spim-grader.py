#!/usr/bin/python
'''
This program is modified from:
SPIM Auto-grader
Owen Stenson
Grades every file in the 'submissions' folder using every test in the 'samples' folder.
Writes to 'results' folder.

Source: https://github.com/stensonowen/spim-grader
Licence: GPL 2.0
'''
import os, time, re
from subprocess import Popen, PIPE, STDOUT

def run(fn, sample_input='\n'):
    #start process and write input
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
    for proc in p:
        time.sleep(.1)
        if proc.poll() is None:
            #process is either hanging or being slow
            time.sleep(5)
            if proc.poll() is None:
                proc.kill()
                f.write("Process hung; no results to report\n")
                f.close()
                return
        output = proc.stdout.read()
        #remove output header
        hdrs = []
        hdrs.append(re.compile("SPIM Version .* of .*\n"))
        hdrs.append(re.compile("Copyright .*, James R. Larus.\n"))
        hdrs.append(re.compile("All Rights Reserved.\n"))
        hdrs.append(re.compile("See the file README for a full copyright notice.\n"))
        hdrs.append(re.compile("Loaded: .*/spim/.*\n"))
        for hdr in hdrs:
            output = re.sub(hdr, "", output)
        errors = proc.stderr.read()
        if errors == "":
            f.write("\t**PROCESS COMPLETED**\t")
            f.write(output + '\n'*2)
        else:
            f.write("\t**PROCESS FAILED TO COMPILE**\t")
            f.write(output + '\n' + errors + '\n'*2)
    f.close() 

def compare(results, expectations):
    diag = open("./diagnostics/{}".format(results), "w")
    results = open("./results/{}".format(results), "r")
    expectations = open("./expectations/{}".format(expectations), "r")

    r = results.readlines()
    e = expectations.readlines()    
    for i in range(len(e)):
        if r[i] == e[i]:
            diag.write("Test Case {}: PASSED\n".format(i+1))
        else:
            diag.write("Test Case {}: FAILED\n".format(i+1))
            diag.write("\tExpected: {}\n".format(e[i]))
            diag.write("\tReceived: {}\n".format(r[i]))

    results.close()
    expectations.close()
    diag.close()

def generate_filename(submission, sample):
    # TODO: ID should be the students' team_name
    try:
        ID = ""
        f = open("./submissions/{}".format(submission), "r")
        lines = f.readlines()
        line = lines[4]
        ID = line[10:].strip()
        f.close()
    except:
        ID = submission
    return ID + '__' + sample

def main():
    #no use in running if content directories aren't present
    assert os.path.isdir("samples")
    assert os.path.isdir("submissions")
    if os.path.isdir("results") is False:
        assert os.path.isfile("results") == False
        os.makedirs("results")
    #cycle through files to grade:
    for submission in os.listdir('submissions'):
        #cycle through samples to test (ignore .example):
        output_file = ""
        for sample in os.listdir('samples'):
            #ignore example files
            if submission == ".example" or sample == ".example":
                continue
            sample_file = open('samples/'+sample, 'r')
            #read sample input; fix windows EOL char
            results = []
            for line in sample_file.readlines():
                sample_input = line
                sample_input = sample_input.replace('\r', '')
                #create process
                p = run(submission, sample_input)
                results.append(p)
            output_file = generate_filename(submission, sample)
            grade(results, output_file)
            compare(output_file, sample)

if __name__ == "__main__":
    main()

