#!/usr/bin/python

import os
from xml.etree import ElementTree

class InputData(object):

    def __init__(self, path = '', dataset = 'beetle'):
        self.path = path
        self.question = {}
        self.dataset = dataset.lower()

    def readDict(self, dict_path):
        pass

    def readFile(self, file_path, dataset = 'beetle'):
        self.dataset = dataset.lower()
        self.file = file_path
        if not os.path.isfile(self.path + self.file):
            print 'File not exist!'
        else:
            self.document = ElementTree.parse(self.path + self.file)
            self.root = self.document.getroot()
            self.question['id'] = self.root.attrib['id']
            self.question['text'] = self.root[0].text
            
            if self.dataset == 'beetle':
                self.readBeetle()
            else:
                self.readSeb()
            
    def readBeetle(self):
        self.question['referenceAnswers'] = []
        for ans in self.root[1]:
            each_ref_ans = {}
            for key, value in ans.attrib.items():
                if key != 'fileID':
                    each_ref_ans[key] = value
            each_ref_ans['text'] = ans.text
            each_ref_ans['studentAnswers'] = []
            self.question['referenceAnswers'].append(each_ref_ans)
        self.question['otherStudentAnswers'] = []

        for ans in self.root[2]:
            each_stu_ans = {}
            ans_id = None
            for key, value in ans.attrib.items():
                if key == 'answerMatch':
                    ans_id = value
                elif key != 'count':
                    each_stu_ans[key] = value
            each_stu_ans['text'] = ans.text
            if ans_id == None:                        
                self.question['otherStudentAnswers'].append(each_stu_ans)
            else:
                for index in range(len(self.question['referenceAnswers'])):
                    if self.question['referenceAnswers'][index]['id'] == ans_id:
                        self.question['referenceAnswers'][index]['studentAnswers'].append(each_stu_ans)
                        break;
        
            
        #print len(self.question['referenceAnswers'])
        return self.question

    def readSeb(self):
        self.question['referenceAnswer'] = {}
        self.question['referenceAnswer']['id'] = self.root[1][0].attrib['id']
        self.question['referenceAnswer']['text'] = self.root[1][0].text
        self.question['studentAnswers'] = []
        for ans in self.root[2]:
            each_stu_ans = {}
            for key, value in ans.attrib.items():
                each_stu_ans[key] = value
            each_stu_ans['text'] = ans.text
            self.question['studentAnswers'].append(each_stu_ans)

        #print len(self.question['studentAnswers'])
        return self.question
        
# Testing code
if __name__ == '__main__':
    #model = InputData('SemEval/train/beetle/Core/')
    #model.readFile('FaultFinding-BULB_C_VOLTAGE_EXPLAIN_WHY1.xml')
    #model.readFile('FaultFinding-BULB_C_VOLTAGE_EXPLAIN_WHY2.xml')
    model = InputData('SemEval/train/seb/Core/')
    model.readFile('EM-inv1-45b.xml', 'seb')
