#coding=UTF-8
'''
Created on 2012-8-14

@author: Moxiaoyong
'''

import threading
from time import sleep
from traceback import format_exc
from struct import unpack, calcsize
from socket import SHUT_RDWR

from lib.Global import Logger, Packager, TerminalManager
from lib.Config import srvCenterConf

class Service(object):
	'''
	服务抽象类
	'''
	server = {}

	def __init__(self, socket, address):
		'''
		服务抽象类
		'''
		if self.__class__ is Service:	#抽象类不能实例化
			Logger.error('Net class dose not instantiation')
			raise Exception( 'Net class dose not instantiation' )
		
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
		self.mainThreadName = None
		self.chkThread = None
		self.commCondition = None
		
		self.magicCode = None
		self.heartCode = None
		self.headerStruct = None
		self.headerSize = None
		
		self.packager = None
		self.terminalManager = None
		
		self.config( srvCenterConf )
		self.setPackager( Packager )
		self.setTerminalManager( TerminalManager )
		
	def config(self, config):
		self.magicCode = config.magicCode
		self.heartCode = config.heartCode
		self.headerStruct = config.headerStruct
		self.headerSize = calcsize( self.headerStruct )
		self.timeout = config.timeout
		
	def setPackager(self, packager):
		self.packager = packager
		
	def setTerminalManager(self, terminalManager):
		self.terminalManager = terminalManager
	
	def running(self):
		self.commCondition = threading.Condition()
		self.recvThread = threading.Thread( target = self.receive )
		self.mainThread = threading.Thread( target = self.main )
		self.mainThreadName = self.mainThread.getName()

	def shutdown(self):
		Logger.error('%s shutdown !'%self.address)
		self.switch = False
		self.sock.shutdown( SHUT_RDWR )
		self.sock.close()
		del Service.server[ self.address ]

	def receive(self):
		try:
			sourceStream = ''
			while self.switch:
				Logger.debug( '%s receiving...' % self.address )
				recvStream = self.sock.recv( 1000 )
				Logger.debug( 'receive raw stream from %s : ' % self.address, recvStream )
				if recvStream:
					self.isAlive = True
					sourceStream = self.parseHeader( '%s%s' % ( sourceStream, recvStream ) )
				elif self.switch == True:
					Logger.info( '%s disconnect...' % self.address )
					self.shutdown()
		except:
			Logger.error( 'receive error : %s' % format_exc() )
			Logger.error('%s receive error : %s'%( self.address, 
											    format_exc() ) )
			self.shutdown()

	def parseHeader(self, stream):
		if len(stream) >= self.headerSize:
			head = unpack(self.headerStruct, stream[ : self.headerSize])
			if head[1] != self.magicCode:
				Logger.error('receive invalid package from %s : '%self.address, stream)
				self.shutdown()
			if head[0] + 2 <= len(stream):
				mStream = stream[self.headerSize : head[0] + 2]
				stream = stream[head[0] + 2 : ]
				if head[2] != self.heartCode:
					self.commCondition.acquire()
					self.packQueue.insert(0, [head[3], head[2], mStream])
					self.commCondition.notify()
					self.commCondition.release()
				stream = self.parseHeader(stream)
		return stream

	def chkHeart(self):
		while self.isAlive and self.switch:
			self.isAlive = False
			sleep( self.timeout )
		if self.switch:
			Logger.error('%s heart time out !'%self.address)
			self.shutdown()
			
	def send(self, stream):
		Logger.debug( '%s send raw stream : ' % self.address, stream )
		self.sock.sendall( stream )
	
	@staticmethod
	def broadcast(data, destAddr=''):
		if destAddr:
			Service.server[ destAddr ].commCondition.acquire()
			Service.server[ destAddr ].packQueue.insert( 0, data )
			Service.server[ destAddr ].commCondition.notify()
		else:
			for srv in Service.server.values():
				srv.commCondition.acquire()
				srv.packQueue.insert( 0, data )
				srv.commCondition.notify()
		
	def main(self, data):
		pass