class DataTypes:
	Byte = 1
	Int = 2
	IntList = 3
	Float = 4
	String = 5
	StringList = 6
	Binary = 7
	
	types = { Byte: int,
			  Int: int,
			  IntList: list,
			  Float: float,
			  String: str,
			  StringList: list,
			  Binary: str }
	
	formats = { Byte: ">B",
			    Int: ">i",
			    IntList: None,
			    Float: ">f",
			    String: None,
			    StringList: None,
			    Binary: None}