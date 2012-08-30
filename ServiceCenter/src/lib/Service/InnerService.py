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
	
	def __init__(self, socket, address):
		super( InnerService, self ).__init__( socket, address )

	def running(self):
		super( InnerService, self ).running()
		self.chkThread = threading.Thread( target=self.chkHeart )
		self.recvThread.start()
		self.mainThread.start()
		self.chkThread.start()
		
	def main(self):
		pass
		