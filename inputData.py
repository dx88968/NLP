#!/usr/bin/python

### Use InputData(directory_path(defalut: ''), dataset(defalut: 'beetle')) to make an instance,
##  Then call InputData.readFile(file_name, dataset(defalut is 'beetle')) to read file.
##  file_name should not include path if directory_path is already set.
##
##  The output is a dictionary, according to dataset
##  For 'beetle':
##      the dictionary is
##          { 'id' -> question id,
##            'text' -> question text,
##            'referenceAnswers' -> [ 0 : { 'id' -> reference answer id
##                                          'category' -> reference answer category(Best/Minimal)
##                                          'text' -> reference answer text
##                                          'studentAnswers' -> [ 0 : { 'id' -> student answer id
##                                                                      'accuracy' -> the accuracy for this reference answer
##                                                                      'text' -> student answer text
##                                                                    }
##                                                                1 : ...
##                                                              ]
##                                        }
##                                    1 : ...
##                                  ]
##            'otherStudentAnswers' -> [ 0 : { 'id' -> student answer id
##                                             'accuracy' -> the accuracy for this reference answer
##                                             'text' -> student answer text
##                                           }
##                                       1 : ...
##                                     ]
##          }
##
##  For 'seb'
##      the dictionary is
##          { 'id' -> question id,
##            'text' -> question text,
##            'referenceAnswer' -> { 'id' -> reference answer id
##                                   'text' -> reference answer text
##                                 }
##            'studentAnswers' -> [ 0 : { 'id' -> student answer id
##                                        'accuracy' -> the accuracy for this reference answer
##                                        'text' -> student answer text
##                                      }
##                                  1 : ...
##                                ]
##          }



import os
from xml.etree import ElementTree

class InputData(object):

    def __init__(self, dataset, path = ''):
        self.path = path
        self.question = {}
        self.dataset = dataset.lower()

    def readDict(self, dict_path):
        pass

    def readFile(self, file_name):
        # self.dataset = dataset.lower()
        # I think one instance only for one kind dataset may be better
        # or it will be a little confusing.
        self.file = file_name
        
        # reset question, let the instance resueable.
        self.question = {}

        if not os.path.isfile(self.path + self.file):
            print 'File not exist!'
        else:
            self.document = ElementTree.parse(self.path + self.file)
            self.root = self.document.getroot()
            self.question['id'] = self.root.attrib['id']
            self.question['text'] = self.root[0].text
            
            if self.dataset == 'beetle':
                return self._readBeetle()
            elif self.dataset == "seb":
                return self._readSeb()
            else:
                raise Exception("Wrong dataset")
    def read(self, file_name):
        """
            return general data structure for all data set
        """
        self.readFile(file_name)
        rsl = {}
        if self.dataset == "beetle":
            rsl["text"] = self.question["text"]
            rsl["id"] = self.question["id"]
            rsl["references"] = [ 
                    {   "text":r["text"], 
                        'category':r['category'], 
                        "id":r["id"]} 
                    for r in self.question["referenceAnswers"] ]
            rsl["student_answers"] = []
            for r in self.question["referenceAnswers"]:
                for a in r["studentAnswers"]:
                    rsl["student_answers"].append({
                        "text":a["text"],
                        "id":a["id"],
                        "accuracy":a["accuracy"]})
            for a in self.question["otherStudentAnswers"]:
                rsl["student_answers"].append({
                    "text":a["text"],
                    "id":a["id"],
                    "accuracy":a["accuracy"]})
            return rsl
        elif self.dataset == "seb":
            pass
        else:
            raise Exception("Wrong dataset")
            
    def _readBeetle(self):
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

    def _readSeb(self):
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
    model = InputData("seb",'SemEval/train/seb/Core/')
    model.readFile('EM-inv1-45b.xml')
