import re
import numpy as np
import numpy.linalg as linalg
from utils import normalize

np.set_printoptions(threshold='nan')

class Reference(object):

    '''
    Splits a text file into an ordered list of words.
    '''

    # List of punctuation characters to scrub. Omits, the single apostrophe,
    # which is handled separately so as to retain contractions.
    PUNCTUATION = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*']

    # Carriage return strings, on *nix and windows.
    CARRIAGE_RETURNS = ['\n', '\r\n']

    # Final sanity-check regex to run on words before they get
    # pushed onto the core words list.
    WORD_REGEX = "^[a-z']+$"


    def __init__(self, ref):
        '''
        Set source file location, build contractions list, and initialize empty
        lists for lines and words.
        '''
        self.content=ref
        self.words=[]
        STOP_WORDS_SET=set()
        stopwordsfile = open("stopwords_shortlist.txt", "r")
        for word in stopwordsfile: # a stop word in each line
            word = word.replace("\n", '')
            word = word.replace("\r\n", '')
            STOP_WORDS_SET.add(word)
        self.split(STOP_WORDS_SET)


    def split(self, STOP_WORDS_SET):
        '''
        Split file into an ordered list of words. Scrub out punctuation;
        lowercase everything; preserve contractions; disallow strings that
        include non-letters.
        '''
        words = self.content.split(' ')
        for word in words:
                clean_word = self._clean_word(word)
                if clean_word and (clean_word not in STOP_WORDS_SET) and (len(clean_word) > 1): # omit stop words
                    self.words.append(clean_word)



    def _clean_word(self, word):
        '''
        Parses a space-delimited string from the text and determines whether or
        not it is a valid word. Scrubs punctuation, retains contraction
        apostrophes. If cleaned word passes final regex, returns the word;
        otherwise, returns None.
        '''
        word = word.lower()
        for punc in Reference.PUNCTUATION + Reference.CARRIAGE_RETURNS:
            word = word.replace(punc, '').strip("'")
        return word if re.match(Reference.WORD_REGEX, word) else None


class Corpus(object):

    '''
    A collection of references.
    '''

    def __init__(self):
        '''
        Initialize empty document list.
        '''
        self.references = []
        self.ready=False

    def addBaseline(self,refs):
        self.references = []
        for ref in refs:
            r=Reference(ref)
            self.add_reference(r)

        self.build_vocabulary()
        try:
            self.plsa(3,50)
            self.ready=True
        except:
            self.ready=False




    def add_reference(self, reference):
        '''
        Add a document to the corpus.
        '''
        self.references.append(reference)


    def build_vocabulary(self):
        '''
        Construct a list of unique words in the corpus.
        '''
        # ** ADD ** #
        # exclude words that appear in 90%+ of the documents
        # exclude words that are too (in)frequent
        discrete_set = set()
        for reference in self.references:
            for word in reference.words:
                discrete_set.add(word)
        self.vocabulary = list(discrete_set)
        


    def plsa(self, number_of_topics, max_iter):

        '''
        Model topics.
        '''
        #print "EM iteration begins..."
        # Get vocabulary and number of documents.
        self.build_vocabulary()
        number_of_references = len(self.references)
        vocabulary_size = len(self.vocabulary)
        
        # build term-ref matrix
        term_ref_matrix = np.zeros([number_of_references, vocabulary_size], dtype = np.int)
        for d_index, ref in enumerate(self.references):
            term_count = np.zeros(vocabulary_size, dtype = np.int)
            for word in ref.words:
                if word in self.vocabulary:
                    w_index = self.vocabulary.index(word)
                    term_count[w_index] = term_count[w_index] + 1
            term_ref_matrix[d_index] = term_count

        # Create the counter arrays.
        self.ref_topic_prob = np.zeros([number_of_references, number_of_topics], dtype=np.float) # P(z | d)
        self.topic_word_prob = np.zeros([number_of_topics, len(self.vocabulary)], dtype=np.float) # P(w | z)
        self.topic_prob = np.zeros([number_of_references, len(self.vocabulary), number_of_topics], dtype=np.float) # P(z | d, w)

        # Initialize
        #print "Initializing..."
        # randomly assign values
        self.ref_topic_prob = np.random.random(size = (number_of_references, number_of_topics))
        for d_index in range(len(self.references)):
            normalize(self.ref_topic_prob[d_index]) # normalize for each refer
        self.topic_word_prob = np.random.random(size = (number_of_topics, len(self.vocabulary)))
        for z in range(number_of_topics):
            normalize(self.topic_word_prob[z]) # normalize for each topic
        """  
        # for test, fixed values are assigned, where number_of_references = 3, vocabulary_size = 15
        self.document_topic_prob = np.array(
        [[ 0.19893833,  0.09744287,  0.12717068,  0.23964181,  0.33680632],
         [ 0.27681925,  0.22971358,  0.1704416,   0.18248461,  0.14054095],
         [ 0.24768207,  0.25136754,  0.14392363,  0.14573845,  0.21128831]])

        self.topic_word_prob = np.array(
      [[ 0.02963563,  0.11659963,  0.06415405,  0.1291839 ,  0.09377842,
         0.09317023,  0.06140873,  0.023314  ,  0.09486251,  0.01538988,
         0.09189075,  0.06957687,  0.05015957,  0.05281074,  0.0140651 ],
       [ 0.09746902,  0.12212085,  0.07635703,  0.02799546,  0.0282282 ,
         0.03685356,  0.01256655,  0.03931912,  0.09545668,  0.00928434,
         0.11392475,  0.12089124,  0.02674909,  0.07219077,  0.12059333],
       [ 0.02209806,  0.05870101,  0.12101806,  0.03733935,  0.02550749,
         0.09906735,  0.0706651 ,  0.05619682,  0.10672434,  0.12259672,
         0.04218994,  0.10505831,  0.00315489,  0.03286002,  0.09682255],
       [ 0.0428768 ,  0.11598272,  0.08636138,  0.10917224,  0.05061344,
         0.09974595,  0.01647265,  0.06376147,  0.04468468,  0.01986342,
         0.10286377,  0.0117712 ,  0.08350884,  0.049046  ,  0.10327543],
       [ 0.02555784,  0.03718368,  0.10109439,  0.02481489,  0.0208068 ,
         0.03544246,  0.11515259,  0.06506528,  0.12720479,  0.07616499,
         0.11286584,  0.06550869,  0.0653802 ,  0.0157582 ,  0.11199935]])
        """
        # Run the EM algorithm
        for iteration in range(max_iter):
            #print "Iteration #" + str(iteration + 1) + "..."
            #print "E step:"
            for d_index, refer in enumerate(self.references):
                for w_index in range(vocabulary_size):
                    prob = self.ref_topic_prob[d_index, :] * self.topic_word_prob[:, w_index]
                    if sum(prob) == 0.0:
                        print "Error in process %s"%refer.content
                        print "d_index = " + str(d_index) + ",  w_index = " + str(w_index)
                        print "self.document_topic_prob[d_index, :] = " + str(self.ref_topic_prob[d_index, :])
                        print "self.topic_word_prob[:, w_index] = " + str(self.topic_word_prob[:, w_index])
                        print "topic_prob[d_index][w_index] = " + str(prob)
                        raise RuntimeError()
                    else:
                        normalize(prob)
                    self.topic_prob[d_index][w_index] = prob
            #print "M step:"
            # update P(w | z)
            for z in range(number_of_topics):
                for w_index in range(vocabulary_size):
                    s = 0
                    for d_index in range(len(self.references)):
                        count = term_ref_matrix[d_index][w_index]
                        s = s + count * self.topic_prob[d_index, w_index, z]
                    self.topic_word_prob[z][w_index] = s
                normalize(self.topic_word_prob[z])
            
            # update P(z | d)
            for d_index in range(len(self.references)):
                for z in range(number_of_topics):
                    s = 0
                    for w_index in range(vocabulary_size):
                        count = term_ref_matrix[d_index][w_index]
                        s = s + count * self.topic_prob[d_index, w_index, z]
                    self.ref_topic_prob[d_index][z] = s
#                print self.document_topic_prob[d_index]
#                assert(sum(self.document_topic_prob[d_index]) != 0)
                normalize(self.ref_topic_prob[d_index])

    def sim(self, a, b):
        """
            Cosine similarity
            a,b : numpy.array
        """
        if isinstance(a, np.matrix):
            a = np.array(a)[0]
        if isinstance(b, np.matrix):
            b = np.array(b)[0]
        num = sum(a *b)
        deno = linalg.norm(a) * linalg.norm(b)

        return num/deno

    def grading(self,target):
        if not self.ready:
            return np.zeros(len(self.ref_topic_prob), dtype = np.float)
        #print self.topic_prob
        t=Reference(target)
        term_count = np.zeros(len(self.vocabulary), dtype = np.int)
        ecount=0
        for word in t.words:
            if word in self.vocabulary:
                try:
                    w_index = self.vocabulary.index(word)
                    term_count[w_index] = term_count[w_index] + 1
                    ecount=ecount+1
                except:
                    continue

        if ecount==0:
            return np.zeros(len(self.ref_topic_prob), dtype = np.float)

        scores=[]

        for i in range(0,len(self.ref_topic_prob)):
            score=0.0
            for j in range(0,len(self.ref_topic_prob[0])):
                weight=self.ref_topic_prob[i,j]
                score=score+weight*self.sim(self.topic_word_prob[j],term_count)

            scores.append(score)

        return scores

