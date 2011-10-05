import outputlanguage

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

python = outputlanguage.OutputLanguage( name="Python",
                                        folder="python",
                                        casing=outputlanguage.Casing.UNDERSCORE,
                                        filters=[("datatype", datatype)
                                                 ]
                                        )
