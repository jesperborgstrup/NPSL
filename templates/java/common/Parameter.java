{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

public class Parameter {
	
	private String name;
	private Object value;
	private DataType type;
	
	public String getName() { return name; }
	public Object getValue() { return value; }
	public DataType getType() { return type; }
	
	public Parameter(String name, byte value) {
		this(name, (Object)value);
		this.type = DataType.Byte;
	}
	
	public Parameter(String name, int value) {
		this(name, (Object)value);
		this.type = DataType.Int;
	}
	
	public Parameter(String name, int[] value) {
		this(name, (Object)value);
		this.type = DataType.IntList;
	}
	
	public Parameter(String name, float value) {
		this(name, (Object)value);
		this.type = DataType.Float;
	}
	
	public Parameter(String name, String value) {
		this(name, (Object)value);
		this.type = DataType.String;
	}
	
	public Parameter(String name, String[] value) {
		this(name, (Object)value);
		this.type = DataType.StringList;
	}
	
	public Parameter(String name, byte[] value) {
		this(name, (Object)value);
		this.type = DataType.Binary;
	}
	
	private Parameter(String name, Object value) {
		this.name = name;
		this.value = value;
	}

}
