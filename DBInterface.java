import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

/**
 * @author pooja
 *
 */
public class DBInterface {

	public static void insertValue(String zipCode, String population) {
		try {
			String myDriver = "org.mariadb.jdbc.Driver";
			String myUrl = "jdbc:mariadb://csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com:3306/testdb";
			Class.forName(myDriver);
			Connection conn = DriverManager.getConnection(myUrl, "admin", "admin123");

			String query = " insert into zipcode_population_data (zipcode, population)" + " values (?, ?)";

			PreparedStatement preparedStmt = conn.prepareStatement(query);
			preparedStmt.setString(1, zipCode);
			preparedStmt.setString(2, population);

			preparedStmt.execute();

			conn.close();
		} catch (Exception e) {
			System.err.println("Got an exception: " + e.getMessage());
			e.printStackTrace();
		}
	}

}
