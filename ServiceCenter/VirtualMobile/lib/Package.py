#coding=UTF-8
from struct import pack, unpack, calcsize

from re import findall

from Global import DB
from Config import srvCenterConf
	
class Package():
	'''
	数据包管理者(单例模式)，管理、生成和解析所有数据包
	'''
	__me = None
	
	def __init__(self):
		self.__db = None
		self.__table = 'datapackage'
		self.__fieldList = [ 'PackageID', 'Name', 'Code', 'Struct', 'StructLabel', 'ExistReply', 'Encrypt' ]
		
		self.__magicCode = None
		self.__heartCode = None
		self.__headerStruct = None
		self.__headerSize = None

		self.__encipherer = {}
		
		self.setDB( DB )
		self.config( srvCenterConf )
		
		
	@staticmethod
	def instance():
		if Package.__me == None:
			Package.__me = Package()
		return Package.__me

	def setDB(self, db):
		self.__db = db
	
	def config(self, config):
		self.__magicCode = config.magicCode
		self.__heartCode = config.heartCode
		self.__headerStruct = config.headerStruct
		self.__headerSize = calcsize( self.__headerStruct )

	def setEncipherer(self, master, encrypt, encipherer):
		if self.__encipherer.has_key( master ) == False:
			self.__encipherer[ master ] = {}
		self.__encipherer[ master ][ encrypt ] = encipherer

	def genHeader(self, bodySize, code, pid):
		return pack( self.__headerStruct, bodySize + self.__headerSize - 2, 
											self.__magicCode, 
											code, 
											pid )

	def parseHeader(self, header):
		return unpack( self.__headerStruct, header )

	def genPackage(self, master, name, pid, data=[]):
		packInfo = self.nameFindPackage( name )
		
		print '='*20
		print packInfo
		
		if packInfo['Struct'] == '':
			return ''
		struct = packInfo['Struct']
		structCount = findall( '\d*[xcbB?hHiIlLqQfdspP]', struct ).__len__()
		groupCount = len( data ) / structCount
		
		if len( data ) % structCount != 0 or ( struct[-1] in ['s', 'p'] and groupCount != 1 ):
			raise Exception( 'Package data invalid!' )

		if struct[-1] in ['s', 'p']:
			struct = '%s%d%s'%( struct[:-1], len( data[-1] ), struct[-1] )
		packBody = pack( '<%s' % ( struct * groupCount ), *data )
		
		#加密
		if packInfo['Encrypt'] in self.__encipherer.keys():
			packBody = self.__encipherer[ master ][ packInfo['Encrypt'] ]( 'encrypt', packBody )
		
		bodySize = len( packBody )
		return '%s%s' % ( self.genHeader( bodySize, packInfo['Code'], pid ), 
							packBody )
		
	def parsePackage(self, master, code, packBody):
		packInfo = self.codeFindPackage( code )
		
		#解密
		if packInfo['Encrypt'] in self.__encipherer.keys():
			packBody = self.__encipherer[ master ][ packInfo['Encrypt'] ]( 'decrypt', packBody )
		
		struct = packInfo['Struct']
		if struct[-1] in ['s', 'p']:
			surplusLen = len( packBody ) - calcsize( struct[:-1] )
			struct = '%s%d%s' % ( struct[:-1], surplusLen, struct[-1] )
		groupCount = len( packBody ) / calcsize( struct )
		data = unpack( '<%s' % ( struct * groupCount ), packBody )
		return data
	
	def setPackage(self, packageInfo):
		for field, value in packageInfo:
			if value == '' and field != 'memo':
				return False
		if self.existsPackage( packageInfo[ 'name' ], packageInfo[ 'code' ] ):
			return False
		return self.__db.io( 'insert', [ self.__table, packageInfo ] )
	
	def existsPackage(self, name='', code=''):
		where = 'Name="%s" OR Code=%s'%( name, code )
		count = self.__db.io( 'count', [ self.__table, where ] )
		return count > 0
	
	def removePackage(self, name='', code=''):
		where = ''
		if name:
			where = 'Name="%s" '%name
		if code:
			where = ( where and 'OR Code=%s'%code ) or 'Code=%s'%code
		return self.__db.io( 'delete', [ self.__table, where ] )
		
	def modifyPackage(self, packageID, packageInfo):
		for field, value in packageInfo:
			if value == '' and field != 'memo':
				return False
		where = 'PackageID=%d' % packageID
		return self.__db.io( 'update', [ self.__table, packageInfo, where ] )
	
	def findAllPackages(self):
		return self.__db.io( 'select', [ self.__table, ','.join( self.__fieldList ) ] )
		
	def codeFindPackage(self, code):
		where = 'Code=%d'%code
		return self.__db.io( 'selectOne', [ self.__table, ','.join( self.__fieldList ), where ] )

	def nameFindPackage(self, name):
		where = 'Name="%s"'%name
		return self.__db.io( 'selectOne', [ self.__table, ','.join( self.__fieldList ), where ] )
	
	def existsReply(self, name):
		where = 'Name="%s"'%name
		return self.__db.io( 'selectOne', [ self.__table, ','.join( self.__fieldList ), where ] )['ExistReply'] == 0b1