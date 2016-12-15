from pprint import pprint
import re
from collections import defaultdict
from itertools import chain, combinations
from copy import deepcopy
import pickle

class Scheduler:
    def __init__(self, quota = 2):
        self.courselist = defaultdict(list)
        self.quota = quota # Take quota amount of classes at most every semester
        self.START = "START"
        self.END = "END"
        self.semester_restrictions = {}
        self.electives = {}
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
        courses = []
        for course in self.courselist:
            match = re.match('^.*\.([1-9][0-9]+)(\..*)?$', course)
            if match and int(match.group(1)) >= course_number:
                courses.append(course)
        #self.electives[elective] = courses
        #self.electives['elective1'] = ['math.145', 'math.61']
        #self.electives['elective2'] = ['math.126', 'math.128', 'math.161', 'math.162']

    def grad_requirement(self, reqs):
        #elec_combs = self.get_combs()
        #print elec_combs
        elec_combs = []
        
        for req in reqs:
            for comb in elec_combs:
                if self.mutually_exclusive(req, comb):
                    self.add_course(self.END, prereqs = [req + comb])
    def schedule(self):
        seqs = self.fulfill_req(self.END, [[self.START]])
        filename = 'applied_math_major_' + str(self.quota) + '.pickle'
        pickle.dump(seqs, open(filename, 'wb')) 

    def fulfill_req(self, course, seq):
        seqs = []
        # For each set of requirements that satisfy this course
        for reqs in self.courselist[course]:
            newseqs = [deepcopy(seq)]
            for precourse in reqs:
                if precourse not in chain(*newseqs[0]):
                    newseqs = self.fulfill_req(precourse, newseqs[0])

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
        return self.get_smallest(seqs)
    def fulfill_electives(self, elective, seq, req):
        #elective_req = [r for r in req if type(r) == dict][0]
        seqs = []
        all_combs = self.get_combs()
        for comb in all_combs:
            if self.havent_taken(comb, seq):
                seqs += self.fulfill_comb(comb, seq)
                print comb
                break
        return self.get_smallest(seqs)


    def get_combs(self):
        all_combs = []
        for comb1 in self.electives['elective1']:
            for comb2 in self.electives['elective2']:
                for comb3 in self.electives['math.61+']:
                    if comb1 != comb2 and comb2 != comb3 and comb1 != comb3:
                        all_combs.append([comb1, comb2, comb3])
        return all_combs

    def mutually_exclusive(self, comb1, comb2):
        for c1 in comb1:
            if c1 in comb2:
                return False
        return True
    def fulfill_comb(self, comb, seq):
        seqs = []

        # For each set of requirements that satisfy this course
        for reqs in comb:
            precourse = reqs[0]
            seqs2 = []
            if reqs[0] not in chain(*seq):
                seqs2 += [self.fulfill_req(reqs[0], deepcopy(seq))]


        return self.get_smallest(seqs)


    def get_smallest(self, seqs):
        min_len = min(len(s) for s in seqs)
        seqs = [s for s in seqs if len(s) == min_len]  
        min_len = min(len([c for c in chain(*s) if c != None]) for s in seqs)
        return [s for s in seqs if \
                len([c for c in chain(*s) if c != None]) == min_len] 


    def havent_taken(self, comb, seq):
        for course in chain(*seq):
            for c in comb:
                if c[0] == course:
                    return False
        return True

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

    s.add_electives('math.61+', 61)
    s.grad_requirement([['math.42', 'math.70', 'math.51', 'math.87', 'math.158' 'math.135', 'math.136', 'math.126', 'math.128']])
    '''
                        ['math.44', 'math.70', 'math.51', 'math.87', 'math.158' 'math.135', 'math.136', 'math.126', 'math.128'],
                        ['math.42', 'math.70', 'math.150.chaos', 'math.87', 'math.158' 'math.135', 'math.136', 'math.126', 'math.128'],
                        ['math.44', 'math.70', 'math.150.chaos', 'math.87', 'math.158' 'math.135', 'math.136', 'math.126', 'math.128'],
                        ['math.42', 'math.70', 'math.51', 'math.87', 'math.158' 'math.135', 'math.136', 'math.161', 'math.162'], 
                        ['math.44', 'math.70', 'math.51', 'math.87', 'math.158' 'math.135', 'math.136', 'math.161', 'math.162'],
                        ['math.42', 'math.70', 'math.150.chaos', 'math.87', 'math.158' 'math.135', 'math.136', 'math.161', 'math.162'],
                        ['math.44', 'math.70', 'math.150.chaos', 'math.87', 'math.158' 'math.135', 'math.136', 'math.161', 'math.162']])'''

    s.schedule()
