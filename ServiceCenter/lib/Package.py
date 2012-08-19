#coding=gbk
from os import path as ospath
from struct import pack, calcsize

from Config import PACKAGE_SIZE
from lib.Tools import runCMD,chkPath
from lib.Log import LOG


def getBasicData():
	pass
	

def pack1(cltlist_string, cmdpack):  #指令包
	mdata_len = cltlist_string.__len__() + cmdpack.__len__()
	package = pack('<HLHHL%ss'%mdata_len, 12 + mdata_len, 
										  0xAAAC, 
										  12 + mdata_len, 
										  0x0001, 
										  0, 
										  '%s%s'%(cltlist_string, cmdpack))
	return package				   

def pack2(result):  #反馈包
	package = pack('<HLHHL%ss'%result.__len__(), 12 + result.__len__(), 
												 0xAAAC, 
												 12 + result.__len__(), 
												 0x0002, 
												 0, 
												 result)
	return package


 
def pack5():	#获取client列表操作包
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x05\x00\x00\x00\x00\x00'
	
def pack6(heartID):	#心跳包
		heartIDString = pack('<L',heartID)
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x06\x00%s'%heartIDString

def packSrvEnd():
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\xf0\xf0\x00\x00\x00\x00'

def packCltEnd():   #给客户端的包发送完成信息
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\xff\xff\x00\x00\x00\x00'
	
def packCtrlEnd():   #给控制端的包发送完成信息
		return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x00\xff\x00\x00\x00\x00'
	   
def packProxyEnd():   #给控制端的包发送完成信息
		return '\x0c\x00\xab\xaa\x00\x00\x06\x00\x00\xff\x00\x00\x00\x00'
	
	
def packRemoteStart( Mac ):
	import socket,binascii
	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	package = binascii.a2b_hex('ffffffffffff'+Mac*16)
	sock.sendto(package,('255.255.255.255',6666))
