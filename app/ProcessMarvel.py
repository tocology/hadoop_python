import sys

print 'Creating BFS starting input for character ' + sys.argv[1]

with open("data/BFS-iteration-0.txt", 'w') as out:

    with open("data/Marvel-Graph.txt") as f:

        for line in f:
            fields = line.split()
            heroID = fields[0]
            numConnections = len(fields) - 1
            connections = fields[-numConnections:]

            color = 'WHITE'
            distance = 9999

            if (heroID == sys.argv[1]) :
                color = 'GRAY'
                distance = 0

            if (heroID != ''):
                edges = ','.join(connections)
                outStr = '|'.join((heroID, edges, str(distance), color))
                out.write(outStr)
                out.write("\n")

    f.close()

out.close()
