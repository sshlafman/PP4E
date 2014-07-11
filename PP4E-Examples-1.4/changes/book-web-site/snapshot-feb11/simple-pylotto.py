# Python 2.X last resort version!

students = []
for line in open('student.txt'):
	students.append(line.rstrip())

import time
for student in students:
	print student	
	time.sleep(0.5)

import random
print 'Winner:', random.choice(students)


# or, for ex-Perl programmers...
"""
print random.choice([line.rstrip() for line in open('students.txt')])
"""

