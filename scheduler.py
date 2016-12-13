from Queue import PriorityQueue
from pprint import pprint
import re
from collections import defaultdict
import itertools
START = "START"
END = "END"
class Scheduler:
    def __init__(self):
        self.graph = defaultdict(list)
    def add(self, node, *prenodes):
        for pn in prenodes:
            #  Maps a class to a list of sets that can fulfill it
            self.graph[node].append(pn)
    def shortest_path(self):
        dist = {}
        for node in self.graph:
            dist[node] = float("inf")
        # Set of nodes that are fulfilled
        fulfilled = set([START])
        seq = [START]
        seq = self.fulfill_req(END, seq)
        print "RESULTS: "
        pprint(seq)
    def fulfill_req(self, node, seq):
        print "fulfilling", node
        
        # For each set of requirements that satisfy this node
        seqs = []
        for reqs in self.graph[node]:
            print "at node ", node, " reqs = ", reqs
            newseqs = [seq[:]]
            for class_ in reqs:
                print "at node ", node, " class_ = ", class_
                if class_ not in newseqs[0]:
                    newseqs = self.fulfill_req(class_, newseqs[0])
                    print "at node ", node, " newseq: ", newseqs
            if not re.match('.*\+', node):
                for s in newseqs:
                    s.append(node)
            print "at node ", node, " reqs = ", reqs, " newseq: ", newseqs
            for s in newseqs:
                if s != seq[:]:
                    seqs.append(s)

        print "at node ", node, " seqs: ", seqs
        min_len = min(len(s) for s in seqs)
        return [s for s in seqs if len(s) == min_len]


if __name__ == "__main__":
    
    all_classes = set(['math.21', 'math.32', 'math.34', 'math.42', 
                       'math.51', 'math.61', 'math.63', 'math.70', 
                       'math.87', 'math.104', 'math.112', 'math.126', 'math.128', \
                       'math.135', 'math.136', 'math.145', 'math.146', \
                       'math.150.time', 'math.150.data', 'math.150.poverty', \
                       'math.150.chaos', 'math.150.scicomp', 'math.158', \
                       'math.161', 'math.162', 'math.168'])
    s = Scheduler()
    s.add('math.21', [START])
    s.add('math.32', [START])
    s.add('math.34', [START])
    s.add('math.42', ['math.34'])
    s.add('math.51', ['math.42'])
    s.add('math.61', ['math.32'])
    s.add('math.63', ['math.32'])
    s.add('math.70', ['math.34'])
    s.add('math.87', ['math.34', 'math.70'])
    s.add('math.104', [START])
    s.add('math.112', ['math.34'])
    s.add('math.126', ['math.51'])
    s.add('math.128', ['math.70'])
    s.add('math.135', ['math.34', 'math.70'])
    s.add('math.136', ['math.135'])
    s.add('math.145', ['math.70'])
    s.add('math.146', ['math.145'])
    s.add('math.150.time', ['math.42', 'math.21'])
    s.add('math.150.data', ['math.70'])
    s.add('math.150.poverty', ['math.42'])
    s.add('math.150.chaos', ['math.51'])
    s.add('math.150.scicomp', ['math.70'])
    s.add('math.158', ['math.42'])
    s.add('math.161', ['math.42'])
    s.add('math.162', ['math.161'])
    s.add('math.168', ['math.135', 'math.145'])

    s.add('math.100+', ['math.104'], ['math.112'], ['math.126'], ['math.128'],\
                       ['math.150.time'], ['math.136'], ['math.146'], \
                       ['math.150.data'], ['math.150.poverty'], \
                       ['math.150.chaos'], ['math.150.scicomp'], ['math.158'],\
                       ['math.161'], ['math.162'], ['math.168'])
    s.add('math.50+', ['math.51'], ['math.61'], ['math.63'], ['math.87'], \
                      ['math.104'], ['math.112'], ['math.126'], \
                      ['math.128'], ['math.136'], ['math.146'], \
                      ['math.150.time'], ['math.150.data'], \
                      ['math.150.poverty'], ['math.150.chaos'], \
                      ['math.150.scicomp'], ['math.158'], ['math.161'], \
                      ['math.162'], ['math.168'])
  
    s.add(END, ['math.42', 'math.70', 'math.135', 'math.145', \
                'math.136', 'math.100+', 'math.100+', 'math.50+', \
                'math.50+', 'math.50+'])
    s.add(END, ['math.42', 'math.70', 'math.135', 'math.145', \
                'math.136', 'math.100+', 'math.100+', 'math.50+', \
                'math.50+', 'math.50+'])
    #pprint(s.graph)
    #print
    s.shortest_path()


