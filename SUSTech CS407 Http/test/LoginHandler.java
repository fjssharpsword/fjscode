package CS407.exp2.test;

/**
 * @author Jason.F
 * @data 2019。10.11
 */

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.Reader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

public class LoginHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange httpExchange) throws IOException {
    	//print the request method
        System.out.println("Method: " + httpExchange.getRequestMethod());
        
        //get cookie content
        Headers reqHeaders = httpExchange.getRequestHeaders();
        List<String> cookies = reqHeaders.get("Cookie");
        if(cookies != null) {
            System.out.println("cookie: " + cookies.get(0));
            
            Map<String, String> map = new HashMap<>();
            String[] str = cookies.get(0).split(";");
            for(String s : str) {
            	String[] ss = s.trim().split("=");
            	map.put(ss[0], ss[1]);
            }
            if(map.get("http_session_id") != null) {
            	String http_session_id = map.get("http_session_id");
            	Map<String, Object> mm = SessionUtil.getSession().get(http_session_id);
            	if(mm != null) {
            		System.out.println("user in cookie: " + mm.get("user")+ "and create time:"+mm.get("create_time"));
            	}
            }
        }

        //get the data from web page.
        InputStream is = httpExchange.getRequestBody();
        String body = is2string(is);
        //String[] str = body.split("&");
        //System.out.println(str[0]);//observe many data
        System.out.println("body: " + body);
        is.close();   
        //parse json 
        JSONObject obj = JSON.parseObject(body);
        String userName = obj.getString("user_name");
        String password = obj.getString("password");
        
        //assert the user and password       
        Headers headers = httpExchange.getResponseHeaders();
        headers.set("Content-Type", "application/json; charset=utf8");
        //set cross-domain access
        headers.set("Access-Control-Allow-Origin", "*");
        headers.set("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS");
        headers.set("Access-Control-Allow-Headers", "Origin,X-Requested-With,Content-Type,Accept");
        String respStr = "";
        User user = new JDBCUtil().queryByNameAndPwd(userName, password);     
        if(user != null) {    
        	respStr = "{\"status\":0,\"msg\":\"login success\"}";
        	
        	//set session for long survive
        	String uuid = UUID.randomUUID().toString();
        	ConcurrentHashMap<String, Map<String, Object>> session = SessionUtil.getSession();
        	long ct = System.currentTimeMillis();
        	Map<String, Object> map = new HashMap<>();
        	map.put("user", user);
        	map.put("create_time", ct);
        	session.put(uuid, map);
        	
        	//set cookie
            List<String> list = new ArrayList<>();
            String cookieStr = "http_session_id=" + uuid;
            //System.out.println("uuid = " + cookieStr);
            list.add(cookieStr);
            headers.put("Set-Cookie", list);
            
        }else {
        	respStr = "{\"status\":400,\"msg\":\"login failed\"}";
        }
        
        //return result to web page
        httpExchange.sendResponseHeaders(200, respStr.length());
        OutputStream os = httpExchange.getResponseBody();   
        os.write(respStr.getBytes());
        os.close();
        httpExchange.close();
    }

    private String is2string(InputStream is) throws IOException {
        final int bufferSize = 1024;
        final char[] buffer = new char[bufferSize];
        final StringBuilder out = new StringBuilder();
        Reader in = new InputStreamReader(is, "UTF-8");
        for (; ; ) {
            int rsz = in.read(buffer, 0, buffer.length);
            if (rsz < 0)
                break;
            out.append(buffer, 0, rsz);
        }
        return out.toString();
    }
}



