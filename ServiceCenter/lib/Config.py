'''
Created on 2012-8-10

@author: Moxiaoyong
'''
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
	
srvCenterConf = Config()
srvCenterConf.innerPort = 8782
srvCenterConf.outerPort = 8983
srvCenterConf.magicCode = 0xDCBA
srvCenterConf.heartCode = 0x0F0F
srvCenterConf.headerStruct = '<HHHH'; 

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