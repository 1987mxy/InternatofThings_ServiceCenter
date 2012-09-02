#coding=UTF-8
'''
Created on 2012-8-14

@author: Moxiaoyong
'''
import threading

from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM
from binascii import a2b_hex
from re import sub

from Service import Service

from lib.Global import Logger
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

	def sendPubKey(self):
		self.rsa = MyRsa.MyRsa()
		self.rsa.generate()
		pubKey = self.rsa.getPubKey()
		
		self.packager.setEncipherer( self.mainThreadName, 'rsa_public', self.rsa.publicCrypt )
		self.packager.setEncipherer( self.mainThreadName, 'rsa_private', self.rsa.privateCrypt )
		
		pubKeyPackage = self.packager.genPackage( self.mainThreadName, 'PubKey', self.pid, [ pubKey ] )
		self.send( 'PubKey', pubKeyPackage )

	def running(self):
		super( OuterService, self ).running()
		
		self.chkCondition = threading.Condition()
		
		self.chkThread = threading.Thread( target = self.chkResponse )
		self.recvThread.start()
		self.mainThread.start()
		self.chkThread.start()
		
		self.sendPubKey()
		
	def chkResponse(self):
		self.chkCondition.acquire()
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
			self.chkCondition.acquire()
			self.pid += 1
			self.respSurplusTime += self.timeout
			self.respWaitCount += 1
			self.chkCondition.notify()
			self.chkCondition.release()

	def main(self):
		self.commCondition.acquire()
		while self.switch:
			if len( self.packQueue ) <= 0:
				self.commCondition.wait()
			( pid, code, package ) = self.packQueue.pop()
			Logger.info('received head from %s : [%d, %2x]' % ( self.address, 
																pid,
																code ) )
			Logger.debug('received package from %s : '%self.address, package)
			
			
			#解析包
			data = self.packager.parsePackage( self.mainThreadName, code, package )
			packInfo = self.packager.codeFindPackage( code )
			
			#发送回应包
			if packInfo['ExistReply'] == 1:
				respPackage = self.packager.genPackage( self.mainThreadName, 'Response', pid )
				self.send( 'Response', respPackage )

			func = getattr( self, packInfo['Name'] )
			unitNum = packInfo['StructLabel'].split( ',' ).__len__()
			data = [data[i : i + unitNum] for i in range( 0, len( data ), unitNum )]
			func( data )

	def Response(self, data):
		self.respWaitCount -= 1

	def Key(self, data):
		data=data[0]
		print 'key:%d'%data[0]
		self.myKey = MyKey.MyKey()
		if not self.myKey.check( data[0] ) and self.switch == True:
			self.shutdown()
		
		print 'deskey:%s'%data[1].__repr__()
		self.myDes = MyDes.MyDes()
		self.myDes.setKey( data[1] )
		self.packager.setEncipherer( self.mainThreadName, 'des', self.myDes.crypt )
		
		terminalList = self.terminalManager.findAllTerminal()
		terminalNames = [ ','.join( [theTerminal['Name'] for theTerminal in terminalList] ) ]
		terminalInfoPackage = self.packager.genPackage( self.mainThreadName, 'TerminalInfo', self.pid, terminalNames )
		self.send( 'TerminalInfo', terminalInfoPackage )
		
		queryPackInfo = self.packager.nameFindPackage( 'QueryStatus' )
		self.commCondition.acquire()
		self.packQueue.insert( 0, [ self.pid, queryPackInfo[ 'Code' ], '' ] )
		self.commCondition.notify()
		self.commCondition.release()
	
	def WOL(self, data):
		udp = socket( AF_INET, SOCK_DGRAM )
		for groupData in data:
			terminalInfo = self.terminalManager.idFindTerminal( groupData[0] )
			package = a2b_hex( 'f' * 12 + sub( '-', '', terminalInfo['Mac'] ) * 16 )
			udp.sendto( package, ( BROADCASTADDR, 6666 ) )
	
	def QueryStatus(self, data):
		terminalStatus = self.terminalManager.getStatus()
		terminalStatusPackage = self.packager.genPackage( self.mainThreadName, 'TerminalStatus', self.pid, terminalStatus )
		self.send( 'TerminalInfo', terminalStatusPackage )
		