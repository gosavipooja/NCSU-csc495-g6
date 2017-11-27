#!/usr/bin/python
import MySQLdb
import json
import urllib.request

# API KEY - AIzaSyClfjFUGKkyE2qVgsMgvsmAgx2ObcuJr8k


def add_weather(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    # cur = conn.cursor()
    # cur.execute("""CREATE TABLE IF NOT EXISTS historical_weather_data(
    #                 zipcode INT,
    #                 `date` DATE,
    #                 avg_temp FLOAT,
    #                 humidity FLOAT,
    #                 PRIMARY KEY(zipcode, date)
    #                 )
    #             """)
    # cur.execute("SELECT * FROM raw_crime_data LIMIT 10") #TODO: Still needs to be done to all rows
    #
    # rows = cur.fetchall()

    f = urllib.request('http://api.wunderground.com/api/2293f254e240bdc5/history_20060405/q/CA/San_Francisco.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']
    temp_f = parsed_json['current_observation']['temp_f']
    print
    "Current temperature in %s is: %s" % (location, temp_f)
    f.close()







def main():
    # create a database connection
    conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                           user="admin",  # your username
                           passwd="admin123",  # your password
                           db="testdb")  # name of the data base
    with conn:
        print("Add weather information")
        add_weather(conn)

    conn.close()


if __name__ == '__main__':
    main()