#coding=UTF-8
'''
Created on 2012-8-19

@author: XPMUser
'''

class DB(object):
	'''
	数据库类，用来操作“数据包表”和“终端表”
	'''
	__db = None

	def __init__(self):
		import sqlite3
		import os.path
		if os.path.isfile( 'Data.dat' ):
			self.__db = sqlite3.connect('Data.dat')
		else:
			self.__db = sqlite3.connect('Data.dat')
			self.__install()
		
		
	def __install(self):
		sql_file = open('install.sql','rb')
		sql = sql_file.read()
		sql_file.close()
		self.__db.executescript( sql )
		
	def sqlDump(self):
		self.removeTerminal()
		sql_file = open('install.sql','rb')
		for sql_line in self.__db.iterdump():
			sql_file.write( sql_line )
		sql_file.close()
		
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
		cur = self.__db.execute( 'SELECT * FROM datapackage %s'%where )
		return cur.rowcount > 0

	def findAllTerminal(self):
		cur = self.__db.execute( 'SELECT * FROM terminal' )
		return cur.fetchall()
	
	def activateTerminal(self, ip):
		self.__db.execute( 'UPDATE terminal SET IsActive=1 WHERE IPv4="%s"'%ip )
		
	def frozenTerminal(self, ip):
		self.__db.execute( 'UPDATE terminal SET IsActive=0 WHERE IPv4="%s"'%ip )
		
	def setPackage(self, protocal, name, direction, code, struct, memo=''):
		if ( not protocal ) or ( not name ) or ( not direction ) or ( not code ) or ( not struct ):
			return False
		if self.existsPackage( name, code ):
			return False
		cur = self.__db.execute( 'INSERT INTO datapackage ( Protocol, Name, Direction, Code, Struct, Memo ) VALUES ( "%s", "%s", %d, "%s", "%s", "%s" )'
									%( protocal, name, direction, code, struct, memo ) )
		return cur.lastrowid
	
	def existsPackage(self, name='', code=''):
		where = 'WHERE Name="%s" OR Code=%s'%( name, code )
		cur = self.__db.execute( 'SELECT * FROM datapackage %s'%where )
		return cur.rowcount > 0
	
	def removePackage(self, name='', code=''):
		where = ''
		if name:
			where = 'WHERE Name="%s" '%name
		if code:
			where = ( where and 'OR Code=%s'%code ) or 'WHERE Code=%s'%code
		self.__db.execute( 'DELETE FROM datapackage %s'%where )
		
	def modifyPackage(self, package_id, protocal, name, direction, code, struct, memo=''):
		if ( not protocal ) or ( not name ) or ( not direction ) or ( not code ) or ( not struct ):
			return False
		self.__db.execute( 'UPDATE datapackage SET Protocol="%s", Name="%s", Direction=%d, Code=%d, Struct="%s", Memo="%s" WHERE PackageID=%d'
							%( protocal, name, direction, code, struct, memo, package_id ) )
		
	def findAllPackages(self):
		cur = self.__db.execute( 'SELECT * FROM datapackage' )
		return cur.fetchall()
		
	def findPackage(self, code):
		cur = self.__db.execute( 'SELECT * FROM datapackage WHERE Code=%d'%code )
		return cur.fetchone()


#test case
if __name__ == '__main__':
	db = DB()