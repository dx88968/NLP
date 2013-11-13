#!/usr/bin/env python2.7

from os import listdir
from inputData import InputData
import plsa
from output import output
import parsers



class basic_lsa(object):
    """
        an work SRA system
    """
    def __init__(self, dataset_type, path, mode, output_filename):
        """
            dataset_type: "beetle" or "seb"
            path: the path of test data
            mode: 2, 3 or 5
            output_filename: "filename"
        """
        self.modes={
                2: [0.75],
                3: [0.40, 0.75],
                5: [0.1, 0.15, 0.20, 0.30]
                }
        self.dataset_type = dataset_type
        self.path = path
        self.mode = mode
        self.output_filename = output_filename

    def run(self):
        head = ["id","Accuracy", "Predicted"]
        rsl = []
        files = listdir(self.path)
        reader = InputData(self.dataset_type, self.path)
        corpus = plsa.Corpus()
        for filename in files:
            question = reader.read(filename)
            references = [ parsers.stem(r["text"]) for r in question["references"]]
            # create the grading model
            corpus.addBaseline(references)
            for answer in question["student_answers"]:
                # get points for an anser
                points = corpus.grading(answer["text"])
                # convert point based result to test based grade
                predicted = self.predict(points)
                print predicted
                rsl.append({"id": answer["id"], 
                    "Accuracy":answer["accuracy"],
                    "Predicted":predicted})
        output(self.output_filename, head, rsl)
        return
    
    def predict(self, points):
        """
            convert points to an text grade based on mode
            points = []
        """
        way2 = ["incorrect", "correct"]
        way3 = ["incorrect", "contradictory", "correct"]
        way5 = ["non_domain", "irrelevant", "contradictory", 
                "partially_correct_incomplete", "correct"]
        point = max(points)
        print point
        if self.mode == 2:
            if point < self.modes[2][0]:
                return way2[0]
            else:
                return way2[1]
        elif self.mode == 3:
            for i in range(2):
                if point < self.modes[3][i]:
                    return way3[i]
            return way3[2]
        elif self.mode == 5:
            for i in range(4):
                if point < self.modes[5][i]:
                    return way5[i]
            return way5[4]
        else:
            raise Exception("Wrong mode")


if __name__ == "__main__":
    basci = basic_lsa("beetle", "../SemEval/train/beetle/Core/", 5, "out.plsa.txt")
    basci.run()
