#coding=UTF-8
'''
Created on 2012-8-23

@author: XPMUser
'''
import socket
import threading
from time import time, sleep
from os import getpid
from struct import pack, unpack

import ICMP
from lib.Global import Packager, DB, Logger
from lib.Service.OuterService import OuterService
from lib.Tools import getMac
from lib.Config import IP, NETMARK, NETWORKADDR

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
		self.__fieldList = [ 'TerminalID', 'Name', 'IPv4', 'Mac' ]

		self.__status = {}
		self.__gapTime = 5
		
		self.__switch = True
		self.__viewerThread = None
		
		self.setDB( DB )

		for terminal in self.findAllTerminal():
			terminal[ 'Status' ] = False
			self.__status[ terminal[ 'IPv4' ] ] = terminal
	
	@staticmethod
	def instance():
		if TerminalManage.__me == None:
			TerminalManage.__me = TerminalManage()
		return TerminalManage.__me
	
	def setDB(self, db):
		self.__db = db
		
	def running(self):
		self.__viewerThread = threading.Thread( target = self.viewer )
		self.__viewerThread.start()
		
	def stop(self):
		self.__switch = False
		
	def viewer(self):
		icmpProtocol = socket.getprotobyname("icmp")
		mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmpProtocol)
		my_ID = getpid() & 0xFFFF
		
		netmarkBit = unpack( '>L', socket.inet_aton( NETMARK ) )[0]
		
		netAddrBit = unpack( '>L', socket.inet_aton( NETWORKADDR ) )[0]
		
		ipCount = netmarkBit ^ 0xFFFFFFFF
		
		def changeStatus( delay, destAddr ):
			if delay:
				Logger.info( 'Find Terminal %s!'%destAddr )
				if self.__status.has_key( destAddr ):
					if self.__status[ destAddr ][ 'Status' ] == False:
						self.activateTerminal( destAddr )
				else:
					try:
						host = socket.gethostbyaddr( destAddr )[0]
					except socket.herror, e:
						if e.errno != 11004:
							raise Exception( 'get host name error!' )
						host = destAddr
					mac = getMac( destAddr )
					self.setTerminal( destAddr, mac, host )
					self.__status[ destAddr ] = {'Name':host, 'IPv4':destAddr, 'Mac':mac, 'Type':1 }
				self.__status[ destAddr ][ 'Status' ] = True
			else:
				if self.__status.has_key( destAddr ):
					self.__status[ destAddr ][ 'Status' ] = False
		
		while self.__switch:
			for existsAddr in self.__status.keys():
				
				ICMP.send_one_ping(mySocket, existsAddr, my_ID)
				delay = ICMP.receive_one_ping(mySocket, my_ID, 2)
				changeStatus( delay, existsAddr )
			
			for i in range( 1, ipCount ):
				destAddr = socket.inet_ntoa( pack( '>L', netAddrBit + i ) )
				if destAddr == IP or self.__status.has_key( destAddr ):
					continue
				ICMP.send_one_ping(mySocket, destAddr, my_ID)
				delay = ICMP.receive_one_ping(mySocket, my_ID, 2)
				changeStatus( delay, destAddr )
				
			queryPackInfo = Packager.nameFindPackage( 'QueryStatus' )
			OuterService.broadcast( [ 0, queryPackInfo[ 'Code' ], '' ] )
			sleep( 30 )

		mySocket.close()
		
	def setTerminal(self, ip, mac='', name=''):
		self.removeTerminal( ip, mac )
		terminalInfo = {}
		terminalInfo[ 'Name' ] = name
		terminalInfo[ 'IPv4' ] = ip
		terminalInfo[ 'Mac' ] = mac
		terminalInfo[ 'Type' ] = '1'
		return self.__db.io( 'insert', [ self.__table, terminalInfo ] )
		
	def removeTerminal(self, ip='', mac=''):
		where = ''
		if ip:
			where = 'IPv4="%s"'%ip
		if mac:
			where = ( where and '%s OR Mac="%s"'%( where, mac ) ) or 'Mac="%s"'%mac
		return self.__db.io( 'delete', [ self.__table, where ] )

	def existsTerminal(self, ip, mac):
		if self.__status:
			count = [ terminal for terminal in self.__status.values() if terminal['IPv4'] == ip and terminal['Mac'] == mac ].__len__()
		else:
			where = 'IPv4="%s" AND Mac="%s"'%( ip, mac )
			count = self.__db.io( 'count', [ self.__table, where ] )
		return count > 0

	def findAllTerminal(self):
		if self.__status:
			return self.__status.values()
		else:
			terminalList = []
			return self.__db.io( 'select', [ self.__table, ','.join( self.__fieldList ) ] )
	
	def nameFindTerminal(self, name):
		if self.__status:
			return [ terminal for terminal in self.__status.values() if terminal['Name'] == name ]
		else:
			where = 'Name="%s"'%name
			return self.__db.io( 'selectOne', [ self.__table, ','.join( self.__fieldList ), where ] )

	def idFindTerminal(self, terminalID):
		if self.__status:
			return [ terminal for terminal in self.__status.values() if terminal['TerminalID'] == terminalID ]
		else:
			where = 'TerminalID=%s'%terminalID
			return self.__db.io( 'selectOne', [ self.__table, ','.join( self.__fieldList ), where ] )
	
	def activateTerminal(self, ip):
		now = int( time() )
		terminalInfo = { 'LastActive': now }
		where = 'IPv4="%s"'
		self.__db.io( 'update', [ self.__table, terminalInfo, where ] )
		
	def getStatus(self, index=None):
		if index == None:
			return [ terminal['Status'] for terminal in self.__status.values() ]
		else:
			return self.__status.values()[ index ][ 'Status' ]