#coding=UTF-8
from struct import pack, unpack, calcsize

from re import findall
	
class _Packager():
	__me = None
	
	def __init__(self):
		self.__db = None
		self.__table = 'datapackage'
		
		self.__magicCode = None
		self.__heartCode = None
		self.__headerStruct = None

	@staticmethod
	def instance(db, config):
		if _Packager.__me == None:
			_Packager.__me = _Packager()
			_Packager.__me.setDB( db )
			_Packager.__me.config( config )
		else:
			return _Packager.__me

	def setDB(self, db):
		self.__db = db
	
	def config(self, config):
		self.__magicCode = config.magicCode
		self.__heartCode = config.heartCode
		self.__headerStruct = config.headerStruct

	def genHeader(self, bodySize, code, pid):
		return pack( self.__headerStruct, bodySize + 6, 
											self.__magicCode, 
											code, 
											pid )

	def parseHeader(self, header):
		return unpack( self.__headerStruct )

	def genePackage(self, name, pid, data):
		packageDetail = self.nameFindPackage( name )
		if packageDetail['Struct'] == '':
			return ''
		struct = packageDetail['Struct']
		structCount = findall( '\d+[xcbB?hHiIlLqQfdspP]', struct ).__len__()
		groupCount = len( data ) / structCount
		if len( data ) % structCount != 0 or ( struct[-1] in ['s', 'p'] and groupCount != 1 ):
			raise 'Package data invalid!'

		if struct[-1] in ['s', 'p']:
			struct = '%s%d%s'%( struct[:-1], len( data[-1] ), struct[-1] )
		bodySize = calcsize( struct ) * groupCount
		return '%s%s' % ( self.genHeader( bodySize, packageDetail['Struct'], pid ), 
							pack( '<%s' % ( struct * groupCount ), *data ) )
		
	def parsePackage(self, code, package):
		packageDetail = self.codeFindPackage( code )
		struct = packageDetail['Struct']
		if struct[-1] in ['s', 'p']:
			surplusLen = len( package ) - calcsize( struct[:-1] )
			struct = '%s%d%s' % ( struct[:-1], surplusLen, struct[-1] )
		groupCount = len( package ) / calcsize( struct )
		data = unpack( '<%s' % ( struct * groupCount ) )
		structLabel = str.split( ',', packageDetail['StructLabel'] )
		structLabelCount = len( structLabel )
		packageData = []
		for i in range( groupCount ):
			thePackageData = {}
			for j in range( structLabelCount ):
				thePackageData[ structLabel[ j ] ] = data[ structLabelCount * i + j ]
			packageData.append( thePackageData )
		return packageData
	
	def setPackage(self, packageInfo):
		for field, value in packageInfo:
			if value == '' and field != 'memo':
				return False
		if self.existsPackage( packageInfo[ 'name' ], packageInfo[ 'code' ] ):
			return False
		return self.__db.insert( self.__table, packageInfo )
	
	def existsPackage(self, name='', code=''):
		where = 'Name="%s" OR Code=%s'%( name, code )
		count = self.__db.count( self.__table, where )
		return count > 0
	
	def removePackage(self, name='', code=''):
		where = ''
		if name:
			where = 'Name="%s" '%name
		if code:
			where = ( where and 'OR Code=%s'%code ) or 'Code=%s'%code
		return self.__db.delete( self.__table, where )
		
	def modifyPackage(self, packageID, packageInfo):
		for field, value in packageInfo:
			if value == '' and field != 'memo':
				return False
		where = 'PackageID=%d' % packageID
		return self.__db.update( self.__table, packageInfo, where )
	
	def findAllPackages(self):
		return self.__db.select( self.__table )
		
	def codeFindPackage(self, code):
		where = 'Code=%d'%code
		return self.__db.selectOne( self.__table, where )

	def nameFindPackage(self, name):
		where = 'Name="%s"'%name
		return self.__db.selectOne( self.__table, where )

from sys import modules
from lib.DB import Database
from lib import Config
modules[__name__] = _Packager.instance( Database, Config.srvCenterConf )