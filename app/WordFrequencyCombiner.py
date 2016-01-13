from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_REGEXP = re.compile(r"[\w']+")

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, lin):
        words = lint.split()
        for word in words:
            yield word.lower(), 1
    
    def combiner(self, key, values):
        yield key, sum(values)
    
    def reducer(self, key, values):
        yield key, sum(values)
        

if __name__ == '__main__':
    MRWordFrequencyCount.run()