#coding=utf-8
from os import path as ospath
from struct import pack, calcsize

from Config import PACKAGE_SIZE
from lib.Tools import runCMD,chkPath
from lib.Log import LOG

import re.findall


def getBasicData():
	pass
	

def pack1(cltlist_string, cmdpack):  #ָ���
	mdata_len = cltlist_string.__len__() + cmdpack.__len__()
	package = pack('<HLHHL%ss'%mdata_len, 12 + mdata_len, 
										  0xAAAC, 
										  12 + mdata_len, 
										  0x0001, 
										  0, 
										  '%s%s'%(cltlist_string, cmdpack))
	return package				   

def pack2(result):  #������
	package = pack('<HLHHL%ss'%result.__len__(), 12 + result.__len__(), 
												 0xAAAC, 
												 12 + result.__len__(), 
												 0x0002, 
												 0, 
												 result)
	return package


 
def pack5():	#��ȡclient�б������
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x05\x00\x00\x00\x00\x00'
	
def pack6(heartID):	#�����
		heartIDString = pack('<L',heartID)
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x06\x00%s'%heartIDString

def packSrvEnd():
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\xf0\xf0\x00\x00\x00\x00'

def packCltEnd():   #��ͻ��˵İ��������Ϣ
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\xff\xff\x00\x00\x00\x00'
	
def packCtrlEnd():   #����ƶ˵İ��������Ϣ
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x00\xff\x00\x00\x00\x00'
	   
def packProxyEnd():   #����ƶ˵İ��������Ϣ
		return '\x0c\x00\xab\xaa\x00\x00\x06\x00\x00\xff\x00\x00\x00\x00'
	
	
def packRemoteStart( Mac ):
	import socket,binascii
	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	package = binascii.a2b_hex('ffffffffffff'+Mac*16)
	sock.sendto(package,('255.255.255.255',6666))
	
class PackageManager():
	
	def __init__(self, db):
		self.__db = db
		self.__table = 'datapackage'
		self.__magicCode = None
		self.__heartCode = None
		self.__headerStruct = None
		
	def config(self, config):
		self.__magicCode = config.magicCode
		self.__heartCode = config.heartCode
		self.__headerStruct = config.headerStruct
		
	def getHeader(self):
		pass
		
	def generatePackage(self, name, data):
		packageDetail = self.nameFindPackage(name)
		struct = re.findall( '\d[xcbB?hHiIlLqQfdspP]', packageDetail['Struct'] )
		structLabel = str.split( ',', packageDetail['StructLabel'] )
		
	def parsePackage(self, code, package):
		packageDetail = self.codeFindPackage(code)
	
	def setPackage(self, packageInfo):
		for field, value in packageInfo:
			if value == '' and field != 'memo':
				return False
		if self.existsPackage( packageInfo[ 'name' ], packageInfo[ 'code' ] ):
			return False
		cur = self.__db.insert( self.__table, packageInfo )
		return cur.lastrowid
	
	def existsPackage(self, name='', code=''):
		where = 'Name="%s" OR Code=%s'%( name, code )
		count = self.__db.count( self.__table, where )
		return count > 0
	
	def removePackage(self, name='', code=''):
		where = ''
		if name:
			where = 'WHERE Name="%s" '%name
		if code:
			where = ( where and 'OR Code=%s'%code ) or 'WHERE Code=%s'%code
		self.__db.delete( self.__table, where )
		return self.__db.rowcount
		
	def modifyPackage(self, packageID, packageInfo):
		for field, value in packageInfo:
			if value == '' and field != 'memo':
				return False
		where = 'PackageID=%d' % packageID
		self.__db.update( self.__table, packageInfo, where )
		return self.__db.rowcount
	
	def findAllPackages(self):
		cur = self.__db.select( self.__table )
		return cur.fetchall()
		
	def codeFindPackage(self, code):
		where = 'Code=%d'%code
		cur = self.__db.select( self.__table, where )
		return cur.fetchone()

	def nameFindPackage(self, name):
		where = 'Name="%s"'%name
		cur = self.__db.select( self.__table, where )
		return cur.fetchone()
		