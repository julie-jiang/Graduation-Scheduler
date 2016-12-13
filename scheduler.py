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
        print "RESULTS: ", seq
    def fulfill_req(self, node, seq):
        print "fulfilling", node
        
        # For each set of requirements that satisfy this node
        seqs = []
        for reqs in self.graph[node]:
            print "at node ", node, " reqs = ", reqs
            newseq = seq[:]
            for class_ in reqs:
                print "at node ", node, " class_ = ", class_
                if class_ not in newseq:
                    newseq= self.fulfill_req(class_, newseq)
                    print "at node ", node, " newseq: ", newseq
            if not re.match('.*\+', node):
                newseq.append(node)
            print "at node ", node, " reqs = ", reqs, " newseq: ", newseq
            if newseq != seq[:]:
                seqs.append(newseq)

        print "at node ", node, " seqs: ", seqs
        min_len = min(len(s) for s in seqs)
        s = min(seqs, key = lambda x: len(x))
        print "at node ", node , " best seq: ", s
        return s

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
                       ['math.150.time'], \
                       ['math.150.data'], ['math.150.poverty'], \
                       ['math.150.chaos'], ['math.150.scicomp'], ['math.158'],\
                       ['math.161'], ['math.162'], ['math.168'])
    s.add('math.50+', ['math.51'], ['math.61'], ['math.63'], ['math.87'], \
                      ['math.104'], ['math.112'], ['math.126'], \
                      ['math.128'], \
                      ['math.150.time'], ['math.150.data'], \
                      ['math.150.poverty'], ['math.150.chaos'], \
                      ['math.150.scicomp'], ['math.158'], ['math.161'], \
                      ['math.162'], ['math.168'])
  
    s.add(END, ['math.42', 'math.70', 'math.135', 'math.145', \
                'math.136', 'math.100+', 'math.50+'])
    s.add(END, ['math.42', 'math.70', 'math.135', 'math.145', \
                'math.146', 'math.100+', 'math.50+'])
    #pprint(s.graph)
    #print
    s.shortest_path()


