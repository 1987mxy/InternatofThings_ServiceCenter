#coding=UTF-8
'''
Created on 2012-8-14

@author: Moxiaoyong
'''

from lib.Service import Service

import threading

class OuterService(Service):
	'''
	classdocs
	'''

	def sendPubKey(self):
		
		pass

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
	
	
	
	def WOL(self, data):
		import socket
		from binascii import a2b_hex
		from lib import TerminalManager
		from re import sub
		udp = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		for groupData in data:
			terminalInfo = TerminalManager.idFindTerminal( groupData[0] )
			package = a2b_hex( 'f' * 12 + sub( '-', '', terminalInfo['Mac'] ) * 16 )
			udp.sendto( package, ( '255.255.255.255', 6666 ) )
