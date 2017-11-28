#!/usr/bin/python
import MySQLdb
import traceback
import urllib.request

from ast import literal_eval

# API KEY - AIzaSyClfjFUGKkyE2qVgsMgvsmAgx2ObcuJr8k

def add_zipcodes(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM crime_data_with_date WHERE zipcode IS NULL LIMIT 10000") #TODO: Still needs to be done to all rows)

        rows = cur.fetchall()

        if not rows:
            print("ALL OF THEM ARE DONE")
            return False

        for row in rows:
            print(row)

            lat = row[-4]
            long = row[-3]

            url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key=AIzaSyClfjFUGKkyE2qVgsMgvsmAgx2ObcuJr8k".format(lat, long)

            request_response = urllib.request.urlopen(url).read()
            dict_response = literal_eval(request_response.decode('utf8'))

            print(dict_response)

            for component in dict_response["results"][0]["address_components"]:
                if(component['types'][0] == "postal_code"):
                    sql_query = "UPDATE raw_crime_data SET zipcode={} WHERE ID={}".format(component['long_name'], row[0])
                    print(sql_query)
                    cur.execute(sql_query)

        return True
    except Exception as e:
        traceback.print_tb()
        return False


def main():
    # create a database connection
    conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                           user="admin",  # your username
                           passwd="admin123",  # your password
                           db="testdb")  # name of the data base
    with conn:
        print("Add zipcode information by reverse geocoding")
        flag = add_zipcodes(conn)
        while(flag):
            print("Add zipcode information by reverse geocoding in loop")
            flag = add_zipcodes(conn)

    conn.close()


if __name__ == '__main__':
    main()

