import lsa2
import numpy
from numpy import zeros
from numpy import mat
from numpy import dot
import numpy.linalg as linalg
import inputData

class grading(object):
    """
        Create an model for one question.
        and return grade for answer.
    """
    def __init__(self, references):
        """
            references: ["ref1 string", "", ...]
        """
        stopwords = ['and','for','in','little','of','the','to']
        ignorechars = ''',.?:'!'''
        self._lsa = lsa2.LSA(stopwords, ignorechars)
        for d in references:
            self._lsa.parse(d)
        self._lsa.build()
        self._lsa.calc()

        self.U, self.S, self.V = self._lsa.get_usv(5)
        self.Si = (self.S+0.001).I

    def grade(self, answer):
        """
            answer: a string
            return grade for one answer, 
        """

        # construct a sudo-document for student answer
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
        qd = dot(dot(q.T, self.U), self.Si)
        #
        grade = []
        # dimension reduction of A
        d = dot(dot(self.U, self.S), self.V)

        # compare the student answet to each reference answer in A
        for i in range(d.shape[1]):
            dd = d[:,i].T * self.U * self.Si
            grade.append(self.sim(qd, dd))
        return grade

    def sim(self, a, b):
        """
            Cosine similarity
            a,b : numpy.array
        """
        if isinstance(a, numpy.matrix):
            a = numpy.array(a)[0]
        if isinstance(b, numpy.matrix):
            b = numpy.array(b)[0]
        num = sum(a *b)
        deno = linalg.norm(a) * linalg.norm(b)
        
        return num/deno

def test():
    p = inputData.InputData("beetle", '../SemEval/train/beetle/Core/' )
    problem = p.readFile('FaultFinding-BULB_C_VOLTAGE_EXPLAIN_WHY1.xml')

    references = [r["text"] for r in problem["referenceAnswers"]]
    student = problem["otherStudentAnswers"][0]["text"]

    print "references"
    for r in references:
        print r
    print "\n"
    print "Student answer"
    print student
    g = grading(references)
    print g.grade(student)

if __name__ == "__main__":
    test()
