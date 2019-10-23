package CS407.exp2.test;

/**
 * @author Jason.F
 * @data 2019.10.11
 */

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.Reader;
import java.util.ArrayList;
import java.util.List;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

public class RegistHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange httpExchange) throws IOException {
    	//print the request method:post or get
        System.out.println("Method: " + httpExchange.getRequestMethod());      
        /*
        //get cookie content
        Headers reqHeaders = httpExchange.getRequestHeaders();     
        List<String> cookies = reqHeaders.get("Cookie");
        if(cookies != null) {
            System.out.println(cookies.size());
            System.out.println(cookies.get(0));
        }*/
        
        //get body data from web page
        InputStream is = httpExchange.getRequestBody();
        String body = is2string(is);
        System.out.println("body: " + body);
        is.close();//close the inputstream
        //get name and password from body
        JSONObject obj = JSON.parseObject(body);//parse json
        String userName = obj.getString("user_name");
        String password = obj.getString("password");
        
        //assert the user in the database
        String respStr = "";
        User user = new JDBCUtil().queryByName(userName);
        if(user != null) {
        	respStr = "{\"status\":400,\"msg\":\"regist failed!\"}";
        }else {
        	respStr = "{\"status\":0,\"msg\":\"regist success!\"}";
        	User u = new User();
        	u.setUserName(userName);
        	u.setPassword(password);
        	new JDBCUtil().insert(u);//insert the new user
        }
        System.out.println(respStr);//console print the result
        //return the result to the web page
        Headers headers = httpExchange.getResponseHeaders();
        headers.set("Content-Type", "application/json; charset=utf8");
        headers.set("Access-Control-Allow-Origin", "*");
        headers.set("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS");
        headers.set("Access-Control-Allow-Headers", "Origin,X-Requested-With,Content-Type,Accept");
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



