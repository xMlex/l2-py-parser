# -*- coding: utf-8 -*-

def decoratorFileIteration(file_name):
	def wrap(f):
		def wrapped_f(*args):
			f = open('dat/%s.txt' % file_name, 'r')
			for l in f:
				e = l.split("\t")
      	f(*args)
        return wrapped_f
    return wrap

@decoratorFileIteration("best file")
def parse_actions(line):
	print(line)

parse_actions()
