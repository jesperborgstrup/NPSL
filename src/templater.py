import context, sys, os.path
from tools.templater.java import files
from optparse import OptionParser

class ArgumentError(Exception):
    def __init__(self, err):
        self.err = err
    def __repr__(self):
        return "ArgumentError: %s" % self.err
    def __str__(self):
        return self.err

def makeOptionParser():
    parser = OptionParser()
    parser.add_option("-i", "--in-folder", dest="inputfolder",
                      help="Read source files from FOLDER", metavar="FOLDER")
    parser.add_option("-l", "--language", dest="language",
                      help="Set language")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="Print output during processing")
    
    return parser

languages = {"java": "tools.templater.java",
             "python": "tools.templater.python"}

class Options:
    infolder = None
    verbose = False
    languagemodule = None


def process_options(optargs):
    options, args = optargs
    
    result = Options()
    result.context = context.Context()

    # Check verbose
    if options.verbose is not None:
        result.verbose = True
    
    # Check output folder
    if options.inputfolder is not None:
        folder = os.path.abspath( options.inputfolder )
        if os.path.exists( folder ) and not os.path.isdir( folder ):
            raise ArgumentError( "%s is not a folder!" % options.inputfolder )
        else:
            result.infolder = folder
            
    # Check language
    if options.language is None:
        raise ArgumentError( "You must specifiy a language with the -l parameter!\r\n" \
                             "Possible languages are:\r\n" + "\r\n".join(languages.__all__.keys()))
    else:
        lang = options.language.lower()
        if not languages.has_key( lang ):
            raise ArgumentError( "%s is not a valid language!\r\n" % options.language + \
                                 "Possible languages are:\r\n" + "\r\n".join(languages.keys()))
        else:
            if lang == "java":
                from tools.templater.java import Java
                return Java(result)
            elif lang == "python":
                from tools.templater.python import Python
                return Python(result)
            
if __name__ == "__main__":
    optionparser = makeOptionParser()
    if len( sys.argv ) <= 1:
        optionparser.print_help()
        sys.exit(-1)
        
    try:
        o = process_options( optionparser.parse_args() )
        o.run()
    except ArgumentError, err:
        sys.stderr.write( str( err ) + "\r\n" )
        sys.exit(-1)
