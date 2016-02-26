# -*- coding: utf-8 -*-

def create_table(name,struct,cur):
	cur.execute('DROP TABLE IF EXISTS %s' % name)		
	cur.execute('CREATE TABLE %s (%s)' % (name, struct))

def create_index(table,field,cur):
	cur.execute('CREATE INDEX index_%s_%s ON %s (%s)' % (table,field,table,field))
