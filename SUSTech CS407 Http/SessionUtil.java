package CS407.exp2;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
* @author Jason.F
* @data 2019.10.11
*/

//create session with singleton mode
public class SessionUtil {

	private static volatile ConcurrentHashMap<String, Map<String, Object>> session = null;
	
	private SessionUtil() {
		
	}
	
	public static ConcurrentHashMap<String, Map<String, Object>> getSession(){
		if(session == null) {
			synchronized(SessionUtil.class) {
				if(session == null) {
					session = new ConcurrentHashMap<>();
				}
			}
		}
		return session;
	}
}
