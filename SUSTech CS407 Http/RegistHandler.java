package CS407.exp2;

/**
 * @author Jason.F
 * @data 2019.10.11
 */

import java.util.HashMap;
import java.util.Map;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

public class RegistHandler{
	public static RequestResult handler(Request request) {
		RequestResult result = new RequestResult();
		System.out.println(request.getHeaders());
		String body = request.getMessage();
		System.out.println(body);
		JSONObject obj = JSON.parseObject(body);
		String userName = obj.getString("user_name");
		String password = obj.getString("password");

		String respStr = "";
		//assert the user in the database
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
		result.setRequest(request);
		result.setResult(respStr);
		return result;
	}
}



