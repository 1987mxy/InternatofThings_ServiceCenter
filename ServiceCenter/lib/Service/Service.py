#coding=UTF-8
'''
Created on 2012-8-14

@author: Moxiaoyong
'''

import threading
from time import sleep

from traceback import format_exc
from struct import unpack, calcsize

from lib.Log import LOG

class Service(object):
	'''
	服务抽象类
	'''

	def __init__(self, socket, address):
		'''
		服务抽象类
		'''
		if self.__class__ is Service:	#抽象类不能实例化
			LOG.error('Net class dose not instantiation')
			raise 'Net class dose not instantiation'
		
		self.__address = address
		self.__sock = socket
		self.__switch = True
		self.__isAlive = True
		self.__pid = 0
		self.__packQueue = []
		self.__timeout = 30

		self.__recvThread = None
		self.__mainThread = None
		self.__chkThread = None
		self.__commCondition = None
		
		self.__magicCode = None
		self.__heartCode = None
		self.__headerStruct = None
		self.__headerSize = None
		
		self.__packager = None
		
	def config(self, config):
		self.__magicCode = config.magicCode
		self.__heartCode = config.heartCode
		self.__headerStruct = config.headerStruct
		self.__headerSize = calcsize( self.__headerStruct )
		self.__timeout = config.timeout
		
	def setPackager(self, packager):
		self.__packager = packager
		
	def running(self):
		self.__commCondition = threading.Condition()
		self.__recvThread = threading.Thread( target = self.receive )
		self.__mainThread = threading.Thread( target = self.main )
	
	def receive(self):
		try:
			sourceStream = ''
			while self.__switch:
				LOG.debug( '%s receiving...' % self.__address )
				recvStream = self.__sock.recv( 1000 )
				LOG.debug( 'receive raw stream from %s : ' % self.__address, recvStream )
				if recvStream:
					self.__isAlive = True
					sourceStream = self.parseHeader( '%s%s' % ( sourceStream, recvStream ) )
				else:
					LOG.info( '%s disconnect...' % self.__address )
					self.shutdown()
		except:
			LOG.error( 'receive error : %s' % format_exc() )
			LOG.error('%s receive error : %s'%( self.__address, 
											    format_exc() ) )
			self.shutdown()

	def parseHeader(self, stream):
		if len(stream) >= self.__headerSize:
			head = unpack(self.__headStruct, stream[ : self.__headerSize])
			if head[1] != self.__magicCode:
				LOG.error('receive invalid package from %s : '%self.__address, stream)
				self.shutdown()
			if head[0] + 2 <= len(stream):
				mStream = stream[self.__headerSize : head[0] + 2]
				stream = stream[head[0] + 2 : ]
				if head[2] != self.__heartCode:
					self.__packQueue.insert(0, [head[3], head[2], mStream])
					self.__commCondition.notify()
				stream = self.parseHead(stream)
		return stream

	def chkHeart(self):
		while self.__isAlive and self.__switch:
			self.__isAlive = False
			sleep( self.__timeout )
		if self.__switch:
			LOG.error('%s heart time out !'%self.__address)
			self.shutdown()
			
	def send(self, stream):
		LOG.debug( '%s send raw stream : ' % self.__address, stream )
		self.__sock.sendall( stream )
		
	def shutdown(self):
		LOG.error('%s shutdown !'%self.__address)
		self.__switch = False
		
	def main(self, data):
		pass