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
		
	def encrypt(self, plaintext):
		return self.__desKey.encrypt( plaintext )
	
	def decrypt(self, ciphertext):
		return self.__desKey.decrypt( ciphertext )
