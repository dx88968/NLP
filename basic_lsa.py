#!/usr/bin/env python2.7

from os import listdir
from inputData import InputData
from grading import grading
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
                3: [0.35, 0.75],
                5: [0, 0.25, 0.5, 0.75]
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
        for filename in files:
            question = reader.read(filename)
            references = [ parsers.stem(r["text"]) for r in question["references"]]
            # create the grading model
            g = grading(references)
            for answer in question["student_answers"]:
                # get points for an anser
                points = g.grade(answer["text"])
                # convert point based result to test based grade
                predicted = self.predict(points)
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
    basci = basic_lsa("beetle", "../SemEval/train/beetle/Core/", 3, "out.lsa.txt")
    basci.run()
