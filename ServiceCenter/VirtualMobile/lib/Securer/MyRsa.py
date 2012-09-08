#coding=UTF-8
'''
Created on 2012-8-21

@author: XPMUser
'''

from Crypto.Random import random
from Crypto.PublicKey import RSA

class MyRsa(object):
	'''
	RSA加密类
	'''

	def __init__(self):
		'''
		Constructor
		'''
		self.__publicKey = None;
		self.__privateKey = None;
		
	def generate(self):
		self.__privateKey = RSA.generate( 1024 )
		self.__publicKey = self.__privateKey.publickey()
		
	def publicCrypt(self, operate, data):
		if operate == 'encrypt':
			return self.__publicKey.encrypt( data, random.randint( 0, 999999 ) )[ 0 ]
		elif operate == 'decrypt':
			return self.__publicKey.decrypt( data )

	def privateCrypt(self, operate, data):
		if operate == 'encrypt':
			return self.__privateKey.encrypt( data, random.randint( 0, 999999 ) )[ 0 ]
		elif operate == 'decrypt':
			return self.__privateKey.decrypt( data )
	
	def getPubKey(self):
		return self.__publicKey.exportKey( 'DER' )
	
	def setPubKey(self, publicKey):
		self.__publicKey = RSA.importKey( publicKey )
	
#===============================================================================
# #unit testing
# if __name__=='__main__':
#	myRsa = MyRsa()
#	myRsa.generate()
#	bk = myRsa.getPubKey()
#	print 'bk:%d'%len( bk )
#	
#	_myRsa = MyRsa()
#	_myRsa.setPubKey( bk )
#	c = _myRsa.publicCrypt( 'encrypt', '1987mxy' )
#	print 'c:%d'%len( c )
# 
#	print myRsa.privateCrypt( 'decrypt', c )
#===============================================================================