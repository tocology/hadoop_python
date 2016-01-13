from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

class Node:
    def __init__(self):
        self.characterID = ''
        self.connections = []
        self.distance = 9999
        self.color = 'WHITE'

    #Format is ID|EDGES|DISTANCE|COLOR
    def fromLine(self, line):
        fields = line.split('|')
        if (len(fields) == 4):
            self.characterID = fields[0]
            self.connections = fields[1].split(',')
            self.distance = int(fields[2])
            self.color = fields[3]

    def getLine(self):
        connections = ','.join(self.connections)
        return '|'.join( (self.characterID, connections, str(self.distance), self.color) )

class MRBFSIteration(MRJob):

    INPUT_PROTOCOL = RawValueProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    def configure_options(self):
        super(MRBFSIteration, self).configure_options()
        self.add_passthrough_option(
            '--target', help="ID of character we are searching for")

    def mapper(self, _, line):
        node = Node()
        node.fromLine(line)
        #If this node needs to be expanded...
        if (node.color == 'GRAY'):
            for connection in node.connections:
                vnode = Node()
                vnode.characterID = connection
                vnode.distance = int(node.distance) + 1
                vnode.color = 'GRAY'
                if (self.options.target == connection):
                    counterName = ("Target ID " + connection +
                        " was hit with distance " + str(vnode.distance))
                    self.increment_counter('Degrees of Separation',
                        counterName, 1)
                yield connection, vnode.getLine()

            #We've processed this node, so color it black
            node.color = 'BLACK'

        #Emit the input node so we don't lose it.
        yield node.characterID, node.getLine()

    def reducer(self, key, values):
        edges = []
        distance = 9999
        color = 'WHITE'

        for value in values:
            node = Node()
            node.fromLine(value)

            if (len(node.connections) > 0):
                #edges = node.connections
                edges.extend(node.connections)

            if (node.distance < distance):
                distance = node.distance

            if ( node.color == 'BLACK' ):
                color = 'BLACK'

            if ( node.color == 'GRAY' and color == 'WHITE' ):
                color = 'GRAY'

        node = Node()
        node.characterID = key
        node.distance = distance
        node.color = color
        #There's a bug in mrjob for Windows where sorting fails
        #with too much data. As a workaround, we're limiting the
        #number of edges to 500 here. You'd remove the [:500] if you
        #were running this for real on a Linux cluster.
        node.connections = edges[:500]

        yield key, node.getLine()

if __name__ == '__main__':
    MRBFSIteration.run()
