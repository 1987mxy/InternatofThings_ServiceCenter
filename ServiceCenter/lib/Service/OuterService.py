'''
Created on 2012-8-14

@author: Moxiaoyong
'''

from lib.Service import Service

import threading

class OuterService(Service):
	'''
	classdocs
	'''

	def running(self):
		super( OuterService, self ).running()
		self.__chkThread = threading.Thread(target=self.chkResponse)
		self.__recvThread.start()
		self.__mainThread.start()
		self.__chkThread.start()
		
	def main(self):
		while self.__switch:
			( code, package ) = self.__queue.pop()
