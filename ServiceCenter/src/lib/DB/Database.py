#coding=UTF-8
'''
Created on 2012-8-19

@author: XPMUser
'''

class _Database(object):
	'''
	数据库类，用来操作“数据包表”和“终端表”
	'''
	__me = None

	def __init__(self):
		import sqlite3
		import os.path
		if os.path.isfile( 'Data.dat' ):
			self.__db = sqlite3.connect('Data.dat')
		else:
			self.__db = sqlite3.connect('Data.dat')
			self.__install()
		
	@staticmethod
	def instance():
		if _Database.__me == None:
			_Database.__me = _Database()
		else:
			return _Database.__me
		pass
		
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
		cur = self.__db.execute( 'INSERT INTO %s SET %s' % ( table, str.join( ', ', columnList ) ) )
		return cur.lastrowid
	
	def delete(self, table, where=''):
		where = ( where and 'WHERE %s' % where ) or ''
		cur = self.__db.execute( 'DELETE FROM %s %s'%( table, where ) )
		return cur.rowcount
	
	def update(self, table, data, where=''):
		columnList = []
		for field, value in data:
			columnList.append( '%s="%s"' % ( field, value ) )
		where = ( where and 'WHERE %s' % where ) or ''
		cur = self.__db.execute( 'UPDATE %s SET %s %s' % ( table, str.join( ', ', columnList ), where ) )
		return cur.rowcount
	
	def select(self, table, where=''):
		where = ( where and 'WHERE %s'%where ) or ''
		cur = self.__db.execute( 'SELECT * FROM %s %s'%(table, where) )
		return cur.fetchall()
	
	def selectOne(self, table, where=''):
		where = ( where and 'WHERE %s'%where ) or ''
		cur = self.__db.execute( 'SELECT * FROM %s %s Limit 0, 1'%(table, where) )
		return cur.fetchone()
	
	def count(self, table, where=''):
		where = ( where and 'WHERE %s'%where ) or ''
		cur = self.__db.execute( 'SELECT COUNT(*) AS `count` FROM %s %s'%(table, where) )
		return cur.fetchone()[ 'count' ]
	
	def query(self, sql):
		cur = self.__db.execute( sql )
		return cur
	
from sys import modules
modules[__name__] = _Database.instance()
