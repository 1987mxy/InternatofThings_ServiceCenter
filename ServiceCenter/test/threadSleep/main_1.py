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
	cond.acquire()
	logger.info('t1 get lock!!')
	while True:
		logger.info('t1 wait!')
		cond.wait()
		logger.info('t1 receive notify!')

def t2():
	global cond
	sleep(2)
	cond.acquire()
	logger.info('t2 get lock!!')
	cond.notify()
	logger.info('t2 notify!!')
	cond.release()
	sleep(1)
	cond.acquire()
	logger.info('_t2 wait t3')
	sleep(5)
	logger.info('_t2 get lock!!')
	cond.notify()
	logger.info('_t2 notify!!')
	cond.release()
	
def t3():
	global cond
	sleep(5)
	cond.acquire()
	logger.info('t3 get lock!!')
	cond.notify()
	logger.info('t3 notify!!')
	cond.release()
	
	
if __name__ == '__main__':
	tt1 = threading.Thread(target=t1)
	tt2 = threading.Thread(target=t2)
	tt3 = threading.Thread(target=t3)
	logger.info('ready go!!!')
	tt1.start()
	tt2.start()
	tt3.start()