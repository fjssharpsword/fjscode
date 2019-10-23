package CS407.exp2;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * @author Jason.F
 * @data 2019.10.21
 */
public class LoginHandlers {

	public static RequestResult handler(Request request) {
		RequestResult result = new RequestResult();
		System.out.println(request.getHeaders());
		Map<String, String> headers = request.getHeaders();
		String cookies = headers.get("Cookie");
		if(cookies != null) {
			System.out.println("cookie: " + cookies);

			Map<String, String> map = new HashMap<>();
			String[] str = cookies.split(";");
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

		String body = request.getMessage();
		System.out.println(body);
		JSONObject obj = JSON.parseObject(body);
		String userName = obj.getString("user_name");
		String password = obj.getString("password");

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
			System.out.println("uuid = " + cookieStr);
			list.add(cookieStr);
			request.getHeaders().put("Set-Cookie", cookieStr);

		}else {
			respStr = "{\"status\":400,\"msg\":\"login failed\"}";
		}
		result.setRequest(request);
		result.setResult(respStr);
		return result;
	}
}
