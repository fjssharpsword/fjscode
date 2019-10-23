package CS407.exp2;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Jason.F
 * @data 2019.10.21
 */
public class HttpMessageParser {
	/**
	 * parse request line
	 *
	 * @param reader
	 * @param request
	 */
	private static void decodeRequestLine(BufferedReader reader, Request request) throws IOException {
	    String[] strs = StringUtils.split(reader.readLine(), " ");
	    assert strs.length == 3;
	    request.setMethod(strs[0]);
	    request.setUri(strs[1]);
	    request.setVersion(strs[2]);
	}

	/**
	 * parse request header
	 *
	 * @param reader
	 * @param request
	 * @throws IOException
	 */
	private static void decodeRequestHeader(BufferedReader reader, Request request) throws IOException {
	    Map<String, String> headers = new HashMap<>(16);
	    String line = reader.readLine();
	    String[] kv;
	    while (!"".equals(line)) {
	        kv = StringUtils.split(line, ":");
	        assert kv.length == 2;
	        headers.put(kv[0].trim(), kv[1].trim());
	        line = reader.readLine();
	    }

	    request.setHeaders(headers);
	}

	
	/**
	 * parse message-body
	 *
	 * @param reader
	 * @param request
	 * @throws IOException
	 */
	private static void decodeRequestMessage(BufferedReader reader, Request request) throws IOException {
	    int contentLen = Integer.parseInt(request.getHeaders().getOrDefault("Content-Length", "0"));
	    if (contentLen == 0) {
	        // return if no message,such get/options method
	        return;
	    }

	    char[] message = new char[contentLen];
	    reader.read(message);
	    request.setMessage(new String(message));
	}


	/**
	 * The request of http includes three parts, such as request line (method+uri+version),
	 * request header, message-body (length of body is showed in content-length. 
	 * @param reqStream
	 * @return
	 */
	public static Request parse2request(InputStream reqStream) throws IOException {
	    BufferedReader httpReader = new BufferedReader(new InputStreamReader(reqStream, "UTF-8"));
	    Request httpRequest = new Request();
	    decodeRequestLine(httpReader, httpRequest);
	    decodeRequestHeader(httpReader, httpRequest);
	    decodeRequestMessage(httpReader, httpRequest);
	    return httpRequest;
	}
	//response 
	public static String buildResponse(Request request, String response) {
	    Response httpResponse = new Response();
	    httpResponse.setCode(200);
	    httpResponse.setStatus("ok");
	    httpResponse.setVersion(request.getVersion());

	    Map<String, String> headers = new HashMap<>();
	    headers.put("Content-Type", "application/json");
	    headers.put("Content-Length", String.valueOf(response.getBytes().length));
		if(request.getHeaders().get("Set-Cookie") != null){
			System.out.println("is cookie = " + request.getHeaders().get("Set-Cookie"));
			headers.put("Set-Cookie", request.getHeaders().get("Set-Cookie"));
		}
		headers.put("Access-Control-Allow-Origin", "*");
		headers.put("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS");
		headers.put("Access-Control-Allow-Headers", "Origin,X-Requested-With,Content-Type,Accept");
	    httpResponse.setHeaders(headers);

	    httpResponse.setMessage(response);

	    StringBuilder builder = new StringBuilder();
	    buildResponseLine(httpResponse, builder);
	    buildResponseHeaders(httpResponse, builder);
	    buildResponseMessage(httpResponse, builder);
	    return builder.toString();
	}


	private static void buildResponseLine(Response response, StringBuilder stringBuilder) {
	    stringBuilder.append(response.getVersion()).append(" ").append(response.getCode()).append(" ")
	            .append(response.getStatus()).append("\n");
	}

	private static void buildResponseHeaders(Response response, StringBuilder stringBuilder) {
	    for (Map.Entry<String, String> entry : response.getHeaders().entrySet()) {
	        stringBuilder.append(entry.getKey()).append(":").append(entry.getValue()).append("\n");
	    }
	    stringBuilder.append("\n");
	}

	private static void buildResponseMessage(Response response, StringBuilder stringBuilder) {
	    stringBuilder.append(response.getMessage());
	}



}
