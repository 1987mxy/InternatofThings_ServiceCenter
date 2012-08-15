'''
Created on 2012-8-14

@author: Moxiaoyong
'''

import socket

from traceback import format_exc
from struct import unpack

from lib.Log import LOG

class Service(object):
	'''
	classdocs
	'''


	def __init__(self, ip='', port, options):
		'''
		Constructor
		'''
		if self.__class__ is Service:   #≥ÈœÛ¿‡ºÏ≤‚
			LOG.error('Net class dose not instantiation')
			raise 'Net class dose not instantiation'
		
		self.__sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__sock.bind( ( ip, port ) )
		self.__address = '%s:%s'%(ip,port)
		self.__switch = True
		self.__death = False
		self.__magicCode = options.magicCode
		self.__heartCode = options.heartCode
		self.__headformat = '<HLHHL'
		
	def receive(self):
		try:
			pdata = ''
			while self.__switch:
				LOG.debug('%s listening...'%self.__address)
				rdata = self.__sock.recv(1000)
				LOG.debug('receive raw_string from %s : '%self.__address, rdata)
				if rdata:
					self.__death = False
					pdata = self.parseHead('%s%s'%(pdata, rdata))
				else:
					LOG.info('%s disconnect...'%self.__address)
					self.exit()
		except:
			LOG.error('receive error : %s'%format_exc())
			LOG.error('%s receive error : %s'%(self.__address, 
											   format_exc()))
			self.exit()

	def parseHead(self, data):
		if len(data) >= 14:
			head = unpack(self.__headformat, data[:14])
			if head[0] + 2 <= len(data):
				mdata = data[ : head[0] + 2]
				data = data[head[0] + 2 : ]
				if head[1] == self.__magicCode:
					if head[3] != self.__heartCode:
						self.net_to_parse.send([head[0], head[3], mdata])
						stackless.schedule()
				else:
					LOG.error('receive FIFA package from %s : '%self.__address, mdata)
					self.exit()
				data = self.parseHead(data)
		return data

	def threadBroadcast(self):
		while self.__switch:
			try:
				rdata = self.broadcast.receive()
				if self.__switch:
					self.__sock.sendall(rdata)
					LOG.debug('send to %s : '%self.__address, rdata)
				else:
					LOG.info('send to %s failed !'%self.__address)
			except Exception:
				LOG.error('%s broadcast error : '%self.__address)
				LOG.error('%s\n%s'%(format_exc(),
									rdata.__repr__()))
				self.exit()

	def chkHeart(self, gapTime):
		while (not self.__death) and self.__switch:
			self.__death = True
			Net.SLEEP.delay_caller(gapTime)
		if self.__switch:
			LOG.error('%s heart time out !'%self.__address)
			self.exit()
	
	def reHeart(self):
		pass
				
	def exit(self):
		pass
		