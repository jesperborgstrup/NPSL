{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.IOException;

public class ByteArray {
	
	private DataInputStream stream;
	
	public ByteArray(byte[] buffer) {
		this.setBuffer(buffer);
	}

	public void setBuffer(byte[] buffer) {
		this.stream = new DataInputStream( new ByteArrayInputStream( buffer ) );
	}
/*
	public byte[] getBuffer() {
		return stream.
	}
*/
	/*
	public byte[] shift(int length) {
		if (buffer.length < length) {
			throw new IndexOutOfBoundsException( String.format("Trying to shift %d bytes from an array of size %d", length, buffer.length ) );
		}
		byte[] result = new byte[length];
		byte[] newBuffer = new byte[buffer.length-length];
		for (int i = 0; i < length; i++)
			result[i] = buffer[i];
		for (int i = 0; i < buffer.length-length; i++)
			newBuffer[i] = buffer[i+length];
		buffer = newBuffer;
		return result;
	}
	*/
	public Object parseType(DataType type) throws IOException {
		Object val = null;
		switch (type) {
		case Byte:
			val = parseByte();
			break;
		case Int:
			val = parseInt();
			break;
		case IntList:
			val = parseIntList();
			break;
		case Float:
			val = parseFloat();
			break;
		case String:
			val = parseString();
			break;
		case StringList:
			val = parseStringList();
			break;
		case Binary:
			val = parseBinary();
			break;
		}
		
		return val;
	}
	
	public byte parseByte() throws IOException {
		return stream.readByte();
	}
	
	public int parseInt() throws IOException {
		return stream.readInt();
	}
	
	public int[] parseIntList() throws IOException {
		int length = parseInt();
		int[] result = new int[length];
		for (int i = 0; i < length; i++)
			result[i] = parseInt();
		
		return result;
	}
	
	public float parseFloat() throws IOException {
		return stream.readFloat();
	}
	
	public String parseString() throws IOException {
		return stream.readUTF();
	}
	
	public String[] parseStringList() throws IOException {
		int length = parseInt();
		String[] result = new String[length];
		for (int i = 0; i < length; i++)
			result[i] = parseString();
		
		return result;
		
	}
	
	public byte[] parseBinary() throws IOException {
		int length = parseInt();
		byte[] result = new byte[length];
		stream.read(result, 0, length);
		return result;
	}

}
