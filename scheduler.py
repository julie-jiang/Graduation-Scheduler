from pprint import pprint
import re
from collections import defaultdict
from itertools import chain
from copy import deepcopy

class Scheduler:
    def __init__(self, quota = 2):
        self.courselist = defaultdict(list)
        self.quota = quota # Take quota amount of classes at most every semester
        self.START = "START"
        self.END = "END"
        self.semester_restrictions = {}
        self.electives = set()
    def add_course(self, course, prereqs = None, semester = None):
        if prereqs == None:
            self.courselist[course]= [[self.START]]
        else:
            for pr in prereqs:
            #  Maps a course to a list of sets of courses that can fulfill it
                self.courselist[course].append(pr)
        if semester != None:
            self.semester_restrictions[course] = semester
    def add_electives(self, elective, course_number):
        self.electives.add(elective)
        courses = []
        for course in self.courselist:
            match = re.match('^.*\.([1-9][0-9]+)(\..*)?$', course)
            if match and int(match.group(1)) >= course_number:
                courses.append([course])
        self.add_course(elective, courses)

    def grad_requirement(self, reqs):
        self.add_course(self.END, prereqs = reqs)

    def schedule(self):
        
        seqs = self.fulfill_req(self.END, [[self.START]])
        print "RESULTS: "
        pprint(seqs) 

    def fulfill_req(self, course, seq):
        seqs = []
        # For each set of requirements that satisfy this course
        for reqs in self.courselist[course]:
            newseqs = [deepcopy(seq)]
            for precourse in reqs:
                if precourse not in chain(*newseqs[0]):
                    if type(precourse) != dict:
                        newseqs = self.fulfill_req(precourse, newseqs[0])
                    else:
                        newseqs = self.fulfill_electives(precourse, newseqs[0], reqs)

            for s in newseqs:
                none_indices = [(i, semester.index(None)) for i, semester \
                                 in enumerate(s) if None in semester \
                                 and i > 0]
                for i, j in none_indices:
                    if self.satisfy_semester(course, i, sequence = s, prereqs = reqs):
                        s[i][j] = course
                        break
                else:
                    while True:
                        new_sem = [None] * self.quota
                        s.append(new_sem)
                        if self.satisfy_semester(course, len(s) - 1):
                            s[-1][0] = course
                            break
                seqs.append(s)
        min_len = min(len(s) for s in seqs)
        seqs = [s for s in seqs if len(s) == min_len]  
        min_len = min(len([c for c in chain(*s) if c != None]) for s in seqs)
        return [s for s in seqs if \
                len([c for c in chain(*s) if c != None]) == min_len] 
    def fulfill_electives(self, elective, seq, req):
        elective_req = [r for r in req if type(r) == dict][0]
        for elective in elective_req:
            seqs = self.fulfill_elec(elective, seq)
        print "seqs with electives fulfilled: "
        pprint(seqs)
        return seqs
    def fulfill_elec(self, elective, seq):
        print "fulfilling elective", elective
        seqs = []
        for reqs in self.courselist[elective]:
            if reqs[0] not in chain(*seq):
                seqs += self.fulfill_req(reqs[0], seq)
                
        min_len = min(len(s) for s in seqs)
        seqs = [s for s in seqs if len(s) == min_len]  
        min_len = min(len([c for c in chain(*s) if c != None]) for s in seqs)
        return [s for s in seqs if \
                len([c for c in chain(*s) if c != None]) == min_len] 


    def satisfy_semester(self, course, index, **kwargs):
        if kwargs:
            for precourse in kwargs['prereqs']:
                if precourse not in chain(*kwargs['sequence'][:index]):
                    return False
        if course not in self.semester_restrictions:
            return True
        semester = 'f' if index % 2 != 0 else 's'
        return self.semester_restrictions[course] == semester





if __name__ == "__main__":
    s = Scheduler(3)
    s.add_course('math.21')
    s.add_course('math.32')
    s.add_course('math.34')
    s.add_course('math.39', semester = 'f')
    s.add_course('math.42', prereqs = [['math.34']])
    s.add_course('math.44', prereqs = [['math.39'], ['math.34', 'math.70']],
                            semester = 's')
    s.add_course('math.51', prereqs = [['math.42']])
    s.add_course('math.61', prereqs = [['math.32']])
    s.add_course('math.63', prereqs = [['math.32']], semester = 's')
    s.add_course('math.70', prereqs = [['math.34'], ['math.39']])
    s.add_course('math.87', prereqs = [['math.34', 'math.70'], \
                                       ['math.39', 'math.70']])
    s.add_course('math.112', prereqs = [['math.34'], ['math.39']] ,semester = 's')
    s.add_course('math.126', prereqs = [['math.51']], semester = 'f')
    s.add_course('math.128', prereqs = [['math.70']], semester = 's')
    s.add_course('math.135', prereqs = [['math.34', 'math.70'], \
                                        ['math.39', 'math.70']], semester = 'f')
    s.add_course('math.136', prereqs = [['math.135']], semester = 's')
    s.add_course('math.145', prereqs = [['math.70']], semester = 'f')
    s.add_course('math.146', prereqs = [['math.145']], semester = 's')
    s.add_course('math.150.time', prereqs = [['math.42', 'math.21'], \
                                             ['math.44', 'math.21']],
                                  semester = 's')
    s.add_course('math.150.data', prereqs = [['math.70']], semester = 's')
    s.add_course('math.150.poverty', prereqs = [['math.42'], ['math.44']], 
                                     semester = 'f')
    s.add_course('math.150.chaos', prereqs = [['math.51']], semester = 'f')
    s.add_course('math.150.scicomp', prereqs = [['math.70']], semester = 'f')
    s.add_course('math.158', prereqs = [['math.42'], ['math.44']], semester = 's')
    s.add_course('math.161', prereqs = [['math.42'], ['math.44']], semester = 'f')
    s.add_course('math.162', prereqs = [['math.161']], semester = 's')
    s.add_course('math.168', prereqs = [['math.135', 'math.145']], semester = 's')

    s.add_electives('math.100+', 100)
    s.add_electives('math.50+', 50)
    
    elective_req = {'math.50+': 1}
    s.grad_requirement([['math.42', 'math.70', 'math.135', 'math.145',
                         'math.136', elective_req], 
                         ['math.42', 'math.70', 'math.135', 'math.145',
                         'math.146', elective_req],
                         ['math.44', 'math.70', 'math.135', 'math.145',
                         'math.136', elective_req],
                         ['math.44', 'math.70', 'math.135', 'math.145',
                         'math.146', elective_req]])

    s.schedule()
