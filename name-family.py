 #!/usr/bin/python
class Student:
	courseMarks={}
	name= ""
	def __init__(self, name, family):
		self.name = name
		self.family = family
		print self.name
		print self.family
		
    	def addCourseMark(self, course, mark):
        	self.courseMarks[course] = mark
		print self.courseMarks
        
    	def average(self):
		a = 0
        	for course, mark in self.courseMarks.iteritems():
			a = a + mark
		print a
		number_courseMarks = len(self.courseMarks)
		avg = a/number_courseMarks
		print avg
			
student = Student('a','a')
student.addCourseMark(0,15)
student.addCourseMark(1,15)
student.addCourseMark(2,30)
student.average()
