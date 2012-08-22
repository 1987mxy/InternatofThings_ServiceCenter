'''
Created on 2012-8-22

@author: XPMUser
'''

from lib.Log import LOG

class Listener(object):
	'''
	classdocs
	'''

	def __init__(self):
		'''
		构造函数
		'''
		if self.__class__ is Listener:	#抽象类不能被实例化
			LOG.error('Listener class dose not instantiation')
			raise 'Listener class dose not instantiation'
		
		