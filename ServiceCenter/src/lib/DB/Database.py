#coding=UTF-8
'''
Created on 2012-8-19

@author: XPMUser
'''
import sqlite3, threading
import os.path

class Database(object):
	'''
	数据库类，用来操作“数据包表”和“终端表”
	'''
	__me = None

	def __init__(self):
		self.__switch = True
		self.__dbQueryQueue = []
		self.__dbReturnQueue = {}
		self.__dbCondition = None
		self.__execThread = None
		self.__execID = 0
		
	@staticmethod
	def instance():
		if Database.__me == None:
			Database.__me = Database()
			Database.__me.running()
		return Database.__me
		
	def running(self):
		self.__dbCondition = threading.Condition()
		self.__execThread = threading.Thread( target=self.execute )
		self.__execThread.start()
		
	def stop(self):
		self.__switch = False
		self.__dbCondition.acquire()
		self.__dbCondition.notify()
		self.__dbCondition.release()
	
	def io(self, function, argv):
		self.__dbCondition.acquire()
		threadID = threading.currentThread().getName()
		execFlag = '%s %d'%( threadID, self.__execID )
		self.__dbQueryQueue.insert( 0, [ execFlag, function, argv ] )
		self.__dbCondition.notify()
		self.__dbCondition.wait()
		result = self.__dbReturnQueue[ execFlag ]
		del self.__dbReturnQueue[ execFlag ]
		self.__execID += 1
		self.__dbCondition.release()
		return result
	
	def execute(self):
		if os.path.isfile( './lib/DB/Data.dat' ):
			self.__db = sqlite3.connect('./lib/DB/Data.dat')
		else:
			self.__db = sqlite3.connect('./lib/DB/Data.dat')
			self.install()
			
		self.__dbCondition.acquire()
		while self.__switch:
			if len( self.__dbQueryQueue ) <= 0:
				self.__dbCondition.wait()
			( execID, function, argv ) = self.__dbQueryQueue.pop()
			func = getattr( self, function )
			self.__dbReturnQueue[ execID ] = func( *argv )
			self.__dbCondition.notify()
		
	def install(self):
		sql_file = open( './lib/DB/install.sql', 'rb' )
		sql = sql_file.read()
		sql_file.close()
		self.__db.executescript( sql )
		
	def backup(self):
		self.delete( 'terminal' )
		sql_file = open( './lib/DB/install.sql', 'wb' )
		for sql_line in self.__db.iterdump():
			sql_file.write( sql_line )
		sql_file.close()
		
	def insert(self, table, data):
		cur = self.query( 'INSERT INTO %s (%s) VALUES ("%s")' % ( table, ','.join( data.keys() ), '","'.join( data.values() ) ) )
		return cur.lastrowid
	
	def delete(self, table, where=''):
		where = ( where and 'WHERE %s' % where ) or ''
		cur = self.query( 'DELETE FROM %s %s'%( table, where ) )
		return cur.rowcount
	
	def update(self, table, data, where=''):
		columnList = []
		for field, value in data.items():
			columnList.append( '%s="%s"' % ( field, value ) )
		where = ( where and 'WHERE %s' % where ) or ''
		cur = self.query( 'UPDATE %s SET %s %s' % ( table, ','.join( columnList ), where ) )
		return cur.rowcount
	
	def select(self, table, fields='*', where=''):
		where = ( where and 'WHERE %s'%where ) or ''
		cur = self.query( 'SELECT %s FROM %s %s'%( fields, table, where ) )
		table = cur.fetchall()
		dataList = []
		if table != None:
			for row in table:
				data = {}
				columnIndex = 0
				for column in cur.description:
					data[ column[0] ] = ( row[ columnIndex ].__class__ is unicode and str( row[ columnIndex ] ) ) or row[ columnIndex ]
					columnIndex += 1
				dataList.append( data )
		return dataList
	
	def selectOne(self, table, fields='*', where=''):
		where = ( where and 'WHERE %s'%where ) or ''
		cur = self.query( 'SELECT %s FROM %s %s Limit 0, 1'%( fields, table, where ) )
		row = cur.fetchone()
		data = {}
		if row != None:
			columnIndex = 0
			for column in cur.description:
				data[ column[0] ] = ( row[ columnIndex ].__class__ is unicode and str( row[ columnIndex ] ) ) or row[ columnIndex ]
				columnIndex += 1
		return data
	
	def count(self, table, where=''):
		where = ( where and 'WHERE %s'%where ) or ''
		cur = self.query( 'SELECT COUNT(*) AS `count` FROM %s %s'%(table, where) )
		return cur.fetchone()[0]
	
	def query(self, sql):
		cur = self.__db.execute( sql )
		self.__db.commit()
		return cur