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
	server = {}

	def __init__(self, socket, address):
		'''
		服务抽象类
		'''
		if self.class__ is Service:	#抽象类不能实例化
			LOG.error('Net class dose not instantiation')
			raise 'Net class dose not instantiation'
		
		Service.server[ address ] = self
		
		self.address = address
		self.sock = socket
		self.switch = True
		self.isAlive = True
		self.pid = 0
		self.packQueue = []
		self.timeout = 30

		self.recvThread = None
		self.mainThread = None
		self.chkThread = None
		self.commCondition = None
		
		self.magicCode = None
		self.heartCode = None
		self.headerStruct = None
		self.headerSize = None
		
		self.packager = None
		
	def config(self, config):
		self.magicCode = config.magicCode
		self.heartCode = config.heartCode
		self.headerStruct = config.headerStruct
		self.headerSize = calcsize( self.headerStruct )
		self.timeout = config.timeout
		
	def setPackager(self, packager):
		self.packager = packager
		
	def running(self):
		self.commCondition = threading.Condition()
		self.recvThread = threading.Thread( target = self.receive )
		self.mainThread = threading.Thread( target = self.main )

	def shutdown(self):
		LOG.error('%s shutdown !'%self.address)
		self.switch = False

	def receive(self):
		try:
			sourceStream = ''
			while self.switch:
				LOG.debug( '%s receiving...' % self.address )
				recvStream = self.sock.recv( 1000 )
				LOG.debug( 'receive raw stream from %s : ' % self.address, recvStream )
				if recvStream:
					self.isAlive = True
					sourceStream = self.parseHeader( '%s%s' % ( sourceStream, recvStream ) )
				else:
					LOG.info( '%s disconnect...' % self.address )
					self.shutdown()
		except:
			LOG.error( 'receive error : %s' % format_exc() )
			LOG.error('%s receive error : %s'%( self.address, 
											    format_exc() ) )
			self.shutdown()

	def parseHeader(self, stream):
		if len(stream) >= self.headerSize:
			head = unpack(self.headStruct, stream[ : self.headerSize])
			if head[1] != self.magicCode:
				LOG.error('receive invalid package from %s : '%self.address, stream)
				self.shutdown()
			if head[0] + 2 <= len(stream):
				mStream = stream[self.headerSize : head[0] + 2]
				stream = stream[head[0] + 2 : ]
				if head[2] != self.heartCode:
					self.packQueue.insert(0, [head[3], head[2], mStream])
					self.commCondition.notify()
				stream = self.parseHead(stream)
		return stream

	def chkHeart(self):
		while self.isAlive and self.switch:
			self.isAlive = False
			sleep( self.timeout )
		if self.switch:
			LOG.error('%s heart time out !'%self.address)
			self.shutdown()
			
	def send(self, stream):
		LOG.debug( '%s send raw stream : ' % self.address, stream )
		self.sock.sendall( stream )
	
	@staticmethod
	def broadcast(self, data, destAddr=''):
		if destAddr:
			Service.server[ destAddr ].__packQueue.append( data )
			Service.server[ destAddr ].__commCondition.notify()
		else:
			for srv in Service.server.values():
				srv.__packQueue.append( data )
				srv.__commCondition.notify()
		
	def main(self, data):
		pass