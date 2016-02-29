# -*- coding: utf-8 -*-

def create_table(name,struct,cur):
	cur.execute('DROP TABLE IF EXISTS %s' % name)		
	cur.execute('CREATE TABLE %s (%s)' % (name, struct))

def create_index(table,field,cur):
	cur.execute('CREATE INDEX index_%s_%s ON %s (%s)' % (table,field,table,field))

# functions
def safe_str(name):
	if name:
		return name.replace('a,','').replace('\\0','').strip()
	return 'NO NAME'

def safe_icon(name):
	return safe_str(name.lower().replace("branchsys.icon.", "").replace("branchsys2.icon2.", "").replace("branchsys2.icon.", "").replace("br_cashtex.item.", "").replace("icon.", "").replace("br_cashtex.item.", "").replace("branchsys.", "").replace("branchsys2.", "").replace('icon.',''))

def save_icon(name):
	f_name = "icons/"+name+".png"
	if os.path.isfile(f_name): 
		return
	f = urllib.request.urlopen('http://l2kc.ru/icons/%s_0.png' % name)
	data = f.read()
	with open(f_name, "wb") as code:
		code.write(data)
	pass

def parse_group_icon(e,cur,sql = 'UPDATE items SET icon=? WHERE id= ?',struct = {'id':1,'icon': -1}):
	if struct['icon'] == -1:
		struct['icon'] = e.index('icon[0]');
	icon = safe_icon(e[struct['icon']])
	cur.execute(sql,(icon, e[struct['id']]))	

def convert_dat_files():
	chronicle = 'Interlude'
	current_dir = os.getcwd()
	dat_files = glob.glob("utils/dat/*.dat")

	for f in dat_files:
		f_name = os.path.splitext(basename(f))[0]
		ddf_file = '%s/utils/l2asm-disasm/DAT_defs/%s/%s.ddf' % (current_dir,chronicle,f_name)
		ddf_file_new = '%s/utils/l2asm-disasm/DAT_defs/%s/%s.ddf' % (current_dir,chronicle,f_name+'-new')
		decode_file = '%s/dat/%s.dat' % (current_dir,f_name)
		clear_file = '%s/dat/%s.txt' % (current_dir,f_name.lower())
		cmd_decode = "wine utils/l2encdec/l2encdec_old.exe -s %s/%s %s" % (current_dir,f,decode_file)
		cmd_format = 'wine utils/l2asm-disasm/l2disasm.exe -d %s -e %s %s %s' % (ddf_file, ddf_file_new, decode_file, clear_file)
		os.system(cmd_decode)
		os.system(cmd_format)
		os.remove(decode_file)
