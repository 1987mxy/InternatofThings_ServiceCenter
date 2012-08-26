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

	def running(self):
		super( InnerService, self ).running()
		self.__chkThread = threading.Thread(target=self.chkResponse)
		self.__recvThread.start()
		self.__mainThread.start()
		self.__chkThread.start()
		
	def main(self):
		while self.__switch:
			pass
		