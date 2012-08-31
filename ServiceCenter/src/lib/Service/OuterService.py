#coding=UTF-8
'''
Created on 2012-8-14

@author: Moxiaoyong
'''
import threading

from struct import unpack
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM
from binascii import a2b_hex
from re import sub

from Service import Service

from lib.Global import Logger, TerminalManager
from lib.Config import BROADCASTADDR
from lib.Securer import MyRsa, MyDes, MyKey

class OuterService(Service):
	'''
	外部服务器，面向Internet的手机控制端
	'''
	
	def __init__(self, socket, address):
		super( OuterService, self ).__init__( socket, address )
		
		self.respWaitCount = 0
		self.respSurplusTime = 0
		
		self.chkCondition = None
		
		self.sendPubKey()

	def sendPubKey(self):
		self.rsa = MyRsa.MyRsa()
		self.rsa.generate()
		pubKey = self.rsa.getPubKey()
		
		self.packager.setEncipherer( 'rsa_public', self.rsa.publicCrypt )
		self.packager.setEncipherer( 'rsa_private', self.rsa.privateCrypt )
		
		pubKeyPackage = self.packager.genPackage( 'PubKey', self.pid, pubKey )
		super( OuterService, self ).send( 'PubKey', pubKeyPackage )

	def running(self):
		super( OuterService, self ).running()
		
		self.chkCondition = threading.Condition()
		
		self.chkThread = threading.Thread( target = self.chkResponse )
		self.recvThread.start()
		self.mainThread.start()
		self.chkThread.start()
		
	def chkResponse(self):
		if self.chkCondition.acquire():
			while self.switch:
				while self.respSurplusTime>0 and self.switch:
					sleep( self.timeout )
					self.respSurplusTime -= self.timeout
				if self.respWaitCount > 0:
					Logger.error('%s response time out !'%self.address)
					self.shutdown()
				else:
					self.chkCondition.wait()	

	def send(self, packName, package):
		super( OuterService, self ).send( package )
		
		if self.packager.existsReply( packName ):
			self.pid += 1
			self.respSurplusTime += self.timeout
			self.respWaitCount += 1
			self.chkCondition.notify()

	def main(self):
		if self.commCondition.acquire():
			while self.switch:
				if len( self.packQueue ) <= 0:
					self.commCondition.wait()
				( pid, code, package ) = self.packQueue.pop()
				Logger.info('received head from %s : [%d, %2x]' % ( self.address, 
																	pid,
																	code ) )
				Logger.debug('received package from %s : '%self.address, package)
				
				
				#解析包
				data = self.packager.parsePackage( code, package )
				packInfo = self.packager.codeFindPackage( code )
				
				#发送回应包
				if packInfo['CanReplay'] == 1:
					respPackage = self.packager.genPackage( 'Response', pid )
					self.send( 'Response', respPackage )

				func = getattr( self, packInfo['Name'] )
				unitNum = str.split( ',', packInfo['StructLabel'] ).__len__()
				data = [data[i : i + unitNum] for i in range( 0, len( data ), unitNum )]
				func( data )

	def Response(self, data):
		self.respWaitCount -= 1

	def Key(self, data):
		( desKey, myKey ) = unpack( '<QL', data )
		self.myKey = MyKey.MyKey()
		if not self.myKey.check( myKey ):
			self.shutdown()
		
		TerminalManager.running()
		
		self.myDes = MyDes.MyDes()
		self.myDes.setKey( desKey )
		self.packager.setEncipherer( 'des', self.myDes.crypt )
		
		terminalList = TerminalManager.findAllTerminal()
		terminalNames = [ [theTerminal['Name'] for theTerminal in terminalList].join( ',' ) ]
		terminalInfoPackage = self.package.genPackage( 'TerminalInfo', self.pid, terminalNames )
		self.send( 'TerminalInfo', terminalInfoPackage )
		
		queryPackInfo = self.packager.nameFindPackage( 'QueryStatus' )
		self.packQueue.append( [ self.pid, queryPackInfo[ 'Code' ], '' ] )
	
	def WOL(self, data):
		udp = socket( AF_INET, SOCK_DGRAM )
		for groupData in data:
			terminalInfo = TerminalManager.idFindTerminal( groupData[0] )
			package = a2b_hex( 'f' * 12 + sub( '-', '', terminalInfo['Mac'] ) * 16 )
			udp.sendto( package, ( BROADCASTADDR, 6666 ) )
	
	def QueryStatus(self, data):
		terminalStatus = TerminalManager.getStatus()
		terminalStatusPackage = self.package.genPackage( 'TerminalStatus', self.pid, terminalStatus )
		self.send( 'TerminalInfo', terminalStatusPackage )
		