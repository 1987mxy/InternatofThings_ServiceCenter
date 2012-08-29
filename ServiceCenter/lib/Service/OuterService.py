#coding=UTF-8
'''
Created on 2012-8-14

@author: Moxiaoyong
'''

from struct import unpack
from time import sleep

import threading

from lib.Log import LOG
from lib import TerminalManager
from lib.Service import Service
from lib.Securer import MyRsa, MyDes, MyKey

class OuterService(Service):
	'''
	classdocs
	'''

	def __init__(self, socket, address):
		super( OuterService, self ).__init__( socket, address )
		
		self.__terminalManager = TerminalManager
		self.__respWaitCount = 0
		self.__respSurplusTime = 0
		
		self.__chkCondition = None
		
		self.sendPubKey()

	def sendPubKey(self):
		self.__rsa = MyRsa.MyRsa()
		self.__rsa.generate()
		pubKey = self.__rsa.getPubKey()
		
		self.__packager.setEncipherer( 'rsa_public', self.__rsa.publicCrypt )
		self.__packager.setEncipherer( 'rsa_private', self.__rsa.privateCrypt )
		
		pubKeyPackage = self.__packager.genPackage( 'PubKey', self.__pid, pubKey )
		super( OuterService, self ).send( 'PubKey', pubKeyPackage )

	def running(self):
		super( OuterService, self ).running()
		
		self.__chkCondition = threading.Condition()
		
		self.__chkThread = threading.Thread( target = self.chkResponse )
		self.__recvThread.start()
		self.__mainThread.start()
		self.__chkThread.start()
		
	def chkResponse(self):
		if self.__chkCondition.acquire():
			while self.__switch:
				while self.__respSurplusTime>0 and self.__switch:
					sleep( self.__timeout )
					self.__respSurplusTime -= self.__timeout
				if self.__respWaitCount > 0:
					LOG.error('%s response time out !'%self.__address)
					self.shutdown()
				else:
					self.__chkCondition.wait()	

	def send(self, packName, package):
		super( OuterService, self ).send( package )
		
		if self.__packager.existsReply( packName ):
			self.__pid += 1
			self.__respSurplusTime += self.__timeout
			self.__respWaitCount += 1
			self.__chkCondition.notify()

	def main(self):
		if self.__commCondition.acquire():
			while self.__switch:
				if len( self.__packQueue ) <= 0:
					self.__commCondition.wait()
				( pid, code, package ) = self.__packQueue.pop()
				LOG.info('received head from %s : [%d, %2x]' % ( self.__address, 
																	pid,
																	code ) )
				LOG.debug('received package from %s : '%self.__address, package)
				
				
				#解析包
				data = self.__packager.parsePackage( code, package )
				packageInfo = self.__packager.codeFindPackage( code )
				
				#发送回应包
				if packageInfo['CanReplay'] == 1:
					respPackage = self.__packager.genPackage( 'Response', pid )
					self.send( 'Response', respPackage )

				func = getattr( self, packageInfo['Name'] )
				unitNum = str.split( ',', packageInfo['StructLabel'] ).__len__()
				data = [data[i : i + unitNum] for i in range( 0, len( data ), unitNum )]
				func( data )

	def Key(self, data):
		( desKey, myKey ) = unpack( '<QL', data )
		self.__myKey = MyKey.MyKey()
		if not self.__myKey.check( myKey ):
			self.shutdown()
		
		self.__myDes = MyDes.MyDes()
		self.__myDes.setKey( desKey )
		self.__packager.setEncipherer( 'des', self.__myDes.crypt )
		
		terminalList = self.__terminalManager.findAllTerminal()
		terminalNames = [theTerminal['Name'] for theTerminal in terminalList].join( ',' )
		
		terminalInfoPackage = self.__package.genPackage( 'TerminalInfo', self.__pid, terminalNames )
		self.send( 'TerminalInfo', terminalInfoPackage )
	
	def WOL(self, data):
		from socket import socket, AF_INET, SOCK_DGRAM
		from binascii import a2b_hex
		from re import sub
		udp = socket( AF_INET, SOCK_DGRAM )
		for groupData in data:
			terminalInfo = self.__terminalManager.idFindTerminal( groupData[0] )
			package = a2b_hex( 'f' * 12 + sub( '-', '', terminalInfo['Mac'] ) * 16 )
			udp.sendto( package, ( '255.255.255.255', 6666 ) )
	
	def Response(self, data):
		self.__respWaitCount -= 1
