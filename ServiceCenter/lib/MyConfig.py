'''
Created on 2012-8-10

@author: Moxiaoyong
'''
class MyConfig(object):
	'''
	≈‰÷√
	'''
	innerPort = None
	outerPort = None
	magicCode = None
	heartCode = None
	responseCode = None
	
srvCenterConf = MyConfig()
srvCenterConf.innerPort = 8782
srvCenterConf.outerPort = 8983
srvCenterConf.magicCode = 0xDCBA
srvCenterConf.heartCode = 0x0F0F