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

		self.__encipherer = {}
		
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
		self.__headerSize = calcsize( self.__headerStruct )

	def setEncipherer(self, type, encipherer):
		self.__encipherer[ type ] = encipherer

	def genHeader(self, bodySize, code, pid):
		return pack( self.__headerStruct, bodySize + self.__headerSize - 2, 
											self.__magicCode, 
											code, 
											pid )

	def parseHeader(self, header):
		return unpack( self.__headerStruct, header )

	def genPackage(self, name, pid, data=[]):
		packDetail = self.nameFindPackage( name )
		if packDetail['Struct'] == '':
			return ''
		struct = packDetail['Struct']
		structCount = findall( '\d+[xcbB?hHiIlLqQfdspP]', struct ).__len__()
		groupCount = len( data ) / structCount
		if len( data ) % structCount != 0 or ( struct[-1] in ['s', 'p'] and groupCount != 1 ):
			raise 'Package data invalid!'

		if struct[-1] in ['s', 'p']:
			struct = '%s%d%s'%( struct[:-1], len( data[-1] ), struct[-1] )
		packBody = pack( '<%s' % ( struct * groupCount ), *data )
		#加密
		if packDetail['Encrypt'] in self.__encipherer.keys():
			packBody = self.__encipherer[ packDetail['Encrypt'] ]( 'encrypt', packBody )
		bodySize = len( packBody )
		
		return '%s%s' % ( self.genHeader( bodySize, packDetail['Struct'], pid ), 
							packBody )
		
	def parsePackage(self, code, packBody):
		packDetail = self.codeFindPackage( code )
		
		#解密
		if packDetail['Encrypt'] in self.__encipherer.keys():
			packBody = self.__encipherer[ packDetail['Encrypt'] ]( 'decrypt', packBody )
		
		struct = packDetail['Struct']
		if struct[-1] in ['s', 'p']:
			surplusLen = len( packBody ) - calcsize( struct[:-1] )
			struct = '%s%d%s' % ( struct[:-1], surplusLen, struct[-1] )
		groupCount = len( packBody ) / calcsize( struct )
		data = unpack( '<%s' % ( struct * groupCount ) )
		return data
#		structLabel = str.split( ',', packDetail['StructLabel'] )
#		structLabelCount = len( structLabel )
#		packageData = []
#		for i in range( groupCount ):
#			thePackageData = {}
#			for j in range( structLabelCount ):
#				thePackageData[ structLabel[ j ] ] = data[ structLabelCount * i + j ]
#			packageData.append( thePackageData )
#		return packageData
	
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
	
	def existsReply(self, name):
		where = 'Name="%s"'%name
		return self.__db.selectOne( self.__table, where )['ExistReply'] == 0b1

from sys import modules
from lib.DB import Database
from lib import Config
modules[__name__] = _Packager.instance( Database, Config.srvCenterConf )