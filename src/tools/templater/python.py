files = [ ('client', ['client.py'
                      ]), 
          ('common', ['__init__.py',
                      'datatypes.py',
                      'message.py',
                      'messagefactory.py',
                      'messagehandler.py',
                      'messagetype.py',
                      'socketthread.py'
                      ]),
          ('server', ['clientthread.py',
                      'server.py'
                      ]) ]

import os.path

class Python:
    def __init__(self, options):
        self.options = options
        
    def run(self):
        for package, filenames in files:
            for filename in filenames:
                absolute = os.path.join( self.options.infolder, filename )
                if not os.path.exists( absolute ):
                    continue
                
                f = open(absolute, "r")
                source = f.readlines()
                f.close()

                # Remove lines with comments and empty lines first
                firstline = source[0].strip()
                while firstline.startswith("#") or firstline == "":
                    source = source[1:]
                    if len( source ) == 0:
                        break
                    firstline = source[0].strip()
                    
                source = "".join(source)
                
                setupline = "{%% set output_dest, package = \"%s\", \"%s\" %%}" % (filename, package)

                prelude = setupline + "\r\n"
                
                template = prelude + source
                templatefilename = os.path.join( self.options.context.templates_folder,
                                                 "python",
                                                 filename )
                
                if not os.path.exists( templatefilename ):
                    print "Warning! Template file %s does not exist. Skipping..." % templatefilename
                    continue
                
                f = open( templatefilename, "w" )
                f.write( template )
                f.close()
                
                if self.options.verbose:
                    print "Wrote %s (%d bytes)" % (filename, len( template ) )