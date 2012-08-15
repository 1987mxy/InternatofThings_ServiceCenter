'''
Created on 2012-8-10

@author: Moxiaoyong
'''
class Config(object):
	'''
	≈‰÷√
	'''
	innerPort = None
	outerPort = None
	magicCode = None
	heartCode = None
	responseCode = None
	
srvCenterConf = Config()
srvCenterConf.innerPort = 8782
srvCenterConf.outerPort = 8983
srvCenterConf.magicCode = 0xDCBA
srvCenterConf.heartCode = 0x0F0F

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

PACKAGE_SIZE = 600  #0x0003∞¸≥§∂»