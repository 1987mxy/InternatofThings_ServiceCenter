#coding=UTF-8
'''
Created on 2012-8-14

@author: Moxiaoyong
'''

import time
from struct import unpack

class MyKey(object):
	'''
	保卫者，用来建立TCP连接后的动态口令校验
	'''

	def __init__(self):
		'''
		Constructor
		'''
		self.__now = 0
		self.switch = True
		
	def __read(self):
		self.__now = int( time.time() )
		
		keyFile = open('./lib/Securer/Key','rb')
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
