import os.path
from jinja2 import Environment, FileSystemLoader, PrefixLoader

class Output:
	options = None
	template_env = None
	
	def __init__(self, options):
		self.options = options
		self.template_env = options.language.get_template_environment()
		
	def run(self):
		import os.path, sys
		if self.options.verbose:
			print "Read NPSL source from file '%s'" % self.options.input_file.name
			print "Output type: %s" % ("Client" if self.options.client else "Server")
			print "Output language: %s" % self.options.language.name
			print "Output to folder '%s'" % self.options.output_folder
			
		input_files = self.options.language.get_filenames_common()
		if self.options.client:
			input_files.extend( self.options.language.get_filenames_client())
		else:
			input_files.extend( self.options.language.get_filenames_server())
				
		output_files = map( lambda f: os.path.abspath( self.options.output_folder + '/' + os.path.basename( f ) ), input_files )
		files = zip( input_files, output_files )
		
		[self.process_file(i,o) for (i,o) in files]

	def process_file(self, input_filename, output_filename):
		if self.options.verbose:
			print "Processing file %s... " % input_filename,

		template = self.template_env.get_template( input_filename )
		output = template.render( self.options.input )

		output_file = open( output_filename, "w" )
		output_file.write( output )
		output_file.close()
		if self.options.verbose:
			print "Done!"
