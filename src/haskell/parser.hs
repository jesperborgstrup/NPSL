module Parser where

import Control.Applicative((<*))
import Text.Parsec
import Text.Parsec.String
import Text.Parsec.Expr
import Text.Parsec.Token
import Text.Parsec.Language
import Utils

import Grammar

TokenParser{ parens = m_parens
           , braces = m_braces
           , identifier = m_identifier
           , reservedOp = m_reservedOp
           , reserved = m_reserved
           , commaSep = m_commaSep
           , integer = m_integer
           , symbol = m_symbol
           , stringLiteral = m_stringLiteral
           , whiteSpace = m_whiteSpace } = makeTokenParser languageDef
           
      
declaration = try assignment <|> try m_module <|> try msg <|> try typedecl <|> try file <?> "Assignment, module, message or file"
       where assignment = do v <- var
	        	     m_reservedOp ":"
	        	     e <- expr
	        	     return (Assignment v e)
	     m_module   = do ns <- sepBy1 m_identifier (char '.')
		 	     ds <- m_parens $ many declaration
		 	     return (Module (ModuleName ns) ds)
	     msg	= do m <- message
	     		     return (MessageDeclaration m)
	     typedecl   = do v <- var
	     		     m_reservedOp ":"
	     		     t <- datatype
	     		     return (TypeDeclaration v t)
	     file       = do m_reserved "File"
	     		     f <- m_stringLiteral
	     		     return (File f)
	     		     
message  = try c2s <|> try s2c <|> try bothways <?> "Message (<=, => or <>)"
    where
           c2s      = do m_reservedOp "=>"
           	         (n, ps) <- rest
                         return (ClientToServer n ps)
           s2c      = do m_reservedOp "<="
           	         (n, ps) <- rest
                         return (ServerToClient n ps)
           bothways = do m_reservedOp "<>"
           	         (n, ps) <- rest
                         return (BothWays n ps)
                         
           rest      = do n <- m_identifier
                    	  ps <- option [] (do m_reservedOp ":"
                    	  	              types <- m_commaSep datatype
                    	  	              return types)
                    	  return (n, ps)

	        	     
var = do v <- m_identifier
	 return (Var v)
           
expr = do p <- prim
	  return (Expr p)
           
prim = num <|> bool <|> str'
     where
       num  = do num <- m_integer
                 return (PrimNum num)
       bool = (m_reserved "True" >> return (PrimBool True)) 
          <|> (m_reserved "False" >> return (PrimBool False))
       str' = do s <- m_stringLiteral
       		 return (PrimStr s)
       		           
datatype = (m_reserved "Bool" >> return BoolData)
       <|> (m_reserved "Byte" >> return ByteData)
       <|> (m_reserved "Int" >> return IntData)
       <|> (m_reserved "IntList" >> return IntListData)
       <|> (m_reserved "String" >> return StringData)
       <|> (m_reserved "StringList" >> return StringListData)
       <|> (m_reserved "Binary" >> return BinaryData)


mainParser = do m_whiteSpace
		ds <- many declaration
		eof
		return ds
		
	--importFiles []     = []
--importFiles (c:cs) =
           
readProtocol :: String -> IO ()
readProtocol input = case parse mainParser "" input of
    Left err -> putStrLn $ "No match: " ++ show err
    Right val -> putStrLn $ show val
    
--parseFile :: String -> [Declaration]
parseFile file = do str <- readFile file
		    case parse mainParser "" str of
		      Left err -> do putStrLn err
		      		     return []
		      Right val -> return val
		      
printFile :: String -> IO ()
printFile file = do decls <- parseFile file
		    putStrLn $ show decls
