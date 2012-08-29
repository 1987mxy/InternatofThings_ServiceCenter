'''
Created on 2012-8-29

@author: XPMUser
'''

class ParentClass(object):
	_test = 5

	def __init__(self):
		self._test1 = 10
	
class ChildClass(ParentClass):
		
	def run(self):
		print self._test1
		print ChildClass._test
	
if __name__=='__main__':
	c = ChildClass()
	c.run()
	print ChildClass._test
	print c._test1