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

setting      ::= identifier + ":" + (string | integer | boolean)
settings     ::= keyword(settings) + "(" + setting* + ")"

npsl         ::= settings | declarations
"""

from pyparsing import *

declarations = Forward()

identifier   = Word(alphas, alphanums + "_")
integer      = Word(nums)
boolean      = CaselessLiteral("true") | CaselessLiteral("false")

lparam       = Suppress( Literal("(") )
rparam       = Suppress( Literal(")") )
direction    = (Literal("=>") | Literal("<=") | Literal("<>"))
datatype     = Keyword("byte") | Keyword("int") | Keyword("ints") | Keyword("float") | \
		       Keyword("string") | Keyword("strings") | Keyword("binary")
parameter    = Group( lparam + identifier + Suppress(Literal(",")) + datatype + rparam )

moduleparam  = Group( Keyword("param") + direction + parameter )
message      = Group( direction + integer + identifier + Group( Optional( delimitedList(parameter) ) ) ) 
module       = Group( identifier + integer + lparam + declarations + rparam )

comment      = Suppress( "#" + restOfLine)

settingvalue = (boolean | integer | quotedString.setParseAction(removeQuotes))
setting      = Group( identifier + Suppress( Literal( ":" ) ) + settingvalue )
settings     = Group( Keyword("settings") + lparam + Group(ZeroOrMore( setting )) + rparam )

declaration  = moduleparam | message | module
declarations << ( ZeroOrMore( declaration ) )

npsl         = ZeroOrMore(settings | declaration) + StringEnd()

npslparser   = npsl.copy()    

npslparser.ignore(comment)


