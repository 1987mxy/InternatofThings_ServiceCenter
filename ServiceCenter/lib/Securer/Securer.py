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
		#time 5byte
		#keyString unit 4byte 
		packTime = keyFile.read(8)
		keyTime = unpack( '<Q', packTime )
		print self.__now - keyTime[0]
		keySeek = ( ( ( self.__now - keyTime[0] ) / 60 ) - 1 ) * 4
		print keySeek
		keyFile.seek( keySeek + 8 )
		keyBin = keyFile.read( 8 )
		print keyBin.__repr__()
		keyFile.close()
		keyList = unpack( '<LL', keyBin )
		return keyList
	
	def check(self, key):
		if not self.switch: return True
		return ( int(key) in self.__read() ) 

#unit test
t = Securer()
print t.read()
