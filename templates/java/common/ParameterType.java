{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

public class ParameterType {
	
	private String name;
	private DataType type;
	
	public ParameterType(String name, DataType type) {
		this.name = name;
		this.type = type;
	}
	
	public String getName() { return name; }
	public DataType getType() { return type; }

}
