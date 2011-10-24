import os.path, time

class Output:
	options = None
	prologue_comment = ""
	
	packages = ["common"]
	
	def __init__(self, options):
		self.options = options
		
		# Read comment file
		comment_file = open( os.path.join( options.context.templates_folder, "common", "comment.txt" ), 'r' )
		self.prologue_comment = comment_file.read()
		comment_file.close()
		
		if self.options.client:
			self.packages.append("client")
		else:
			self.packages.append("server")
		
	def run(self):
		if self.options.verbose:
			print "Read NPSL source from file '%s'" % self.options.input_file.name
			print "Output type: %s" % ("Client" if self.options.client else "Server")
			print "Output language: %s" % self.options.language.name
			print "Output to folder '%s'" % self.options.output_folder
			
		for output_dest, contents in self.options.language.get_files(self.packages):
			self.write_file(output_dest, contents)

	def write_file(self, output_dest, contents):
		if self.options.verbose:
			print "Processing file %s... " % output_dest,

		output_filename = os.path.join(self.options.output_folder, output_dest)
		output_dir = os.path.dirname( output_filename )
		if not os.path.exists( output_dir ):
			os.makedirs( output_dir )

		output_file = open( output_filename, "w" )
		self.write_prologue_comment( output_file, output_dest )
		output_file.write( contents )
		output_file.close()
		if self.options.verbose:
			print "Done!"
			
	def write_prologue_comment(self, output_file, output_dest):
		comment = self.options.language.comment( self.prologue_comment )
		comment = comment.replace( "%filename%", output_dest )
		comment = comment.replace( "%timestamp%", time.strftime( "%d/%m/%Y %H:%i:%s" ) )
		output_file.write( comment )
