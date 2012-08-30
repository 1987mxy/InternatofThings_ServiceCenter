#coding=UTF-8
'''
Created on 2012-8-21

@author: XPMUser
'''

from lib import Listener
from lib.Config import srvCenterConf

if __name__ == '__main__':
	Listener.instance(srvCenterConf).running()