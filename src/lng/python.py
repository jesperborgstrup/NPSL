from outputlanguage import OutputLanguage, Casing

def datatype(str):
    if str == 'byte':
        return "DataTypes.Byte"
    elif str == 'int':
        return "DataTypes.Int"
    elif str == 'ints':
        return "DataTypes.IntList"
    elif str == 'float':
        return "DataTypes.Float"
    elif str == 'string':
        return "DataTypes.String"
    elif str == 'strings':
        return "DataTypes.StringList"
    elif str == 'binary':
        return "DataTypes.Binary"
    else:
        raise RuntimeError( 'Unknown datatype: ' % str )
    
class LanguagePython(OutputLanguage):
    
    def __init__(self):
        OutputLanguage.__init__(self, 
                                name="Python", 
                                folder="python",
                                casing=Casing.UNDERSCORE,
                                filters=[("datatype", datatype),
                                         ]
                                )
        
    def parse_file(self, template):
        m = template.module.__dict__
        
        if not m.has_key("output_dest"):
            return None
        output_dest = m["output_dest"]
        
        return (output_dest, template.render(self.options.input))

    def comment(self, lines):
        return map(lambda l: "# " + l, lines)

    