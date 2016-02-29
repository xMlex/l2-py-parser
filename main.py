#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os.path, types, sqlite3 as sql
import glob
from subprocess import call
from os.path import basename
import urllib.request, urllib.parse, urllib.error
from helper import *
import parsers

CONVERT_FILES = False

if __name__ == "__main__":
# Convert files
	if CONVERT_FILES:
		convert_dat_files()

# Create db file
	try:
		con = sql.connect('db.sqlite')
		cur = con.cursor()    
		cur.execute('SELECT SQLITE_VERSION()')  
		print("SQLite version: %s" % cur.fetchone())

		cur.execute("PRAGMA synchronous=OFF")
		cur.execute("PRAGMA count_changes=OFF")
		cur.execute("PRAGMA journal_mode=MEMORY")
		cur.execute("PRAGMA temp_store=MEMORY")

		create_table('items', 'id integer, name string, add_name string, description string, icon string', cur)
		create_table('npc', 'id integer, name string, description string', cur)
		create_table('actions', 'id integer,category integer, name string, description string, icon string, skill string', cur)
		create_table('castles', 'id integer, name string, location string, description string', cur)
		
	#Run all parser in parsers
		for i in dir(parsers): 
			if i.startswith('parser_'):
				getattr(parsers, i)(cur=cur)
		con.commit()
		print('All files parsed')
	except BaseException as e:
		print("Error: %s" % e)
		sys.exit(1)
	finally:
		if con:
			con.close()


