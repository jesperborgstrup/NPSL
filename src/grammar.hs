module Grammar where

import Text.Parsec
import Text.Parsec.Char
import Text.Parsec.Token
import Text.Parsec.Language

data Protocol     = Protocol [Declaration] deriving (Show)
data Declaration  = Assignment Var Expr
		  | Module ModuleName [Declaration]
		  | MessageDeclaration Message
		  | TypeDeclaration Var DataType
		  | File String deriving (Show)
data ModuleName   = ModuleName [String] deriving (Show)
data Var          = Var String deriving (Show)
data Expr         = Expr Prim deriving (Show)
data Prim         = PrimNum Integer 
		  | PrimBool Bool
		  | PrimStr String deriving (Show)
data Message      = ClientToServer MessageName [DataType]
                  | ServerToClient MessageName [DataType]
                  | BothWays MessageName [DataType] deriving (Show)
type MessageName  = String
data DataType     = ByteData
		  | IntData
		  | IntListData
		  | StringData
		  | StringListData
		  | BoolData
		  | BinaryData deriving (Show)

languageDef = emptyDef { commentLine = "#"
		       , identStart = letter <|> char '_'
		       , identLetter = alphaNum <|> char '_'
--		       , opStart = oneOf ":\"[]{}"
--		       , opLetter = ":\"[]{}"
		       , reservedOpNames = [":", "=>", "<=", "<>"]
		       , reservedNames = ["File", "True", "False", "Bool", "Byte", "Int", "IntList", "String", "StringList", "Binary"]
		       }