#coding=UTF-8

'''
Created on 2012-9-1

@author: XPMUser
'''

import socket, threading
from struct import unpack, calcsize

from lib.Securer.MyRsa import MyRsa
from lib.Securer.MyAes import MyAes
from lib.Config import srvCenterConf
from lib.Global import Packager, Logger, DB

class srv(object):
	def __init__(self,sock):
		self.sock = sock
		self.switch = True
		
		self.tStatus = []
		
		self.tname = None

	def config(self, config):
		self.magicCode = config.magicCode
		self.heartCode = config.heartCode
		self.headerStruct = config.headerStruct
		self.headerSize = calcsize( self.headerStruct )
		self.timeout = config.timeout
	
	def running(self):
		t = threading.Thread(target=self.recv)
		self.tname = t.getName()
		t.start()
		self.o = threading.Thread(target=self.open)
	
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
		packInfo = Packager.codeFindPackage( code )
		data = Packager.parsePackage( self.tname, code, packbody )

		#发送回应包
		if packInfo['ExistReply'] == 1:
			respPackage = Packager.genPackage( self.tname, 'Response', pid )
			self.send( respPackage )

		func = getattr(self, packInfo['Name'])
		func( data )
	
	def send(self, data):
		Logger.debug( 'send raw stream:', data )
		self.sock.sendall( data )
		
	def PubKey(self, data):
		data = data[0]
		myRsa = MyRsa()
		myRsa.setPubKey( data )
		Packager.setEncipherer( self.tname, 'rsa_public', myRsa.publicCrypt )
		
		myAes = MyAes()
		myAes.generate()
		aes = myAes.getKey()
		Packager.setEncipherer( self.tname, 'des', myAes.crypt )
		key = int( raw_input( 'Please input your Secret Key: ' ) )
		keyPackage = Packager.genPackage( self.tname, 'Key', 2, [key, aes])
		self.send( keyPackage )
		
	def Response(self, data):
		Logger.debug( 'receive response!' )
		
	def TerminalInfo(self, data):
		data = data[0]
		terminalNames = data.split( ',' )
		self.tStatus = []
		print 'Terminal'+'='*30
		for terminal in terminalNames:
			self.tStatus.append([terminal,0])
			Logger.info('terminal: %s'%terminal)
			
	def TerminalStatus(self, data):
		data = list(data)
		print 'Terminal Status'+'='*23
		for t in self.tStatus:
			status = data.pop(0)
			print '%s:%s'%( t[0], (status==1 and 'online') or 'offline' )
			t[1]=status
			
		if not self.o.isAlive():
			self.o.start()
		
	def open(self):
		print '='*38
		while self.switch:
			name = raw_input( 'which terminal: ' )
			for i in range( len( self.tStatus ) ):
				if self.tStatus[i][0] == name:
					if self.tStatus[i][1] == 0:
						wolPackager = Packager.genPackage( self.tname, 'WOL', 3, [ i ] )
						self.send( wolPackager )
						Logger.info( 'open %s!'%self.tStatus[i][0] )
					else:
						Logger.info( '%s is online!'%self.tStatus[i][0] )
					break;

if __name__ == '__main__':
	mobileSock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	mobileSock.connect( ( '172.16.0.101', 8782 ) )
#	mobileSock.connect( ( '172.16.27.192', 8782 ) )
	
	s = srv( mobileSock )
	s.config( srvCenterConf )
	s.running()