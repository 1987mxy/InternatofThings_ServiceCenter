#coding=UTF-8

import logging
from sys import stdout
from os import path, mkdir

from Config import PRINT_RUNLOG, PRINT_LOG, Status

class Log(object):
	'''
	日志(单例模式)
	'''
	__me = None
	
	def __init__(self):
#		runlog
		self.logger = logging.getLogger('runlog')
		self.logger.setLevel(logging.DEBUG)
		lpath = pathRule('run')
		logfile = logging.FileHandler(lpath, "w")
		logfile.setLevel(logging.DEBUG)
		fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
		logfile.setFormatter(fmt)
		self.logger.addHandler(logfile)
		if PRINT_RUNLOG and PRINT_LOG:
			display = logging.StreamHandler(stdout)
			display.setLevel(logging.INFO)
			self.logger.addHandler(display)  #print to screen
#		erroself.logger
		lpath = pathRule('error')
		logfile = logging.FileHandler(lpath, "w")
		logfile.setLevel(logging.ERROR)
		logfile.setFormatter(fmt)
		self.logger.addHandler(logfile)
	
	@staticmethod
	def instance():
		if Log.__me == None:
			Log.__me = Log()
		return Log.__me
	
	def formatHex(self, string):
		hexlist = []
		for char in string:
			hexlist.append( '%02x ' % ord( char ) )
		return str.join( hexlist )
	
	def critical(self, string, argument = None):   #high
		if  Status == 'release':
			if argument:
				self.logger.critical('%s%s'%(string, argument.__len__()))
			else:
				self.logger.critical(string)
		elif  Status == 'debug':
			if argument:
				self.logger.critical('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.critical(string)
	
	def error(self, string, argument = None):
		if Status == 'release':
			if argument:
				self.logger.error('%s%s'%(string, argument.__len__()))
			else:
				self.logger.error(string)
		elif Status == 'debug':
			if argument:
				self.logger.error('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.error(string)

	def warning(self, string, argument = None):
		if Status == 'release':
			if argument:
				self.logger.warning('%s%s'%(string, argument.__len__()))
			else:
				self.logger.warning(string)
		elif Status == 'debug':
			if argument:
				self.logger.warning('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.warning(string)

	def info(self, string, argument = None):
		if Status == 'release':
			if argument:
				self.logger.info('%s%s'%(string, argument.__len__()))
			else:
				self.logger.info(string)
		elif Status == 'debug':
			if argument:
				self.logger.info('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.info(string)
	
	def debug(self, string, argument = None):  #low
		if Status == 'release':
			if argument:
				self.logger.debug('%s%s'%(string, argument.__len__()))
			else:
				self.logger.debug(string)
		elif Status == 'debug':
			if argument:
				self.logger.debug('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.debug(string)
				
def pathRule(logtype, filetype = 'log'):
	from time import strftime,localtime
	time = strftime('%Y-%m-%d %H_%M_%S',localtime())
	if not path.exists("log"):
		mkdir("log")
	return r'./log/%s_%s.%s'%(time, logtype, filetype)