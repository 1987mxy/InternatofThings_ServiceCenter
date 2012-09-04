'''
Created on 2012-9-4

@author: XPMUser
'''
import threading
from time import sleep
import Config,Log,Tools

logger = Log.Log()

def t1():
	logger.info('t1 start long sleep!')
	sleep(15)
	logger.info('t1 wake up!!')
	pass

def t2():
	for i in range(10):
		logger.info(i)
		sleep(2)
	pass

if __name__ == '__main__':
	tt1 = threading.Thread(target=t1)
	tt2 = threading.Thread(target=t2)
	logger.info('ready go!!!')
	tt1.start()
	tt2.start()