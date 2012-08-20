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
		self.__public_key = None;
		self.__private_key = None;
		
	def generate(self):
		( self.__public_key, self.__private_key ) = rsa.newkeys( 370, poolsize=4 )		#md5+4byte需要370
		
	def publicEncrypt(self, data):
		return rsa.encypt( data, self.__public_key )
	
	def privateEncrypt(self, data):
		return rsa.encypt( data, self.__private_key )
	
	def publicDecrypt(self, data):
		return rsa.decypt( data, self.__public_key )
	
	def privateDecrypt(self, data):
		return rsa.decypt( data, self.__private_key )