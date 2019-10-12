package CS407.exp1;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Inet4Address;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;


/**
* @author 11949039+Fang Jiansheng
* @data 2019.9.26
*/
public class TcpClient {

	private static Socket socket= new Socket(); 
	
	@SuppressWarnings("resource")
	public static void main(String[] args) throws UnknownHostException, IOException {
		//connect server
		socket.connect(new InetSocketAddress(Inet4Address.getLocalHost(), 11000), 3000);
		while(true){
			
			OutputStream os = socket.getOutputStream();
			PrintWriter pw = new PrintWriter(os);
			InputStream in = socket.getInputStream();
			//menu
			Scanner reader=new Scanner(System.in);
			System.out.println("Please enter menu No!");
			System.out.println("1.Register");
			System.out.println("2.Login");
			
			char opt = reader.next().charAt(0);
			if (opt =='1'){
				System.out.println("please enter your name, For example, jason");
				String name = reader.next();
				System.out.println("please enter your password, For example, 666");
				String pwd = reader.next();
				//send
				String msg = "r|"+name+"|"+pwd;
				pw.println(msg);
				pw.flush();
				//receive
				byte[] rbuf = new byte[1024 * 256];
				int rlen = in.read(rbuf);//read function may lead to block
				if(rlen < 0) {
					if(socket != null) {
						socket.close();
					}
					break;
				}
				String rmessage = new String(rbuf, 0, rlen);
				if (!"".equals(rmessage)) {
					System.out.println("server msg =" + rmessage);
				}
			}
			else if (opt =='2')	{
				System.out.println("please enter your name, For example, jason");
				String lname = reader.next();
				System.out.println("please enter your password, For example, 666");
				String lpwd = reader.next();
				//send
				String lmsg = "l|"+lname+"|"+lpwd;
				pw.println(lmsg);
				pw.flush();
				//receive
				byte[] lbuf = new byte[1024 * 256];
				int llen = in.read(lbuf);//read function may lead to block
				if(llen < 0) {
					if(socket != null) {
						socket.close();
					}
					break;
				}
				String lmessage = new String(lbuf, 0, llen);
				if (!"".equals(lmessage)) {
					System.out.println("server msg =" + lmessage);
				}
			}
		}
		if(socket != null) {
			socket.close();
		}
	}
}