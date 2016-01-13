from mrjob.job import MRJob
from mrjob.step import MRStep

class MostPopularSuperHero(MRJob):
    
    def configure_options(self):
        super(MostPopularSuperHero, self).configure_options()
        self.add_file_option('--names', help='Path to Marvel-Names.txt')
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper_count_friends_per_line,
                   reducer=self.reducer_combine_friends),
            MRStep(mapper=self.mapper_prep_for_sort,
                   mapper_init=self.load_name_dictionary,
                   reducer=self.reducer_find_max_friends)
        ]
            
    def mapper_count_friends_per_line(self, _, line):
        fields = line.split()
        heroID = fields[0]
        numFriends = len(fields) - 1
        yield int(heroID), int(numFriends)
        
    def reducer_combine_friends(self, heroID, friendsCount):
        yield heroID, sum(friendsCount)
        
    def mapper_prep_for_sort(self, heroID, friendsCount):
        heroName = self.heroName[heroID]
        yield None, (friendsCount, heroName)
    
    def reducer_find_max_friends(self, key, value):
        yield max(value)
        
    def load_name_dictionary(self):
        self.heroName = {}
        
        with open("Marvel-Names.txt") as f:
            for line in f:
                fields = line.split()
                heroID = int(fields[0])
                self.heroName[heroID] = fields[1]

if __name__ == '__main__':
    MostPopularSuperHero.run()