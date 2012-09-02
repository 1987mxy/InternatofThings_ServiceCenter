#coding=UTF-8
'''
Created on 2012-8-28

@author: XPMUser
'''

from pyDes import *

class MyDes(object):
	'''
	classdocs
	'''

	def __init__(self, key=''):
		'''
		Constructor
		'''
		if key == '':
			from random import randrange, seed
			from time import time
			from struct import pack
			seed( time() )
			intKey = randrange( 18446744073709551615 )
			self.__key = pack( '<Q', intKey )
		else:
			self.__key = key
		self.__generate()
		
	def setKey(self, key):
		self.__key = key
		self.__generate()
		
	def __generate(self):
		self.__desKey = des( self.__key, CBC, bytearray( 8 ), pad=None, padmode=PAD_PKCS5 )
		
	def crypt(self, operate, data):
		if operate == 'encrypt':
			return self.__desKey.encrypt( data )
		elif operate == 'decrypt':
			return self.__desKey.decrypt( data )

	def getKey(self):
		return self.__key