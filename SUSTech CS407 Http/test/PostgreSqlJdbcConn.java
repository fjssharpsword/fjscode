package CS407.exp2.test;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class PostgreSqlJdbcConn {
	@SuppressWarnings("unused")
	public static void main(String args[]) {
		Connection c = null;
		Statement stmt = null;
		try{
			Class.forName("org.postgresql.Driver");
			c = DriverManager.getConnection("jdbc:postgresql://localhost:5432/CS407DB","postgres", "postgre");
			c.setAutoCommit(false);
			}catch (Exception e) {
				e.printStackTrace();
				System.err.println(e.getClass().getName()+": "+e.getMessage());
				System.exit(0);
			}
		System.out.println("Opened database successfully");
		
		try {
			//stmt = c.createStatement();
			//String sql = "insert into users(name, pwd) values('1','1');";
			//stmt.executeUpdate(sql);
			stmt = c.createStatement();
			ResultSet rs = stmt.executeQuery("select * from users");
			while(rs.next()){
				String name = rs.getString("name");
				String pwd = rs.getString("pwd");
				System.out.println(name + "," + pwd);
			}
			rs.close();
			stmt.close();
			c.commit();
			c.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	 }
}
