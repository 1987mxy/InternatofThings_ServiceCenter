#coding=UTF-8
'''
Created on 2012-8-14

@author: Moxiaoyong
'''

import threading

import Service

class InnerService(Service.Service):
	'''
	内部服务器，面向局域网的各种终端
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
		