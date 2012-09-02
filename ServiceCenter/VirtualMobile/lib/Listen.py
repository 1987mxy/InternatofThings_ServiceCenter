#coding=UTF-8
'''
Created on 2012-8-22

@author: XPMUser
'''
import socket, threading

from Global import Logger, TerminalManager
from Config import RUN, srvCenterConf
from Service import InnerService, OuterService

class Listen(object):
	'''
	聆听者，聆听网络socket连接
	'''
	__me = None

	def __init__(self):
		'''
		构造函数
		'''
		self.__config = None
		
		self.__innerThread = None
		self.__outerThread = None
		self.__innerPort = None
		self.__outerPort = None
		
		self.config( srvCenterConf )
		
	@staticmethod
	def instance():
		if Listen.__me == None:
			Listen.__me = Listen()
		return Listen.__me
		
	def config(self, config):
		self.__innerPort = config.innerPort
		self.__outerPort = config.outerPort
		
	def running(self):
		self.__innerThread = threading.Thread(target=self.__innerListener)
		self.__outerThread = threading.Thread(target=self.__outerListener)
		self.__innerThread.start()
		self.__outerThread.start()
		
	def __innerListener(self):
		sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		sock.bind( ( '', self.__innerPort ) )
		sock.listen(100)
		Logger.info('Inner service listening...')
		while RUN:
			sockclient, addr = sock.accept()
			Logger.info( '%s:%s Inner service connected...'%addr )
			inner = InnerService.InnerService( sockclient, addr[0] )
			inner.running()
		sock.close()
	
	def __outerListener(self):
		sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		sock.bind( ( '', self.__outerPort ) )
		sock.listen(100)
		Logger.info('Outer service listening...')
		while RUN:
			sockclient, addr = sock.accept()
			Logger.info( '%s:%s Outer service connected...'%addr )
			outer = OuterService.OuterService( sockclient, addr[0] )
			outer.setTerminalManager( TerminalManager )
			outer.running()
		sock.close()