#coding=UTF-8
'''
Created on 2012-8-21

@author: XPMUser
'''

import rsa

class MyRsa(object):
	'''
	classdocs
	'''

	def __init__(self):
		'''
		Constructor
		'''
		self.__publicKey = None;
		self.__privateKey = None;
		
	def generate(self):
		( self.__publicKey, self.__privateKey ) = rsa.newkeys( 178 )		#8byte(desKey)+4byte(myKey)需要178
		
	def publicCrypt(self, operate, data):
		if operate == 'encrypt':
			return rsa.encrypt( data, self.__publicKey )
		elif operate == 'decrypt':
			return rsa.decrypt( data, self.__publicKey )

	def privateCrypt(self, operate, data):
		if operate == 'encrypt':
			return rsa.encrypt( data, self.__privateKey )
		elif operate == 'decrypt':
			return rsa.decrypt( data, self.__privateKey )
	
	def getPubKey(self):
		return self.__publicKey._save_pkcs1_der()