import os
import jinja2

def apply_template(path, vars):
	loader = jinja2.FileSystemLoader( [ os.getcwd() ] )
	env = jinja2.Environment(loader=loader, extensions=['jinja2.ext.do'])
	env.line_statement_prefix = '@'
	
	return env.get_template(path).render(**vars)
