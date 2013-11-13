#!/usr/bin/env python2.7
from basic_lsa import basic_lsa
from basic_plsa import basic_lsa as plsa
import sys

def main():
    argv = sys.argv
    if len(argv) != 6:
        print "wrong parameters!"
        print "run.py method dataset_type data_path model output"
        return
    if argv[1] == "lsa":
        basic = basic_lsa
    elif argv[1] == "plsa":
        basic = plsa
    basic = basic(argv[2], argv[3], int(argv[4]), argv[5])
    basic.run()

if __name__ == "__main__":
    main()

