#!/usr/bin/env python2.7
from basic_lsa import basic_lsa as lsa
from basic_plsa import basic_lsa as plsa

methods = {"lsa":lsa, "plsa":plsa }
ways = [2,3,5]
data_sets = {"beetle":r"../SemEval/train/beetle/Core/", "seb":r"../SemEval/train/seb/Core/"}

for method in methods:
    for way in ways:
        for data in data_sets:
            print method, way, data, data_sets[data]
            b = methods[method](data, data_sets[data], way, "%s_%d_%s.txt" % (method, way, data))
            b.run()

    
