"""
direction    ::= "=>" | "<=" | "<>"
datatype     ::= "byte" | "int" | "ints" | "float" | "string" | "strings" | "binary"
parameter    ::= "(" + identifier + "," + datatype + ")"
identifier   ::= alpha + ( alphanum + "_" )*

moduleparam  ::= keyword(param) + direction + parameter
message      ::= direction + int + identifier + parameter + ("," + parameter)*
module       ::= identifier + "(" + declarations + ")"

declaration  ::= moduleparam | message | module
declarations ::= declaration*

npsl         ::= declarations
"""

from pyparsing import *

declarations = Forward()

identifier   = Word(alphas, alphanums + "_")
integer      = Word(nums)

lparam       = Suppress( Literal("(") )
rparam       = Suppress( Literal(")") )
direction    = (Literal("=>") | Literal("<=") | Literal("<>"))
datatype     = Keyword("byte") | Keyword("int") | Keyword("ints") | Keyword("float") | \
		       Keyword("string") | Keyword("strings") | Keyword("binary")
parameter    = Group( lparam + identifier + Suppress(Literal(",")) + datatype + rparam )

moduleparam  = Group( Keyword("param") + direction + parameter )
message      = Group( direction + integer + identifier + Group( Optional( delimitedList(parameter) ) ) ) 
module       = Group( identifier + lparam + declarations + rparam )

declaration  = moduleparam | message | module
declarations << ( ZeroOrMore( declaration ) )

npsl         = declarations + StringEnd()

if __name__ == "__main__":
	import sys, os, os.path
	if len( sys.argv ) == 0:
		sys.exit(-1)
		
	filename = sys.argv[1]
	if not os.path.exists( filename ):
		sys.exit(-1)
		
	f = open(filename)
	input = "".join( f.readlines() )
	
	print npsl.parseString( input ).asXML()
	
