#coding=UTF-8
'''
Created on 2012-8-23

@author: XPMUser
'''
import socket
import threading

from time import time
from os import getpid
from struct import pack, unpack

import ICMP
from lib.Global import Packager, DB, TerminalManager
from lib.Config import NETMARK, NETWORKADDR

class TerminalManage(object):
	'''
	终端管理者(单例模式)，管理所有终端
	'''
	__me = None

	def __init__(self):
		'''
		Constructor
		'''
		self.__db = None
		self.__table = 'terminal'

		self.__status = {}
		self.__gapTime = 5
		
		self.__switch = True
		self.__viewerThread = None
		
		self.setDB( DB )
	
	@staticmethod
	def instance():
		if TerminalManage.__me == None:
			TerminalManage.__me = TerminalManage()
		return TerminalManage.__me
	
	def setDB(self, db):
		self.__db = db
		
	def viewer(self):
		icmpProtocol = socket.getprotobyname("icmp")
		mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmpProtocol)
		my_ID = getpid() & 0xFFFF
		
		for terminal in self.findAllTerminal():
			self.__status[ terminal[ 'IPv4' ] ] = False
		
		netmarkBit = unpack( 'L', socket.inet_aton( NETMARK ) )[0]
		
		netAddrBit = unpack( 'L', socket.inet_aton( NETWORKADDR ) )[0]
		
		ipCount = netmarkBit ^ 0xFFFFFFFF
		
		def changeStatus( delay, destAddr ):
			if delay:
				if destAddr in self.__status.keys():
					if self.__status[ destAddr ] == False:
						self.activateTerminal( destAddr )
				else:
					host = socket.gethostbyaddr( destAddr )[0]
					self.setTerminal( ip=destAddr, name=host )
				self.__status[ destAddr ] = True
			else:
				if destAddr in self.__status.keys():
					self.__status[ destAddr ] = False
		
		while self.__switch:
			for existsAddr in self.__status.keys():
				ICMP.send_one_ping(mySocket, existsAddr, my_ID)
				delay = ICMP.receive_one_ping(mySocket, my_ID, 2)
				changeStatus( delay, existsAddr )
			
			for i in range( 1, ipCount ):
				destAddr = socket.inet_ntoa( pack( 'L', netAddrBit + i ) )
				if destAddr in self.__status.keys():
					continue
				ICMP.send_one_ping(mySocket, destAddr, my_ID)
				delay = ICMP.receive_one_ping(mySocket, my_ID, 2)
				changeStatus( delay, destAddr )
				
			queryPackInfo = Packager.nameFindPackage( 'QueryStatus' )
			OuterService.broadcast( [ 0, queryPackInfo[ 'Code' ], '' ] )
			time.sleep( 30 )

		mySocket.close()
	
	def running(self):
		self.__viewerThread = threading.Thread( target = self.viewer )
		self.__viewerThread.start()
	
	def stop(self):
		self.__switch = False
		
	def setTerminal(self, ip, mac='', name=''):
		self.removeTerminal( ip, mac )
		terminalInfo = {}
		terminalInfo[ 'Name' ] = name
		terminalInfo[ 'IPv4' ] = ip
		terminalInfo[ 'Mac' ] = mac
		terminalInfo[ 'Type' ] = 1
		return self.__db.insert( self.__table, terminalInfo )
		
	def removeTerminal(self, ip='', mac=''):
		where = ''
		if ip:
			where = 'IPv4="%s" '%ip
		if mac:
			where = ( where and 'OR Mac="%s"'%mac ) or 'Mac="%s"'%mac
		return self.__db.delete( self.__table, where )

	def existsTerminal(self, ip, mac):
		where = 'IPv4="%s" AND Mac="%s"'%( ip, mac )
		count = self.__db.count( self.__table, where )
		return count > 0

	def findAllTerminal(self):
		return self.__db.select( self.__table )
	
	def nameFindTerminal(self, name):
		where = 'Name="%s"'%name
		return self.__db.selectOne( self.__table, where )

	def idFindTerminal(self, terminalID):
		where = 'TerminalID=%s'%terminalID
		return self.__db.selectOne( self.__table, where )
	
	def activateTerminal(self, ip):
		now = int( time() )
		terminalInfo = { 'LastActive': now }
		where = 'IPv4="%s"'
		self.__db.update( self.__table, terminalInfo, where )
		
	def getStatus(self, index):
		if index:
			return self.__status.values()
		else:
			return self.__status.values()[ index ]
		
TerminalManager = TerminalManage.instance()