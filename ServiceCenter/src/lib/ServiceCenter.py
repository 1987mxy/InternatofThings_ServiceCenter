#coding=UTF-8
'''
Created on 2012-8-10

@author: Moxiaoyong
'''

import socket

from lib import Config

class ServiceCenter(object):
	'''
	服务中心
	'''
	def __init__(self):
		'''
		Constructor
		'''
		global srvCenterConf
		self.__inner = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__inner.bind(('', srvCenterConf.innerPort))
		self.__outer = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__outer.bind(('', srvCenterConf.outerPort))