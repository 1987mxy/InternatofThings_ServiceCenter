'''
Created on 2012-9-2

@author: XPMUser
'''

import sqlite3

if __name__ == '__main__':
	db = sqlite3.connect('Data.dat')
	cur = db.execute('select * from datapackage')
	print cur.fetchall()
	print cur.description