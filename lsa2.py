from numpy import zeros
from scipy.linalg import svd
from scipy import dot
from scipy import transpose
#following needed for TFIDF
from math import log
from numpy import asarray, sum

titles = ["Terminal 1 and the positive terminal are separated by the gap",
          "positive battery terminal is separated by a gap from terminal 1",
          "Because terminal 1 is connected to the positive battery terminal",
          "i do not understand",
          "Terminal 1 is seperated from the positive terminal",
          "because terminal one and the positive terminal are connected",
          "becaquse there was a gap in the connection",
          "Terminal 1 is not connected to the positive terminal",
          "because it was connected to the positive terminal"
          ]
stopwords = ['and','edition','for','in','little','of','the','to']
ignorechars = ''',:'!'''

class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0        
    def parse(self, doc):
        words = doc.split();
        for w in words:
            w = w.lower().translate(None, self.ignorechars)
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]
        self.dcount += 1      
    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
        self.A = zeros([len(self.keys), self.dcount])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i,d] += 1
    def calc(self):
        self.U, self.S, self.Vt = svd(self.A,full_matrices=False)
        self.formatS()

    def formatS(self):
        self.temp=zeros([len(self.S),len(self.S)])
        for i in range(0,len(self.S)):
            self.temp[i,i]=self.S[i]


    def TFIDF(self):
        WordsPerDoc = sum(self.A, axis=0)        
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])
    def printA(self):
        print 'Here is the count matrix'
        print self.A
    def printSVD(self):
        print 'Here are the singular values'
        print self.S
        print 'Here are the first 3 columns of the U matrix'
        print -1*self.U[:, 0:3]
        print 'Here are the first 3 rows of the Vt matrix'
        print -1*self.Vt[0:3, :]

mylsa = LSA(stopwords, ignorechars)
for t in titles:
    mylsa.parse(t)
mylsa.build()
mylsa.printA()
mylsa.calc()
#mylsa.printSVD()
he=dot(dot(mylsa.U,mylsa.temp),mylsa.Vt)
print he[:,0:1]
print transpose(he)[3:4,:]
print dot(transpose(he)[3:4,:],he[:,0:1])
#print dot(he[:,0:1],transpose(he)[1:2,:])


