#coding=UTF-8
'''
Created on 2012-8-14

@author: Moxiaoyong
'''

from struct import unpack

import threading

from lib.Service import Service
from lib.Securer import MyRsa, MyDes, MyKey

class OuterService(Service):
	'''
	classdocs
	'''

	def __init__(self, socket, address):
		super( OuterService, self ).__init__( socket, address )
		self.sendPubKey()

	def sendPubKey(self):
		self.__ras = MyRsa.MyRsa()
		self.__ras.generate()
		pubKey = self.__ras.getPubKey()
		pubKeyPackage = self.__packager.genPackage( 'PubKey', 0, pubKey )
		super( OuterService, self ).send( pubKeyPackage )

	def running(self):
		super( OuterService, self ).running()
		self.__chkThread = threading.Thread(target=self.chkResponse)
		self.__recvThread.start()
		self.__mainThread.start()
		self.__chkThread.start()
		
	def main(self):
		if self.__threadingCondition.acquire():
			while self.__switch:
				if len( self.__queue ) == 0:
					self.__threadingCondition.wait()
				( pid, code, package ) = self.__queue.pop()
				
				#发送回应包
				respPackage = self.__packager.genPackage( 'Response', pid )
				self.send( respPackage )
				
				#解析包
				data = self.__packager.parsePackage( code, package )
				packageInfo = self.__packager.codeFindPackage( code )
				
				func = getattr( self, packageInfo['Name'] )
				unitNum = str.split( ',', packageInfo['StructLabel'] ).__len__()
				data = [data[i : i + unitNum] for i in range( 0, len( data ), unitNum )]
				func( data )
	
	def Key(self, data):
		data = self.__ras.privateDecrypt( data[ 0 ] )
		self.__ras = None
		( desKey, myKey ) = unpack( '<QL', data )
		self.__myKey = MyKey.MyKey()
		if not self.__myKey.check( myKey ):
			self.shutdown()
		self.__myDes = MyDes.MyDes()
		self.__myDes.setKey( desKey )
	
	def WOL(self, data):
		from socket import socket, AF_INET, SOCK_DGRAM
		from binascii import a2b_hex
		from lib import TerminalManager
		from re import sub
		udp = socket( AF_INET, SOCK_DGRAM )
		for groupData in data:
			terminalInfo = TerminalManager.idFindTerminal( groupData[0] )
			package = a2b_hex( 'f' * 12 + sub( '-', '', terminalInfo['Mac'] ) * 16 )
			udp.sendto( package, ( '255.255.255.255', 6666 ) )
			
	def send(self, stream):
		ciphertext = self.__myDes.encrypt( stream )
		super( OuterService, self ).send( ciphertext )
