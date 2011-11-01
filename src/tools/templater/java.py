files = [ ('client', ['client/Client.java',
                      'client/ConnectException.java'
                      ]), 
          ('common', ['common/ByteArray.java',
                      'common/Connection.java',
                      'common/DataType.java',
                      'common/DisconnectReason.java',
                      'common/Logger.java',
                      'common/Message.java',
                      'common/MessageFactory.java',
                      'common/MessageHandler.java',
                      'common/MessageType.java',
                      'common/Parameter.java',
                      'common/SocketThread.java'
                      ]),
          ('server', ['server/ClientThread.java',
                      'server/Server.java'
                      ]) ]

import os.path

class Java:
    def __init__(self, options):
        self.options = options
        
    def run(self):
        for package, filenames in files:
            for filename in filenames:
                absolute = os.path.join( self.options.infolder, filename )
                if not os.path.exists( absolute ):
                    continue
                
                f = open(absolute, "r")
                source = f.read()
                f.close()
                
                source = source[source.index("package")+8:]
                packagename = source[:source.index(";")]
                npslpackagename = packagename[:packagename.index("npsl")+4]

                source = source[source.index("\n")+1:]
                source = source.replace(npslpackagename, "{{ java_package_root }}")
                
                setupline = "{%% set package, java_subpackage = \"%s\", \"%s\" %%}" % (package,package)
                packageline = "package {{ java_package }};"
                
                prelude = setupline + "\r\n" + packageline + "\r\n"
                
                template = prelude + source
                templatefilename = os.path.join( self.options.context.templates_folder,
                                                 "java",
                                                 filename )
                
                if not os.path.exists( templatefilename ):
                    print "Warning! Template file %s does not exist. Skipping..." % templatefilename
                    continue
                
                f = open( templatefilename, "w" )
                f.write( template )
                f.close()
                
                if self.options.verbose:
                    print "Wrote %s (%d bytes)" % (filename, len( template ) )