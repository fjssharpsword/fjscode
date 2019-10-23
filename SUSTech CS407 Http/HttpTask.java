package CS407.exp2;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;

/**
 * @author Jason.F
 * @data 2019.10.21
 */
//parse http protocol
public class HttpTask implements Runnable {
    private Socket socket;

    public HttpTask(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        if (socket == null) {
            throw new IllegalArgumentException("socket can't be null.");
        }

        try {
        	//response setting
            OutputStream outputStream = socket.getOutputStream();
            PrintWriter out = new PrintWriter(outputStream);
            //parse request packet
            Request httpRequest = HttpMessageParser.parse2request(socket.getInputStream());
            //System.out.println(httpRequest);
            RequestResult result = null;
            switch (httpRequest.getUri()){
                case DataKey.LOGIN_REQ:
                    result = LoginHandlers.handler(httpRequest);
                    System.out.println("result = " + result);
                    break;
                case DataKey.REGIST_REQ:
                	result = RegistHandler.handler(httpRequest);
                    System.out.println("result = " + result);
                    break;
                case DataKey.TEST:
                    System.out.println(httpRequest.getHeaders().get("Cookie"));
                    result = new RequestResult("request is test");
                    break;
                default:
                    result = new RequestResult("request is error");
                    break;
            }
            try {
                String httpRes = HttpMessageParser.buildResponse(httpRequest, result.getResult());
                out.print(httpRes);
            } catch (Exception e) {
                String httpRes = HttpMessageParser.buildResponse(httpRequest, e.toString());
                out.print(httpRes);
            }
            out.flush();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

