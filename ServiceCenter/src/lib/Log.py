#coding=UTF-8

import logging
from sys import stdout
from os import path,mkdir

from lib import Config

LOG = None

class mylog(object):
	def __init__(self, logger):
		self.logger = logger
	
	def formatHex(self, string):
		hexlist = []
		for s in string:
			hexlist.append('%02x '%ord(s))
		return ''.join(hexlist)
	
	def critical(self, string, argument = None):   #high
		if  Config.Status == 'release':
			if argument:
				self.logger.critical('%s%s'%(string, argument.__len__()))
			else:
				self.logger.critical(string)
		elif  Config.Status == 'debug':
			if argument:
				self.logger.critical('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.critical(string)
	
	def error(self, string, argument = None):
		if Config.Status == 'release':
			if argument:
				self.logger.error('%s%s'%(string, argument.__len__()))
			else:
				self.logger.error(string)
		elif Config.Status == 'debug':
			if argument:
				self.logger.error('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.error(string)

	def warning(self, string, argument = None):
		if Config.Status == 'release':
			if argument:
				self.logger.warning('%s%s'%(string, argument.__len__()))
			else:
				self.logger.warning(string)
		elif Config.Status == 'debug':
			if argument:
				self.logger.warning('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.warning(string)

	def info(self, string, argument = None):
		if Config.Status == 'release':
			if argument:
				self.logger.info('%s%s'%(string, argument.__len__()))
			else:
				self.logger.info(string)
		elif Config.Status == 'debug':
			if argument:
				self.logger.info('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.info(string)
	
	def debug(self, string, argument = None):  #low
		if Config.Status == 'release':
			if argument:
				self.logger.debug('%s%s'%(string, argument.__len__()))
			else:
				self.logger.debug(string)
		elif Config.Status == 'debug':
			if argument:
				self.logger.debug('%s%s'%(string, self.formatHex(argument)))
			else:
				self.logger.debug(string)
				
def _pathrule(logtype, filetype = 'log'):
	from time import strftime,localtime
	time = strftime('%Y-%m-%d %H_%M_%S',localtime())
	if not path.exists("log"):
		mkdir("log")
	return r'./log/%s_%s.%s'%(time, logtype, filetype)
	
def run_log():
#	runlog
	global LOG
	rlog = logging.getLogger('runlog')
	rlog.setLevel(logging.DEBUG)
	lpath = _pathrule('run')
	logfile = logging.FileHandler(lpath, "w")
	logfile.setLevel(logging.DEBUG)
	fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	logfile.setFormatter(fmt)
	rlog.addHandler(logfile)
	if Config.PRINT_RUNLOG and Config.PRINT_LOG:
		display = logging.StreamHandler(stdout)
		display.setLevel(logging.INFO)
		rlog.addHandler(display)  #print to screen
#	errorlog
	lpath = _pathrule('error')
	logfile = logging.FileHandler(lpath, "w")
	logfile.setLevel(logging.ERROR)
	logfile.setFormatter(fmt)
	rlog.addHandler(logfile)
	LOG = mylog(rlog)
	#print LOG

if LOG == None:
	run_log()