'''
Created on 2012-8-14

@author: Moxiaoyong
'''

import socket

class InnerService(object):
	'''
	classdocs
	'''


	def __init__(self, ip='', port):
		'''
		Constructor
		'''
		self.__sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__sock.bind( ( ip, port ) )
		