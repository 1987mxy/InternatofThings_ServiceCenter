'''
Created on 2012-8-23

@author: XPMUser
'''

import time

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
		now = int( time.time() )
		terminalInfo = { 'LastActive': now }
		where = 'IPv4="%s"'
		self.__db.update( self.__table, terminalInfo, where )
		
from sys import modules
from lib.DB import Database
modules[__name__] = _TerminalManager.instance( Database )