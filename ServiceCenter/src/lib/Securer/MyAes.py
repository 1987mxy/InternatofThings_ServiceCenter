#coding=UTF-8
'''
Created on 2012-9-8

@author: XPMUser
'''

from struct import pack

from Crypto import Random
from Crypto.Random import random
from Crypto.Cipher import AES

class MyAes(object):
	'''
	AES加密类
	'''

	def __init__(self):
		'''
		Constructor
		'''
		self.__key = None
		self.__aesKey = None
		self.__iv = None

	def generate(self):
		if self.__key == None or self.__iv == None:
			self.rndKey()
		self.__aesKey = AES.new( self.__key, AES.MODE_CFB, self.__iv )
		
	def crypt(self, operate, data):
		if operate == 'encrypt':
			return self.__aesKey.encrypt( data )
		elif operate == 'decrypt':
			return self.__aesKey.decrypt( data )
		
	def rndKey(self):
		intKey1 = random.randrange( 0xFFFFFFFFFFFFFFFF )
		intKey2 = random.randrange( 0xFFFFFFFFFFFFFFFF )
		self.__key = pack( '<QQ', intKey1, intKey2 )
		self.__iv = Random.new().read( AES.block_size )
	
	def getKey(self):
		return self.__key + self.__iv
	
	def setKey(self, key):
		self.__key = key[:16]
		self.__iv = key[16:]
		self.generate()
		
#unit testing
if __name__=='__main__':
	myAes = MyAes()
	myAes.generate()
	key = myAes.getKey()
	print 'key:%d'%len(key)
	c = myAes.crypt( 'encrypt', '1987mxy' )
	print 'c:%d'%len(c)
	
	_myAes = MyAes()
	_myAes.setKey( key )
	_myAes.generate()
	print _myAes.crypt( 'decrypt', c )
