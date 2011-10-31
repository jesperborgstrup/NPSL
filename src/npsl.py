from optparse import OptionParser
from npslparser import npsl
from output import Output
from context import Context
import os.path, sys, languages

class ArgumentError(Exception):
	def __init__(self, err):
		self.err = err
	def __repr__(self):
		return "ArgumentError: %s" % self.err
	def __str__(self):
		return self.err

class Options:
	input = {}
	input_file = sys.stdin
	client = None
	output_folder = "out"
	output_language = None
	verbose = False
	context = None
	extra = {}
	
	def __init__(self):
		
		pass
	def __repr__(self):
		return "\r\n".join( [ repr( self.client ), repr( self.input ) ] )
	def __str__(self):
		return "\r\n".join( [ str( self.client ), str( self.input ) ] )
	

def makeOptionParser():
	parser = OptionParser()
	parser.add_option("-i", "--in-file", dest="filename",
					  help="Read NPSL from FILE (if not specified, standard input will be used.)",
					  metavar="FILE")
	parser.add_option("-c", "--client", dest="client", action="store_true",
					  help="Output client")
	parser.add_option("-s", "--server", dest="client", action="store_false",
					  help="Output server")
	parser.add_option("-o", "--out-folder", dest="outputfolder",
					  help="Output code files to FOLDER (defaults to 'out')", metavar="FOLDER")
	parser.add_option("-l", "--out-language", dest="language",
					  help="Output files in language LANG", metavar="LANG")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
					  help="Print output during processing")
	parser.add_option("--java-package", dest="java_package", metavar="PACKAGE",
					  help="Sets Java packages to PACKAGE.npsl")
	
	return parser

default_settings = {"java_package": "com.example",
					"ignore_unknown_messages": True}

def get_default_settings(settings):
	# Prefix with 'setting_'
	result = {}
	for (setting, value) in default_settings.iteritems():
		prefixed_setting = "setting_%s" % setting
		result[prefixed_setting] = value if not settings.has_key(setting) else settings[setting]
	return result

def process_options(optargs):
	options, args = optargs
	result = Options()
	result.context = Context()

	# Check verbose
	if options.verbose is not None:
		result.verbose = True
	
	# Check input file
	if options.filename is not None:
		file = os.path.abspath( options.filename )
		if os.path.exists( file ) and os.path.isfile( file ):
			result.input_file = open( file )
		else:
			raise ArgumentError( "File %s doesn't exist!" % options.filename )
			
	# Check client or server output
	if options.client is None:
		raise ArgumentError( "You must select client (-c) or server (-s)!" )
	else:
		result.client = options.client
		
	# Check output folder
	if options.outputfolder is not None:
		folder = os.path.abspath( options.outputfolder )
		if os.path.exists( folder ) and not os.path.isdir( folder ):
			raise ArgumentError( "%s is not a folder!" % options.outputfolder )
		else:
			result.output_folder = folder
			
	# Check language
	if options.language is None:
		raise ArgumentError( "You must specifiy a language with the -l parameter!\r\n" \
							 "Possible languages are:\r\n" + "\r\n".join(languages.__all__.keys()))
	else:
		lang = options.language.lower()
		if not languages.__all__.has_key( lang ):
			raise ArgumentError( "%s is not a valid language!\r\n" % options.language + \
								 "Possible languages are:\r\n" + "\r\n".join(languages.__all__.keys()))
		else:
			result.language = languages.__all__[lang]
			
	# Read NPSL
	result.input.update( npsl.parseString( "".join(result.input_file.readlines()) )[0] )
	
	result.input.update( get_default_settings( result.input["settings"] ) )
	
	try:
		result.language.set_options(result, optargs)
	except RuntimeError, err:
		raise ArgumentError(err.message)

	# Make output folder if it doesn't exist
	if not os.path.exists( result.output_folder ):
		os.mkdir( result.output_folder )
	return result

if __name__ == "__main__":
	optionparser = makeOptionParser()
	if len( sys.argv ) <= 1:
		optionparser.print_help()
		sys.exit(-1)
		
	try:
		o = Output( process_options( optionparser.parse_args() ) )
		o.run()
	except ArgumentError, err:
		sys.stderr.write( str( err ) + "\r\n" )
		sys.exit(-1)
		
