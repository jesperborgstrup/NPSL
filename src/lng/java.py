from outputlanguage import OutputLanguage, Casing
import os.path

def datatype(str):
    if str == 'byte':
        return "DataType.Byte"
    elif str == 'int':
        return "DataType.Int"
    elif str == 'ints':
        return "DataType.IntList"
    elif str == 'float':
        return "DataType.Float"
    elif str == 'string':
        return "DataType.String"
    elif str == 'strings':
        return "DataType.StringList"
    elif str == 'binary':
        return "DataType.Binary"
    else:
        raise RuntimeError( 'Unknown datatype: ' % str )

class LanguageJava(OutputLanguage):
    
    def __init__(self):
        OutputLanguage.__init__(self, 
                                name="Java", 
                                folder="java",
                                casing=Casing.CAMEL_CASING,
                                filters=[("datatype", datatype),
                                         ]
                                )
        
    def set_options(self, options, cmd_optargs):
        cmd_options, cmd_args = cmd_optargs
        
        settings = options.input["settings"]
        
        if not settings.has_key("java_package"):
            raise RuntimeError("No java package specified. Specify a package with the 'javapackage' setting")
        
        options.input["java_package_root"] = settings["java_package"] + ".npsl"
        
        OutputLanguage.set_options(self, options, cmd_optargs)

    def parse_file(self, template):
        m = template.module.__dict__

        if not m.has_key("java_subpackage"):
            return None
        subpackage = m["java_subpackage"]
        javapackage = self.options.input["java_package_root"] + "." + subpackage
        
        filename = os.path.basename(m["__name__"])
        output_dest = "src/" + javapackage.replace(".", "/") + "/" + filename
        
        self.options.input["java_package"] = javapackage
#        print self.options.input
#        import sys
#        sys.exit()
        
        return (output_dest, template.render(self.options.input))

    def comment(self, comment):
        lines = comment.splitlines()
        lines = map(lambda line: " * " + line, lines)
        return "/*\r\n" + "\r\n".join(lines) + "\r\n */\r\n"
