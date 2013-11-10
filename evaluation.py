#!/usr/bin/env python2.7
import basic_lsa
import sys

def main():
    argv = sys.argv
    if len(argv) != 5:
        print "wrong parameters!"
        print "evaluation.py dataset_type data_path model output"
        return
    basic = basic_lsa.basic_lsa(argv[1], argv[2], int(argv[3]), argv[4])
    basic.run()

if __name__ == "__main__":
    main()

