'''
Created on 2012-8-26

@author: XPMUser
'''

class Event(object):
	'''
	classdocs
	'''

	def __init__(self):
		'''
		Constructor
		'''
		pass
	
	def packRemoteStart( Mac ):
		import socket,binascii
		sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		package = binascii.a2b_hex('ffffffffffff'+Mac*16)
		sock.sendto(package,('255.255.255.255',6666))