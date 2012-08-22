'''
Created on 2012-8-14

@author: Moxiaoyong
'''

import threading
import time.sleep

from traceback import format_exc
from struct import unpack

from lib.Log import LOG

class Service(object):
	'''
	服务抽象类
	'''

	def __init__(self, socket):
		'''
		构造函数
		'''
		if self.__class__ is Service:	#抽象类不能被实例化
			LOG.error('Net class dose not instantiation')
			raise 'Net class dose not instantiation'
		
		self.__sock = socket
		self.__switch = True
		self.__is_alive = True
		
		self.__magicCode = None
		self.__heartCode = None
		self.__headerStruct = None
		
	def config(self, config):
		self.__magicCode = config.magicCode
		self.__heartCode = config.heartCode
		self.__headerStruct = config.headerStruct
		
	def receive(self):
		try:
			pdata = ''
			while self.__switch:
				LOG.debug('%s listening...'%self.__address)
				rdata = self.__sock.recv(1000)
				LOG.debug('receive raw string from %s : '%self.__address, rdata)
				if rdata:
					self.__isAlive = False
					pdata = self.parseHeader('%s%s'%(pdata, rdata))
				else:
					LOG.info('%s disconnect...'%self.__address)
					self.exit()
		except:
			LOG.error('receive error : %s'%format_exc())
			LOG.error('%s receive error : %s'%(self.__address, 
											   format_exc()))
			self.exit()

	def parseHeader(self, data):
		if len(data) >= 8:
			head = unpack(self.__headStruct, data[:8])
			if head[1] != self.__magicCode:
				LOG.error('receive invalid package from %s : '%self.__address, data)
				self.exit()
			if head[0] + 2 <= len(data):
				mdata = data[ : head[0] + 2]
				data = data[head[0] + 2 : ]
				if head[2] != self.__heartCode:
					self.main([head[0], head[2], mdata])
				data = self.parseHead(data)
		return data

	def chkResp(self, gap_time):
		while self.__isAlive and self.__switch:
			self.__isAlive = True
			time.sleep( gap_time )
		if self.__switch:
			LOG.error('%s response time out !'%self.__address)
			self.exit()
			
	def send(self, data):
		self.__sock.sendall( data )
		
	def exit(self):
		self.__switch = False
		pass
		
	def submit(self, data):
		
		pass