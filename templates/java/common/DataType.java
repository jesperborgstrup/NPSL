{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

public enum DataType {
	Byte,
	Int,
	IntList,
	Float,
	String,
	StringList,
	Binary
}