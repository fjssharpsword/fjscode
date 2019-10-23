package CS407.exp2;
/**
 * @author Jason.F
 * @data 2019.10.11
 */
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class SessionThread implements Runnable {
    @Override
    public void run() {
        while(true){
            ConcurrentHashMap<String, Map<String, Object>> session = SessionUtil.getSession();
            if(session.size() > 0){
                List<String> list = new ArrayList<>();
                for(Map.Entry<String, Map<String, Object>> entry : session.entrySet()){
                    Map<String, Object> map = entry.getValue();
                    long curTime = System.currentTimeMillis();
                    long ct = (long)map.get("create_time");
                    if((curTime - ct) >= Consts.SESSION_TIME){
                        list.add(entry.getKey());
                    }
                }
                if(list.size() > 0){
                    for(String s : list){
                        session.remove(s);
                    }
                }
            }

            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
