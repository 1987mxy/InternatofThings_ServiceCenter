'''
Created on 2012-8-14

@author: Moxiaoyong
'''

from lib.Service import Service

import threading

class InnerService(Service):
	'''
	classdocs
	'''
	server = []
	
	def __init__(self, socket, address):
		InnerService.server[ address ] = self
		
		super( InnerService, self ).__init__( socket, address )

	def running(self):
		super( InnerService, self ).running()
		self.__chkThread = threading.Thread( target=self.chkHeart )
		self.__recvThread.start()
		self.__mainThread.start()
		self.__chkThread.start()
		
	def main(self):
		pass
		