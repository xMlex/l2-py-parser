#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os.path, sqlite3 as sql
import urllib.request, urllib.parse, urllib.error

# functions
def safe_str(name):
	if name:
		return name.replace('a,','').replace('\\0','').strip()
	return 'NO NAME'

def safe_icon(name):
	return safe_str(name.lower().replace("branchsys.icon.", "").replace("branchsys2.icon2.", "").replace("branchsys2.icon.", "").replace("br_cashtex.item.", "").replace("icon.", "").replace("br_cashtex.item.", "").replace("branchsys.", "").replace("branchsys2.", ""))

def save_icon(name):
	f_name = "icons/"+name+".png"
	if os.path.isfile(f_name): 
		return
	f = urllib.request.urlopen('http://l2kc.ru/icons/%s_0.png' % name)
	data = f.read()
	with open(f_name, "wb") as code:
		code.write(data)
	pass

def parse_group_icon(file_name,struct,sql):
	i = 0;
	f = open(file_name, 'r')
	for l in f:
		e = l.split("\t")
		if struct['icon'] == -1:
			struct['icon'] = e.index('icon[0]');
		i += 1
		icon = safe_icon(e[struct['icon']])
		cur.execute(update_item_icon,(icon, e[struct['id']]))	
	f.close()
	return i

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

	# Items name
	sys.stdout.write('Items ... ')
	cur.execute('DROP TABLE IF EXISTS items')
	cur.execute('CREATE TABLE items (id integer, name string, add_name string, description string, icon string)')

	item_struc = {'id': 0, 'name': 1, 'add_name': 2, 'descr': 3}
	insert_item = 'INSERT INTO items VALUES(?,?,?,?,?)'

	f = open('dat/itemname-e.txt', 'r')
	for l in f:
		e = l.split("\t")
		cur.execute(insert_item,(e[item_struc['id']],e[item_struc['name']],e[item_struc['add_name']],e[item_struc['descr']],''))
	f.close()
	cur.execute('CREATE INDEX index_items_id ON items (id)')
	print('%s' % cur.execute('SELECT COUNT(*) FROM items').fetchone())

	# Npc names 
	sys.stdout.write('Npc ... ')
	cur.execute('DROP TABLE IF EXISTS npc')		
	cur.execute('CREATE TABLE npc (id integer, name string, description string)')
	insert = 'INSERT INTO npc VALUES(?,?,?)'

	struct = {'id':0,'name':1,'descr':2}
	f = open('dat/NpcName-e.txt', 'r')
	for l in f:
		e = l.split("\t")
		name = safe_str(e[struct['name']])
		descr = safe_str(e[struct['descr']])
		cur.execute(insert,(e[struct['id']],name,descr))
	cur.execute('CREATE INDEX index_npc_id ON npc (id)')
	print('%s' % cur.execute('SELECT COUNT(*) FROM npc').fetchone())

	# Armor Group
	sys.stdout.write('Armor Group ... ')
	update_item_icon = 'UPDATE items SET icon=? WHERE id= ?'

	struct = {'id':1,'icon': -1}
	i = parse_group_icon('dat/armorgrp.txt',struct,update_item_icon)
	print('%s' % i)

	# Etc Item Group
	sys.stdout.write('Etc Item Group ... ')
	i = parse_group_icon('dat/etcitemgrp.txt',struct,update_item_icon)
	print('%s' % i)

	# Weapon Group
	sys.stdout.write('Weapon Group ... ')
	i = parse_group_icon('dat/weapongrp.txt',struct,update_item_icon)
	print('%s' % i)

	print('All files parse')
except BaseException as e:
	print("Error %s:" % e.args[0])
	sys.exit(1)
finally:
  if con:
    con.close()


