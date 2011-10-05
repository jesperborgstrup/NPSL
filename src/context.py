import os.path, sys

class Context:
	root_folder = ""
	templates_folder = ""
	src_folder = ""
	
	def __init__(self):
		self.src_folder       = os.path.dirname( sys.argv[0] )
		self.root_folder      = os.path.abspath( self.src_folder + '/..' )
		self.templates_folder = os.path.abspath( self.root_folder + '/templates' )
