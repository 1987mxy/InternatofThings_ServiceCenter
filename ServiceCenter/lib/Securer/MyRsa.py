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
		
	def publicEncrypt(self, data):
		return rsa.encrypt( data, self.__publicKey )
	
	def privateEncrypt(self, data):
		return rsa.encrypt( data, self.__privateKey )
	
	def publicDecrypt(self, data):
		return rsa.decrypt( data, self.__publicKey )
	
	def privateDecrypt(self, data):
		return rsa.decrypt( data, self.__privateKey )
	
	def getPubKey(self):
		return self.__publicKey._save_pkcs1_der()