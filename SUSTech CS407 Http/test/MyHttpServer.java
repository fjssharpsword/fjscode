package CS407.exp2.test;
/**
* @author Jason.F
* @data 2019.10.11
*/
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

public class MyHttpServer {  
  
    public static void main(String[] args) { 
    	//start httpserver and session
    	SessionThread st = new SessionThread();
    	Thread thread = new Thread(st);
    	thread.start();
        try {  
        	//server listening port=8082 
            HttpServer hs = HttpServer.create(new InetSocketAddress(8082), 0); 
            //mapping web and server
            hs.createContext("/regist", new RegistHandler());
            //hs.createContext("/registSuccess", new RegistSuccHandler());
            hs.createContext("/login", new LoginHandler());
            //hs.createContext("/test", new TestHandler());
            //hs.createContext("/index", new indexHandler());
            hs.setExecutor(null);//default
            hs.start();
        } catch (IOException e) {  
            e.printStackTrace();  
        }  
    }  
}

/***
class indexHandler implements HttpHandler{
    @Override
    public void handle(HttpExchange exchange) throws IOException {
    	Headers responseHeaders = exchange.getResponseHeaders();
        responseHeaders.set("Content-Type", "text/html;charset=utf-8");//set header
        
        //get session in which the user is saved if he/she has logined.
    	ConcurrentHashMap<String, Map<String, Object>> session = SessionUtil.getSession();
    	Headers reqHeaders = exchange.getRequestHeaders();
    	List<String> cookies = reqHeaders.get("Cookie");//get cookie
    	String http_session_id = "" + System.currentTimeMillis();
        if(cookies != null) {
            System.out.println(cookies.size());
            System.out.println(cookies.get(0));
            Map<String, String> map = new HashMap<>();
            String[] str = cookies.get(0).split(";");
            for(String s : str) {
            	String[] ss = s.trim().split("=");
            	map.put(ss[0], ss[1]);
            }
            if(map.get("http_session_id") != null) {
            	http_session_id = map.get("http_session_id");
            }
        }
        
        Map<String, Object> mm = SessionUtil.getSession().get(http_session_id);
        String response = "";
        if(mm != null) {//has logined
        	response = "<h3>Welcome!</h3>";
        	// reset create_time
        	long ct = System.currentTimeMillis();
        	mm.put("create_time", ct);
        	SessionUtil.getSession().put(http_session_id, mm);
        }else {
        	response = "<h3>Please login first!</h3>";
        }
        
        //return result
        System.out.println(response);
        exchange.sendResponseHeaders(200, 0);
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}

class RegistSuccHandler implements HttpHandler{
    @Override
    public void handle(HttpExchange exchange) throws IOException {
    	Headers responseHeaders = exchange.getResponseHeaders();
        responseHeaders.set("Content-Type", "text/html;charset=utf-8");
        String response = "<h3>Register success!</h3>";
        exchange.sendResponseHeaders(200, 0);
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}


class TestHandler implements HttpHandler{
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String response = "hello world";
        exchange.sendResponseHeaders(200, 0); 
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}

***/
