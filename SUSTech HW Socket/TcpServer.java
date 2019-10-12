package CS407.exp1;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;

/**
* @author 11949039+Fang Jiansheng
* @data 2019.9.26
*/
public class TcpServer {
	private static Socket socket; //single connect
	private static ServerSocket serverSocket;
	private static Map<String, String> mapNP = new HashMap<>();
	
	public static void main(String[] args) throws IOException {
		serverSocket = new ServerSocket(11000);
		
		while(true) { //monitor
			socket = serverSocket.accept();//waiting for the connection from client
			
			if(socket.isConnected()) {//accept request and handle
				MyThread thread = new MyThread();
				Thread tt = new Thread(thread);
				thread.setSocket(socket);
				thread.setThread(tt);
				tt.start();
			}
		}
	}
	
	static class MyThread implements Runnable{
		private Thread thread;
		private Socket socket;
//		private Map<String, String> mapNP = new HashMap<String, String>();

		public Thread getThread() {
			return thread;
		}

		public void setThread(Thread thread) {
			this.thread = thread;
		}

		public Socket getSocket() {
			return socket;
		}

		public void setSocket(Socket socket) {
			this.socket = socket;
		}

		@Override
		public void run() {
			startListen(getSocket());
		}
		
		public void startListen(Socket socket) {
			try {
				while(true) {
					InputStream in = socket.getInputStream();
					byte[] buf = new byte[1024 * 256];
					int len = in.read(buf);
					String message = new String(buf, 0, len);
					if (!"".equals(message)) {
						System.out.println("client msg =" + message);
						String[] buff = message.split("\\|");
						if (buff[0].equals("r")){//register
							String name = buff[1];
							String pwd = buff[2];
							String retmsg = "";
							if (mapNP.containsKey(name)){
								retmsg = "Register Fail: this name have been registered";
							}else{//insert 
								mapNP.put(name, pwd);
								retmsg = "Register Success";
							}
							OutputStream os = socket.getOutputStream();
							PrintWriter pw = new PrintWriter(os);
							pw.println(retmsg);
							pw.flush();
						}
						else if (buff[0].equals("l")){//login
							String name = buff[1];
							String pwd = buff[2];
							String retmsg = "";
							if (mapNP.containsKey(name)){//this name have been registered
								String cpwd = mapNP.get(name);
								if (pwd.equals(cpwd)) retmsg = "Login Success";
								else retmsg = "Login Fail: password is not correct";
							}else{//insert 
								retmsg = "Login Fail: this name does not exist";
							}
							OutputStream os = socket.getOutputStream();
							PrintWriter pw = new PrintWriter(os);
							pw.println(retmsg);
							pw.flush();
						}
						else {
							OutputStream os = socket.getOutputStream();
							PrintWriter pw = new PrintWriter(os);
							pw.println("register or login failed!");
							pw.flush();
						}
					}
				}
			}catch(Exception e) {
				if(socket != null) {
					try {
						socket.close();
					} catch (IOException e1) {
						e1.printStackTrace();
					}
				}
				getThread().interrupt();
			}
		}
		
	}

}