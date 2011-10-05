from glob import glob
from jinja2 import Environment, FileSystemLoader, PrefixLoader
import sys, os.path

class Casing:
	CAMEL_CASING = 1
	UNDERSCORE = 2
	
	@staticmethod
	def case(casing, name):
		if casing == CAMEL_CASING:
			return undefined
		elif casing == UNDERSCORE:
			return name
	
class OutputLanguage:
	name = ""
	folder = ""
	casing = -1
	filters = []
	context = None
	
	def __init__(self, name, folder, casing, filters=[]):
		self.name = name
		self.folder = folder
		self.casing = casing
		self.filters = filters
		self.filters.append(("direction", OutputLanguage.filter_direction))

	@staticmethod
	def filter_direction(items, direction):
		return filter(lambda i: i["direction"] == direction, items)

	def get_template_environment(self):
		loader = PrefixLoader({
				"common": FileSystemLoader( self.get_common_templates_folder() ),
				"client": FileSystemLoader( self.get_client_templates_folder() ),
				"server": FileSystemLoader( self.get_server_templates_folder() )
				})
		env = Environment(loader=loader)
		for name, func in self.filters:
			env.filters[name] = func
		return env
		
		
	def get_templates_folder(self, sub=""):
		return os.path.abspath( self.context.templates_folder + '/' + self.folder + sub )

	def get_common_templates_folder(self):
		return self.get_templates_folder('/common')
		
	def get_client_templates_folder(self):
		return self.get_templates_folder('/client')
		
	def get_server_templates_folder(self):
		return self.get_templates_folder('/server')
		
	def get_filenames(self, subfolder):
		return map( lambda p: os.path.relpath(p, self.get_templates_folder()), glob( self.get_templates_folder() + '/%s/*.*' % subfolder ) )
		
	def get_filenames_common(self):
		return self.get_filenames('common')
		
	def get_filenames_client(self):
		return self.get_filenames('client')
		
	def get_filenames_server(self):
		return self.get_filenames('server')
		
	def __repr__(self):
		return "OutputLanguage %s" % self.name
	
