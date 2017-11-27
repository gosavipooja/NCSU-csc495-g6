import java.text.ParseException;

import org.json.simple.JSONArray;
import org.json.simple.parser.JSONParser;

import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.WebResource;

/**
 * @author pooja
 *
 */
public class WebInterface {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		doStuff();
	}

	private static void doStuff() throws ParseException {
		Client client = Client.create();
		WebResource webResource = client.resource(
				"https://api.census.gov/data/2010/sf1?get=P0010001&for=zip+code+tabulation+area:*&in=state:17");
		String response = webResource.get(String.class);
		JSONParser parser = new JSONParser();
		JSONArray jsonArr;
		try {
			jsonArr = (JSONArray) parser.parse(response);

			for (Object obj : jsonArr.toArray()) {
				JSONArray jsonInnerArray = (JSONArray) obj;
				String population = (String) jsonInnerArray.get(0);
				String zip = (String) jsonInnerArray.get(2);
				if (population.startsWith("P")) {
					continue;
				} else {
					System.out.println("Entry:");
					System.out.println("\tPopulation: " + population);
					System.out.println("\tState: " + jsonInnerArray.get(1));
					System.out.println("\tZip: " + zip);
					DBInterface.insertValue(zip, population);
				}
			}
		} catch (org.json.simple.parser.ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
