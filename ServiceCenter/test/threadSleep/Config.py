#coding=UTF-8
'''
Created on 2012-8-10

@author: Moxiaoyong
'''

from Tools import getIP, getNetmark, getBroadcostAddr, getNetworkAddr

class Config(object):
	'''
	配置
	'''
	
	def __init__(self):
		self.innerPort = None
		self.outerPort = None
		self.magicCode = None
		self.heartCode = None
		self.responseCode = None
		self.timeout = None
	
srvCenterConf = Config()
srvCenterConf.innerPort = 8983
srvCenterConf.outerPort = 8782
srvCenterConf.magicCode = 0xDCBA
srvCenterConf.heartCode = 0x0F0F
srvCenterConf.headerStruct = '<HHHH'
srvCenterConf.timeout = 30


#===============================================================================
# network
#===============================================================================

IP = getIP()

NETMARK = getNetmark()

BROADCASTADDR = getBroadcostAddr()

NETWORKADDR = getNetworkAddr()

#===============================================================================
# log
#===============================================================================

PRINT_LOG = True

PRINT_RUNLOG = True

PRINT_PERFORMANCELOG = True

#===============================================================================
# program parameter
#===============================================================================

Status = 'debug'

#===============================================================================
# PACKAGE
#===============================================================================

RUN = True