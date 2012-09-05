#coding=UTF-8

'''
Created on 2012-9-1

@author: XPMUser
'''

import socket, threading
from struct import unpack, pack, calcsize

from lib.Securer.MyRsa import MyRsa
from lib.Securer.MyDes import MyDes
from lib.Securer.MyKey import MyKey
from lib.Config import srvCenterConf
from lib.Global import Packager, Logger, DB

class srv(object):
	def __init__(self,sock):
		self.sock = sock
		self.switch = True
		
		self.tStatus = []

	def config(self, config):
		self.magicCode = config.magicCode
		self.heartCode = config.heartCode
		self.headerStruct = config.headerStruct
		self.headerSize = calcsize( self.headerStruct )
		self.timeout = config.timeout
	
	def running(self):
		t = threading.Thread(target=self.recv)
		t.start()
	
	def recv(self):
		sourceStream = ''
		while self.switch:
			recvStream = self.sock.recv( 1000 )
			Logger.debug( 'receive raw stream from Server : ', recvStream )
			if recvStream:
				sourceStream = self.parseHeader( '%s%s' % ( sourceStream, recvStream ) )
			else:
				Logger.error( 'disconnect!' )
				DB.stop()
				self.sock.shutdown( socket.SHUT_RDWR )
				self.sock.close()
				self.switch = False

	def parseHeader(self, stream):
		if len(stream) >= self.headerSize:
			head = unpack(self.headerStruct, stream[ : self.headerSize])
			if head[1] != self.magicCode:
				Logger.error('receive invalid package from Server : ', stream)
				self.shutdown()
			if head[0] + 2 <= len(stream):
				mStream = stream[self.headerSize : head[0] + 2]
				stream = stream[head[0] + 2 : ]
				if head[2] != self.heartCode:
					self.packQueue( head[3], head[2], mStream )
				stream = self.parseHeader(stream)
		return stream
	
	def packQueue(self, pid, code, packbody):
		tname = threading.currentThread().getName()
		packInfo = Packager.codeFindPackage( code )
		data = Packager.parsePackage( tname, code, packbody )

		#发送回应包
		if packInfo['ExistReply'] == 1:
			respPackage = Packager.genPackage( tname, 'Response', pid )
			self.send( respPackage )

		func = getattr(self, packInfo['Name'])
		func( data )
	
	def send(self, data):
		Logger.debug( 'send raw stream:', data )
		self.sock.sendall( data )
		
	def PubKey(self, data):
		tname = threading.currentThread().getName()
		myRsa = MyRsa()
		print myRsa.setPubKey( data[0] )
		Packager.setEncipherer( tname, 'rsa_public', myRsa.publicCrypt )
		
		myDes = MyDes()
		des = myDes.getKey()
		print 'des:%s'%des.__repr__()
		Packager.setEncipherer( tname, 'des', myDes.crypt )
		myKey = MyKey()
		key = myKey.getKey()
		print 'key:%d'%key
		keyPackage = Packager.genPackage( tname, 'Key', 2, [key, des])
		self.send( keyPackage )
		
	def Response(self, data):
		Logger.info( 'receive response!' )
		
	def TerminalInfo(self, data):
		data = data[0]
		terminalNames = data.split( ',' )
		self.tStatus = []
		for terminal in terminalNames:
			self.tStatus.append([terminal,0])
			Logger.info('terminal: %s'%terminal)
			
	def TerminalStatus(self, data):
		data = list(data)
		for t in self.tStatus:
			t[1]=data.pop(0)
		print dict(self.tStatus)
		

if __name__ == '__main__':
	mobileSock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
#	mobileSock.connect( ( '172.16.0.101', 8782 ) )
	mobileSock.connect( ( '172.16.27.192', 8782 ) )
	
	s = srv( mobileSock )
	s.config( srvCenterConf )
	s.running()