import lsa2
import numpy
from numpy import zeros
from numpy import mat
import numpy.linalg as linalg
import inputData

class grading(object):
    """
        Create an model for one question.
        and return grade for answer.
    """
    def __init__(self, references):
        stopwords = ['and','for','in','little','of','the','to']
        ignorechars = ''',.?:'!'''
        self._lsa = lsa2.LSA(stopwords, ignorechars)
        for d in references:
            self._lsa.parse(d)
        self._lsa.build()
        self._lsa.calc()

        self.U = self._lsa.U
        self.Si = mat(self._lsa.S).I

    def grade(self, answer):
        """
            return grade for one answer, 
            answer should be a stirng.
        """
        count = {}
        for w in answer.split():
            if w in count:
                count[w]+=1
            else:
                count[w] = 1
        q = zeros( [len(self._lsa.keys), 1] )
        for i,k in enumerate(self._lsa.keys):
            if k in count:
                q[i] = count[k]
        dq = q * self.U * self.Si
        print q

        grade = []
        for idoc in range(len(self._lsa.A[0])):
            d = self._lsa.A[:,idoc]
            d = numpy.mat(d)
            dd = d * self.U * self.Si
            grade.append(self.sim(dq, dd))
        return grade

    def sim(self, a, b):
        """
            Cosine similarity
            a,b : numpy.array
        """
        num = sum(a *b)
        deno = linalg.norm(a) * linalg.norm(b)
        
        return num/deno
p = inputData.InputData('../SemEval/train/beetle/Core/', "beetle")
problem = p.readFile('FaultFinding-BULB_C_VOLTAGE_EXPLAIN_WHY1.xml')

references = [r["text"] for r in problem["referenceAnswers"]]
student = problem["otherStudentAnswers"][0]["text"]
for r in references:
    print r
print "\n"
print student
g = grading(references)
print g.grade(student)
