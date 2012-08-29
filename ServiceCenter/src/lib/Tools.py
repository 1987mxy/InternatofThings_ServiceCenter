#coding=gbk
from os import popen
from time import sleep
from re import split, findall, M
import socket
import platform.system

from lib.Log import LOG
		
#def killProcess(processName):
#	tasklist = popen('tasklist /FI "IMAGENAME eq %s"'%processName).readlines()
#	result = ''
#	if tasklist:
#		for line in tasklist[3:]:
#			pid = split('\s+', line, 2)[1]
#			result = runCMD('killprocess.exe %s' % pid)
#			if processName in popen('tasklist /FI "IMAGENAME eq %s"'%processName).read():
#				LOG.error('kill process fail : %s'%result)
#			else:
#				result = '关闭%s进程成功\n'%processName
#	return result

def killProcess(processName):
	i = 0
	while processName.lower() in popen('tasklist /FI "IMAGENAME eq %s"'%processName).read().lower():
		popen('start /B taskkill /F /IM %s /T'%processName)
		if i>=5:
			LOG.error('关闭%s进程失败\n'%processName)
		else:
			i+=1
			sleep(1)
	if i>0:
		return '关闭%s进程成功\n'%processName
	else:
		return ''
	
def getIP():
	host = socket.gethostname()
	return socket.gethostbyname( host )

def getNermark():
	netmarkPool = ['128.0.0.0','192.0.0.0','224.0.0.0','240.0.0.0','248.0.0.0','252.0.0.0','254.0.0.0','255.0.0.0',
					'255.128.0.0','255.192.0.0','255.224.0.0','255.240.0.0','255.248.0.0','255.252.0.0','255.254.0.0','255.255.0.0',
					'255.255.128.0','255.255.192.0','255.255.224.0','255.255.240.0','255.255.248.0','255.255.252.0','255.255.254.0','255.255.255.0',
					'255.255.255.128','255.255.255.192','255.255.255.224','255.255.255.240','255.255.255.248','255.255.255.252','255.255.255.254']
	systemName = platform.system()
	if systemName == 'Windows':
		ipCommand = 'ipconfig'
	elif systemName == 'Linux':
		ipCommand = 'ifconfig'
	ipInfo = popen( ipCommand ).read()
	
	for theNetmark in netmarkPool:
		netmark = findall( theNetmark, ipInfo, M )
		if netmark:
			return netmark.pop()
