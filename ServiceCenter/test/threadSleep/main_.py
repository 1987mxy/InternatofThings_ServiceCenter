'''
Created on 2012-9-4

@author: XPMUser
'''
import threading
from time import sleep
import Config,Log,Tools

logger = Log.Log()

cond = threading.Condition()

def t1():
	global cond
	logger.info('t1 start!')
	sleep(5)
	if cond.acquire():
		logger.info('t1 get lock!')
	else:
		logger.info('t1 do not get lock!')
	logger.info('t1 notify!!')
	cond.notify()
	logger.info('t1 wait!!')
	cond.wait()
	logger.info('t1 receive notify!!')

def t2():
	global cond
	logger.info('t2 start!')
	sleep(3)
	if cond.acquire():
		logger.info('t2 get lock!')
	else:
		logger.info('t2 do not get lock!')
	logger.info('t2 sleep 10 second!!')
	sleep(10)
	logger.info('t2 notify!!')
	cond.notify()
	logger.info('t2 wait!!')
	cond.wait()
	logger.info('t2 receive notify!!')

if __name__ == '__main__':
	tt1 = threading.Thread(target=t1)
	tt2 = threading.Thread(target=t2)
	logger.info('ready go!!!')
	tt1.start()
	tt2.start()