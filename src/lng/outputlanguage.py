from glob import glob
from jinja2 import Environment, FileSystemLoader, PrefixLoader
import sys, os.path, fnmatch

class Casing:
	CAMEL_CASING = 1
	UNDERSCORE = 2
	
	@staticmethod
	def case(casing, name):
		if casing == Casing.CAMEL_CASING:
#			return undefined
			return name
		elif casing == Casing.UNDERSCORE:
			return name
	
class OutputLanguage:
	name = ""
	folder = ""
	casing = -1
	filters = []
	options = None
	template_env = None
	
	def __init__(self, name, folder, casing, filters=[]):
		self.name = name
		self.folder = folder
		self.casing = casing
		self.filters = filters
		self.filters.append(("direction", OutputLanguage.filter_direction))
		
	def set_options(self, options, cmd_optargs):
		self.options = options

	@staticmethod
	def filter_direction(items, direction):
		return filter(lambda i: i["direction"] == direction, items)

	def get_template_environment(self):
		loader = FileSystemLoader( self.get_templates_folder() )

		env = Environment(loader=loader)
		env.filters.update(self.filters)
		return env
		
	def get_templates_folder(self):
		return os.path.abspath( self.options.context.templates_folder + '/' + self.folder )

	# To be overridden by implementing OutputLanguage 
	def parse_file(self, template):
		return None
	
	# To be overridden by implementing OutputLanguage 
	def comment(self, lines):
		return ""

	def get_files(self, target_packages):
		self.template_env = self.get_template_environment()
		files = []
		rootfolder = self.get_templates_folder()
		for root, dirnames, filenames in os.walk(rootfolder):
			for file in fnmatch.filter(filenames, '*.*'):
				filename = os.path.join(root, file)
				rel_filename = os.path.relpath(filename, self.get_templates_folder())
				
				template = self.template_env.get_template( rel_filename )
				
				m = template.module.__dict__
		
				package =  m["package"] if m.has_key("package") else None
				if package is None or not package in target_packages:
					continue
				
				parse_file_result = self.parse_file(template)
				if parse_file_result is None:
					continue
				
				yield parse_file_result
					
	def __repr__(self):
		return "OutputLanguage %s" % self.name
	
