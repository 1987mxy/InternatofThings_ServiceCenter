#coding=UTF-8
'''
Created on 2012-8-19

@author: XPMUser
'''

class Database(object):
	'''
	数据库类，用来操作“数据包表”和“终端表”
	'''

	def __init__(self):
		import sqlite3
		import os.path
		if os.path.isfile( 'Data.dat' ):
			self.__db = sqlite3.connect('Data.dat')
		else:
			self.__db = sqlite3.connect('Data.dat')
			self.__install()
		
	def __install(self):
		sql_file = open( 'install.sql', 'rb' )
		sql = sql_file.read()
		sql_file.close()
		self.__db.executescript( sql )
		
	def backup(self):
		self.delete( 'terminal' )
		sql_file = open( 'install.sql', 'wb' )
		for sql_line in self.__db.iterdump():
			sql_file.write( sql_line )
		sql_file.close()
		
	def insert(self, table, data):
		columnList = []
		for field, value in data:
			columnList.append( '%s="%s"' % ( field, value ) )
		self.__db.execute( 'INSERT INTO %s SET %s' % ( table, str.join( ', ', columnList ) ) )
	
	def delete(self, table, where=''):
		where = ( where and 'WHERE %s' % where ) or ''
		self.__db.execute( 'DELETE FROM %s %s'%( table, where ) )
	
	def update(self, table, data, where=''):
		columnList = []
		for field, value in data:
			columnList.append( '%s="%s"' % ( field, value ) )
		where = ( where and 'WHERE %s' % where ) or ''
		self.__db.execute( 'UPDATE %s SET %s %s' % ( table, str.join( ', ', columnList ), where ) )
	
	def select(self, table, where=''):
		where = ( where and 'WHERE %s'%where ) or ''
		cur = self.__db.execute( 'SELECT * FROM %s %s'%(table, where) )
		return cur.fetchall()
	
	def count(self, table, where=''):
		where = ( where and 'WHERE %s'%where ) or ''
		cur = self.__db.execute( 'SELECT COUNT(*) AS `count` FROM %s %s'%(table, where) )
		return cur.fetchone()[ 'count' ]
	
	def query(self, sql):
		cur = self.__db.execute( sql )
		return cur
	
################################################
		
	def setTerminal(self, ip, mac):
		self.removeTerminal( ip, mac )
		self.__db.execute( 'INSERT INTO terminal( IPv4, Mac, Type, IsActive ) VALUES( "%s", "%s", 1, 0 )'%( ip, mac ) )
		
	def removeTerminal(self, ip='', mac=''):
		where = ''
		if ip:
			where = 'WHERE IPv4="%s" '%ip
		if mac:
			where = ( where and 'OR Mac="%s"'%mac ) or 'WHERE Mac="%s"'%mac
		self.__db.execute( 'DELETE FROM terminal %s'%where )

	def existsTerminal(self, ip, mac):
		where = 'WHERE IPv4="%s" AND Mac="%s"'%( ip, mac )
		cur = self.__db.execute( 'SELECT * FROM terminal %s'%where )
		return cur.rowcount > 0

	def findAllTerminal(self):
		cur = self.__db.execute( 'SELECT * FROM terminal' )
		return cur.fetchall()
	
	def activateTerminal(self, ip):
		self.__db.execute( 'UPDATE terminal SET IsActive=1 WHERE IPv4="%s"'%ip )
		
	def frozenTerminal(self, ip):
		self.__db.execute( 'UPDATE terminal SET IsActive=0 WHERE IPv4="%s"'%ip )
		

	
#test case
if __name__ == '__main__':
	db = DB()