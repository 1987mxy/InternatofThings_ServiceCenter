#coding=UTF-8
'''
Created on 2012-8-22

@author: XPMUser
'''
import socket, threading

from Global import Logger, TerminalManager
from Config import srvCenterConf
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
		self.__switch = True
		
		self.__innerThread = None
		self.__outerThread = None
		self.__innerPort = None
		self.__outerPort = None
		
		self.__innerSock = None
		self.__outerSock = None
		
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
		
	def stop(self):
		self.__switch = False
		self.__innerSock.shutdown( socket.SHUT_RDWR )
		self.__innerSock.close()
		self.__outerSock.shutdown( socket.SHUT_RDWR )
		self.__outerSock.close()
		
	def __innerListener(self):
		self.__innerSock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__innerSock.bind( ( '', self.__innerPort ) )
		self.__innerSock.listen(100)
		Logger.info( 'Inner service listening...' )
		while self.__switch:
			sockclient, addr = self.__innerSock.accept()
			Logger.info( '%s:%s Inner service connected...'%addr )
			inner = InnerService.InnerService( sockclient, addr[0] )
			inner.running()
		self.__innerSock.close()
	
	def __outerListener(self):
		self.__outerSock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__outerSock.bind( ( '', self.__outerPort ) )
		self.__outerSock.listen(100)
		Logger.info( 'Outer service listening...' )
		while self.__switch:
			sockclient, addr = self.__outerSock.accept()
			Logger.info( '%s:%s Outer service connected...'%addr )
			outer = OuterService.OuterService( sockclient, addr[0] )
			outer.setTerminalManager( TerminalManager )
			outer.running()
		self.__outerSock.close()