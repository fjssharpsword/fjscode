package CS407.exp2;
/**
 * @author Jason.F
 * @data 2019.10.11
 */
import java.util.HashMap;
import java.util.Map;

public class RequestResult {
    private Request request;

    private String result;

    public Request getRequest() {
        return request;
    }

    public void setRequest(Request request) {
        this.request = request;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public RequestResult(Request request, String result) {
        this.request = request;
        this.result = result;
    }

    public RequestResult() {
    }

    public RequestResult(String result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "RequestResult{" +
                "request=" + request +
                ", result='" + result + '\'' +
                '}';
    }
}
