from pprint import pprint
import re
from collections import defaultdict
from itertools import chain, combinations
from copy import deepcopy
import numpy
import pickle

class Sensitivity:
    def __init__(self):
        self.courselist = defaultdict(list)
        self.START = "START"
        self.END = "END"
        self.semester_restrictions = {}
        self.freefloats = defaultdict(list)
        
    def add_course(self, course, prereqs = None, semester = None):
        if prereqs == None:
            self.courselist[course]= [[self.START]]
        else:
            for pr in prereqs:
            #  Maps a course to a list of sets of courses that can fulfill it
                self.courselist[course].append(pr)
        if semester != None:
            self.semester_restrictions[course] = semester

    def get_semesters(self):
        semesters = []
        for i in range(self.num_semesters):
            semesters.append([])
        return semesters
    def calculate_floats(self, seq):

        self.num_semesters = len(seq) - 2 
        self.quota = len(seq[1])
        
        #pprint(seq)
        none_indices = self.get_none_indices(seq)
        for i, sem in enumerate(seq):
            for course in sem:
                if course != None and course != self.START and course != self.END:
                    for j in none_indices:
                        if j > i and self.can_be_delayed(course, i, j, seq) \
                            and self.satisfy_semester(course, j):
                            freefloat = j - i
                            self.freefloats[course].append(freefloat)
                            break
                    else:
                        self.freefloats[course].append(0)


                            
                        


    def can_be_delayed(self, course, i, j, seq):
        for sem in seq[i:j + 1]:
            for course2 in sem:
                if course in chain(*self.courselist[course2]):
                    return False
        return True
    def get_semester_index(self, seq, course):
        for i, sem in enumerate(seq):
            if course in sem:
                return i
    def get_none_indices(self, seq):
        none_indices = []
        for i in range(self.num_semesters, 0 , -1):
            for j in range(self.quota - 1, -1, -1):
                if seq[i][j] == None:
                    none_indices.append(i)
                    break
        return none_indices
    def print_floats(self):
        floats = {}
        for course in self.freefloats:
            floats[course] = numpy.mean(self.freefloats[course])
        pprint(floats)

    def satisfy_semester(self, course, index):
        if course not in self.semester_restrictions:
            return True
        semester = 'f' if index % 2 != 0 else 's'
        return self.semester_restrictions[course] == semester
    def satisfy_requirements(self, course, index, seq):
        for req in self.courselist[course]:
            if self.satisfy_one_req(course, index, seq, req):
                return True

        return False
    def satisfy_dependency(self, course, index, seq):
        for i, sem in enumerate(seq[:index + 1]):
            for precourse in sem:
                if course in chain(*self.courselist[precourse]):
                    if not self.satisfy_requirements(precourse, i, seq):
                        return False

        return True
        
    def satisfy_one_req(self, course, index, seq, req):
        for precourse in req:
            if precourse not in chain(*seq[:index]):
                return False
        return True


if __name__ == "__main__":
    s = Sensitivity()
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
    

    sequences = pickle.load(open('math_major_3.pickle', 'rb'))
    for seq in sequences: 
        s.calculate_floats(seq)
    seq = [['START'],
          ['math.34', None, None],
          ['math.42', 'math.70', 'math.112'],
          ['math.135', 'math.145', 'math.87'],
          ['math.136', 'math.158', 'math.146'],
          ['math.161', None, None],
          ['END', None, None]]
    #s.calculate_floats(seq)
    s.print_floats()
