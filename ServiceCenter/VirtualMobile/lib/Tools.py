#coding=UTF-8
from socket import gethostname, gethostbyname, inet_aton, inet_ntoa
import platform

from re import findall, I
from os import popen
from struct import unpack, pack

#获取Mac地址
def getMac(ip):
	arpList = popen('arp -a %s'%ip)
	for arp in arpList.readlines():
		if ip in arp:
			mac = findall( '[0-9A-F]{2}[-:][0-9A-F]{2}[-:][0-9A-F]{2}[-:][0-9A-F]{2}[-:][0-9A-F]{2}[-:][0-9A-F]{2}', arp, I )
			return ( mac and mac[0] ) or ''
	return ''

#获取本机IP地址
def getIP():
	host = gethostname()
	return gethostbyname( host )

#获取本机子网掩码
def getNetmark():
	netmarkPool = [	'255.255.255.0','255.255.0.0','255.0.0.0',
					'255.255.255.254','255.255.255.252','255.255.255.248','255.255.255.240','255.255.255.224','255.255.255.192','255.255.255.128',
					'255.255.254.0','255.255.252.0','255.255.248.0','255.255.240.0','255.255.224.0','255.255.192.0','255.255.128.0',
					'255.254.0.0','255.252.0.0','255.248.0.0','255.240.0.0','255.224.0.0','255.192.0.0','255.128.0.0',
					'254.0.0.0','252.0.0.0','248.0.0.0','240.0.0.0','224.0.0.0','192.0.0.0','128.0.0.0' ]
	systemName = platform.system()
	if systemName == 'Windows':
		ipCommand = 'ipconfig'
	elif systemName == 'Linux':
		ipCommand = 'ifconfig'
	ipCfg = popen( ipCommand ).read()
	
	for theNetmark in netmarkPool:
		if theNetmark in ipCfg:
			return theNetmark
		
#获取本网段广播地址
def getBroadcostAddr():
	ip = getIP()
	netmark = getNetmark()
	ipBit = unpack( 'L', inet_aton( ip ) )[0]
	netmarkBit = unpack( 'L', inet_aton( netmark ) )[0]
	
	netAddrBit = ipBit & netmarkBit
	ipCount = netmarkBit ^ 0xFFFFFFFF
	
	return inet_ntoa( pack( 'L', netAddrBit + ipCount ) )

#获取本网段网络地址
def getNetworkAddr():
	ip = getIP()
	netmark = getNetmark()
	ipBit = unpack( 'L', inet_aton( ip ) )[0]
	netmarkBit = unpack( 'L', inet_aton( netmark ) )[0]
	
	return inet_ntoa( pack( 'L', ipBit & netmarkBit ) )

#test case
if __name__=='__main__':
	print getIP()
	print getNetmark()
	print getNetworkAddr()
	print getBroadcostAddr()
	print getMac('172.16.0.254')