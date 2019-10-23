package CS407.exp2.test;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
* @author Jason.F
* @data 2019.10.11
*/
public class JDBCUtil {

	public Connection getConn() {
		String driver = Consts.driver;
		String url = Consts.url;
		String username = Consts.username;
		String password = Consts.password;
		Connection conn = null;
		try {
			Class.forName(driver); // load classLoader
			conn = (Connection) DriverManager.getConnection(url, username, password);
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return conn;
		
	}
	
	public int insert(User user) {
	    Connection conn = getConn();
	    int i = 0;
	    String sql = "insert into users (name ,pwd) values(?,?)";
	    PreparedStatement pstmt;
	    try {
	        pstmt = (PreparedStatement) conn.prepareStatement(sql);
	        pstmt.setString(1, user.getUserName());
	        pstmt.setString(2, user.getPassword());
	        i = pstmt.executeUpdate();
	        pstmt.close();
	        conn.close();
	    } catch (SQLException e) {
	        e.printStackTrace();
	    }
	    return i;
	}
	
	public User queryByName(String userName) {
		User user = null;
	    Connection conn = getConn();
	    String sql = "select * from users where name = '" + userName + "'";
	    PreparedStatement pstmt;
	    try {
	        pstmt = (PreparedStatement)conn.prepareStatement(sql);
	        ResultSet rs = pstmt.executeQuery();
	        int col = rs.getMetaData().getColumnCount();
	        System.out.println("============================");
	        while (rs.next()) {
	        	user = new User();
	        	user.setId(rs.getInt(1));
	        	user.setUserName(rs.getString(2));
	        	user.setPassword(rs.getString(3));
	            System.out.println("user = " + user);
	        }
	        System.out.println("============================");
	    } catch (SQLException e) {
	        e.printStackTrace();
	    }
	    return user;
	}
	
	public User queryByNameAndPwd(String userName, String password) {
		User user = null;
	    Connection conn = getConn();
	    String sql = "select * from users where name = '" + userName + "' and pwd = '" + password + "'";
	    PreparedStatement pstmt;
	    try {
	        pstmt = (PreparedStatement)conn.prepareStatement(sql);
	        ResultSet rs = pstmt.executeQuery();
	        int col = rs.getMetaData().getColumnCount();
	        System.out.println("============================");
	        while (rs.next()) {
	        	user = new User();
	        	user.setId(rs.getInt(1));
	        	user.setUserName(rs.getString(2));
	        	user.setPassword(rs.getString(3));
	            System.out.println("user = " + user);
	        }
	        System.out.println("============================");
	    } catch (SQLException e) {
	        e.printStackTrace();
	    }
	    return user;
	}
}
