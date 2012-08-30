'''
Created on 2012-8-30

@author: XPMUser
'''

import re, threading

class MyClass(object):
	def __init__(self):
		print type(re)
		print type(threading)

	def test(self):
		print type(re)
		print type(threading)

from sys import modules
modules[__name__]=MyClass()
