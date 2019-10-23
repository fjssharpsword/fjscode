package CS407.exp2;

import java.util.Map;

/**
 * @author Jason.F
 * @data 2019.10.11
 */
public class Request {
    /**
    * method: GET/POST/PUT/DELETE/OPTION...
     */
    private String method;
    /**
     * uri
     */
    private String uri;
    /**
     * http version
     */
    private String version;

    /**
     * packet header
     */
    private Map<String, String> headers;

    /**
     * relevant parameters
     */
    private String message;

	public String getMethod() {
		return method;
	}

	public void setMethod(String method) {
		this.method = method;
	}

	public String getUri() {
		return uri;
	}

	public void setUri(String uri) {
		this.uri = uri;
	}

	public String getVersion() {
		return version;
	}

	public void setVersion(String version) {
		this.version = version;
	}

	public Map<String, String> getHeaders() {
		return headers;
	}

	public void setHeaders(Map<String, String> headers) {
		this.headers = headers;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}

	@Override
	public String toString() {
		return "Request [method=" + method + ", uri=" + uri + ", version=" + version + ", headers=" + headers
				+ ", message=" + message + "]";
	}
}

