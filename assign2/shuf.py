#!/usr/bin/python
"""
Author: Yili Liu 20537049
"""

import random, sys, argparse

class shuf:
    def __init__(self, echo, inputRange, headCount, repeat, File):
        self.File = File
        self.echo = echo
        self.inputRange = inputRange
        self.headCount = int(headCount)
        self.repeat = repeat

    #shuffles the lines of the file
    def shuffle(self):
        random.shuffle(self.File)

    #puts echo array in file and shuffles
    def set_echo(self):
        self.File.extend(self.echo)
        random.shuffle(self.File)

    #sets range, makes an array of the range, and shuffles
    def set_range(self):
        start = int(self.inputRange[0])
        end = int(self.inputRange[1]) + 1
        for i in range(start, end):
            self.File.append(i)
        random.shuffle(self.File)

    #prints out the ahuffles file (make sure headcount is counted if needed)
    def print_count(self):
        if self.headCount > len(self.File):
            self.headCount = len(self.File)
        for i in range(0, self.headCount):
            print(self.File[i])

    #creates a continuous loop, repeatedly printing out file in random order
    def print_repeat(self):
        rng = self.headCount
        for i in range(0, rng):
            print(random.choice(self.File))
    
def main():
    version_msg = "%prog 1.0"
    usage_msg = """%prog [OPTION] [-e] [-i] [-n] [-r] FILE"""

parser = argparse.ArgumentParser()

#add all of the arguments 
parser.add_argument("filename", action="store", nargs="?")
parser.add_argument("-e", "--echo",
                    action="store", nargs="+", dest="echo", default="",
                    help="treat each argument as an input line")
parser.add_argument("-i", "--input-range",
                    action="store", dest="inputRange", default="",
                    help="treat each number LO through HI as an input line")
parser.add_argument("-n", "--head-count",
                    action="store", dest="headCount", default=sys.maxsize,
                    type=int,
                    help="output at most COUNT lines")
parser.add_argument("-r", "--repeat",
                    action="store_true", dest="repeat", default=False,
                    help="output lines are repeated forever")
    
args = parser.parse_args()
m_file = []

#check that input range and file were not both given
if args.filename != None and args.inputRange != "":
    sys.exit("Error: both file and input range were given")
    
if args.filename is None or args.filename == "-":
    if args.inputRange == "" and args.echo == "":
        m_file = sys.stdin.read().splitlines()

#checks and reads in the text file given echo is not called
if args.filename is not None and args.echo == "" and args.filename != "-":
    f = open(args.filename, 'r')
    m_file = f.read().splitlines()
    f.close()

#Checking Validity of Headcount
if args.headCount is not None:
    #make sure the headcount given is a number
    try:
        headCount = int(args.headCount)
    except:
        parser.error("Error: Headcount is Invalid: {0}".format(args.headCount))
    #make sure headcount is a positive integer
    if args.headCount < 0:
        sys.exit("Error: Headcount cannot be negative")
elif args.headCount is None:
    headCount = sys.maxsize #head count was not called

#Checking Validity of Input Range
if args.inputRange == "":
    m_inputRange = ""
elif args.inputRange != "":
    #splits range into an array of two
    m_inputRange = args.inputRange.split("-", 1)
    #make sure two arguments are given
    try:
        int(m_inputRange[0])
        int(m_inputRange[1])
    except:
        parser.error("Error: Invalid input range".format(args.inputRange))
    #make sure the first number is smaller than the second
    if int(m_inputRange[0]) > int(m_inputRange[1]):
        sys.exit("Error: Invalid input range")

#executes all commands
execute = shuf(args.echo, m_inputRange, args.headCount, args.repeat, m_file)

#if -i is called, execute input range 
if execute.inputRange != "":
    execute.set_range()
#if -e is called, execute echo
if execute.echo != "":
    execute.set_echo()

#print out the results
execute.shuffle()
if args.repeat is False:
    execute.print_count()
else:
    execute.print_repeat() #if needed, print repeat
