'''
Created on 2012-8-23

@author: XPMUser
'''

from time import time
import socket
from os import getpid

from lib.TerminalManager import icmp
from lib import Tools

class _TerminalManager(object):
	'''
	classdocs
	'''
	__me = None

	def __init__(self, db):
		'''
		Constructor
		'''
		self.__db = None
		self.__table = 'terminal'

		self.__status = {}
		self.__gapTime = 5
		
		self.__switch = True
	
	@staticmethod
	def instance(db):
		if _TerminalManager.__me == None:
			_TerminalManager.__me = _TerminalManager()
			_TerminalManager.__me.setDB( db )
		else:
			return _TerminalManager.__me
		pass
	
	def setDB(self, db):
		self.__db = db
		
	def supervisor(self):
		icmpProtocol = socket.getprotobyname("icmp")
		my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmpProtocol)
		my_ID = getpid() & 0xFFFF
		
		for terminal in self.findAllTerminal():
			self.__status[ terminal[ 'IPv4' ] ] = False
		
		ip = Tools.getIP()
		netmark = Tools.getNermark()
		
		ipBit = socket.inet_aton( ip )
		netmarkBit = socket.inet_aton( netmark )
		netAddrBit = ipBit & netmarkBit
		
		ipCount = netmarkBit ^ 0xffffffff
		
		for i in range( 1, ipCount ):
			dest_addr = socket.inet_ntoa( netAddrBit + i )
			icmp.send_one_ping(my_socket, dest_addr, my_ID)
			delay = icmp.receive_one_ping(my_socket, my_ID, 2)
			
		my_socket.close()
		pass
	
	def stop(self):
		self.__switch = False
		
	def setTerminal(self, ip, mac):
		self.removeTerminal( ip, mac )
		terminalInfo = { 'IPv4': ip, 'Mac': mac, 'Type': 1 }
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
		
from sys import modules
from lib.DB import Database
modules[__name__] = _TerminalManager.instance( Database )