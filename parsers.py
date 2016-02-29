# -*- coding: utf-8 -*-
import sys
from helper import *

files_structs = {
		'itemname-e': {'insert': 'INSERT INTO items VALUES(?,?,?,?,?)', 'struct': {'id': 0, 'name': 1, 'add_name': 2, 'descr': 3},'create_index':{'table': 'items','filed':'id'}},
		'npcname-e': {'insert': 'INSERT INTO npc VALUES(?,?,?)', 'struct': {'id':0,'name':1,'descr':2},'create_index':{'table': 'npc','filed':'id'}},
		'actionname-e': {'insert': 'INSERT INTO actions VALUES(?,?,?,?,?,?)', 'struct': {'id':1,'category':3, 'name': 777, 'icon': 778,'descr': 779,'skill': 780}},
		'armorgrp':{'insert': 'UPDATE items SET icon=? WHERE id= ?','struct': {'id':1,'icon': -1}},
		'etcitemgrp':{'insert': 'UPDATE items SET icon=? WHERE id= ?','struct': {'id':1,'icon': -1}},
		'weapongrp':{'insert': 'UPDATE items SET icon=? WHERE id= ?','struct': {'id':1,'icon': -1}},
		'castlename-e':{'insert': 'INSERT INTO castles VALUES(?,?,?,?)','struct': {'id':2,'name':3,'location':4,'desc':5}},
	}

def decoratorL2FileIteration(file_name):
	def wrap(fn):
		def wrapped_f(cur, *args):
			sys.stdout.write('%s ... ' % file_name)
			f = open('dat/%s.txt' % file_name, 'r')
			i = 0;
			for l in f:
				i += 1				
				e = l.split("\t")
				fn(e, files_structs[file_name]['insert'], files_structs[file_name]['struct'], cur)
			f.close()
			if 'create_index' in files_structs[file_name]:
				create_index(files_structs[file_name]['create_index']['table'], files_structs[file_name]['create_index']['filed'], cur)
			print('%s' % i)
		return wrapped_f
	return wrap

@decoratorL2FileIteration('itemname-e')
def parser_1items(e, insert_query, struct, cur):
	cur.execute(insert_query,(e[struct['id']],e[struct['name']],e[struct['add_name']],safe_str(e[struct['descr']]),''))

@decoratorL2FileIteration('npcname-e')
def parser_2npc(e, insert_query, struct, cur):
	name = safe_str(e[struct['name']])
	descr = safe_str(e[struct['descr']])
	cur.execute(insert_query,(e[struct['id']],name,descr))

@decoratorL2FileIteration('actionname-e')
def parser_actions(e, insert_query, struct, cur):
	icon = safe_icon(e[struct['icon']])
	name = safe_str(e[struct['name']])
	descr = safe_str(e[struct['descr']])
	cur.execute(insert_query,(e[struct['id']],e[struct['category']],name,descr,icon,e[struct['skill']]))

@decoratorL2FileIteration('armorgrp')
def parser_armorgrp(e, insert_query, struct, cur):	
	parse_group_icon(e, cur, insert_query, struct)

@decoratorL2FileIteration('etcitemgrp')
def parser_etcitemgrp(e, insert_query, struct, cur):	
	parse_group_icon(e, cur, insert_query, struct)

@decoratorL2FileIteration('weapongrp')
def parser_weapongrp(e, insert_query, struct, cur):	
	parse_group_icon(e, cur, insert_query, struct)

@decoratorL2FileIteration('castlename-e')
def parser_castlename(e, insert_query, struct, cur):	
	name = safe_str(e[struct['name']])
	location = safe_str(e[struct['location']])
	desc = safe_str(e[struct['desc']])
	cur.execute(insert_query,(e[struct['id']],name,location,desc))












