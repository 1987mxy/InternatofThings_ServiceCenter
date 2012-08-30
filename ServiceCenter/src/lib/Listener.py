#coding=UTF-8
'''
Created on 2012-8-22

@author: XPMUser
'''

import socket, threading
from lib.Log import LOG
from lib.Config import RUN, srvCenterConf
from lib.Service import InnerService, OuterService

class _Listener(object):
	'''
	聆听者，聆听网络socket连接
	'''
	__me = None

	def __init__(self):
		'''
		构造函数
		'''
		self.__inner
		self.__outer
		self.__innerPort
		self.__outerPort
		
	@staticmethod
	def instance(config):
		if _Listener.__me == None:
			_Listener.__me = _Listener()
			_Listener.__me.config( config )
		else:
			return _Listener.__me
		
	def config(self, config):
		self.__innerPort = config.innerPort
		self.__outerPort = config.outerPort
		
	def running(self):
		self.__inner = threading.Thread(target=self.__innerListener)
		self.__outer = threading.Thread(target=self.__outerListener)
		self.__inner.start()
		self.__outer.start()
		
	def __innerListener(self):
		sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		sock.bind( ( '', self.__innerPort ) )
		sock.listen(100)
		while RUN:
			sockclient, addr = sock.accept()
			LOG.info('%s:%s Inner service connected...'%addr)
			inner = InnerService.InnerService(sockclient, addr[0])
			inner.config( srvCenterConf )
			inner.running()
		sock.close()
	
	def __outerListener(self):
		sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		sock.bind( ( '', self.__outerPort ) )
		sock.listen(100)
		while RUN:
			sockclient, addr = sock.accept()
			LOG.info('%s:%s Outer service connected...'%addr)
			outer = OuterService.OuterService(sockclient, addr[0])
			outer.config( srvCenterConf )
			outer.running()
		sock.close()

from sys import modules
modules[__name__] = _Listener.instance( srvCenterConf )