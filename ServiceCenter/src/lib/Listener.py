'''
Created on 2012-8-22

@author: XPMUser
'''

import socket, threading
from lib.Log import LOG
from lib.Config import RUN
from lib.Service import InnerService, OuterService

class Listener(object):
	'''
	classdocs
	'''

	def __init__(self):
		'''
		构造函数
		'''
		self.__inner
		self.__outer
		self.__innerPort
		self.__outerPort
		
	def config(self, config):
		self.__innerPort = config.innerPort
		self.__outerPort = config.outerPort
		
	def running(self):
		self.__inner = threading.Thread(target=self.__innerListener)
		self.__outer = threading.Thread(target=self.__outerListener)
		self.__inner.start()
		self.__outer.start()
		
	def __innerListener(self):
		global RUN
		sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		sock.bind( ( '', self.__innerPort ) )
		sock.listen(100)
		while RUN:
			sockclient, addr = sock.accept()
			LOG.info('%s:%s Inner service connected...'%addr)
			inner = InnerService(sockclient, addr)
			inner.running()
		sock.close()
	
	def __outerListener(self):
		global RUN
		sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		sock.bind( ( '', self.__outerPort ) )
		sock.listen(100)
		while RUN:
			sockclient, addr = sock.accept()
			LOG.info('%s:%s Outer service connected...'%addr)
			outer = OuterService(sockclient, addr)
			outer.running()
		sock.close()
		
		