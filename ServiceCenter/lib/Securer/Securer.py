'''
Created on 2012-8-14

@author: Moxiaoyong
'''

import time
from struct import unpack

class Securer(object):
	'''
	classdocs
	'''

	def __init__(self):
		'''
		Constructor
		'''
		self.__now = 0
		self.switch = True
		
	def read(self):
		self.__now = int( time.time() )
		
		keyFile = open('./Key','rb')
		packTime = keyFile.read(8)
		keyTime = unpack( '<Q', packTime )

		keySeek = ( ( ( self.__now - keyTime[0] ) / 60 ) - 1 ) * 4
		keyFile.seek( keySeek + 8 )
		keyBin = keyFile.read( 8 )
		keyFile.close()
		
		keyNum = len( keyBin ) / 4
		keyList = unpack( '<'+'L'*keyNum , keyBin )
		return keyList
		
	def check(self, key):
		if not self.switch: return True
		return ( int(key) in self.__read() ) 

#unit test
t = Securer()
print t.read()