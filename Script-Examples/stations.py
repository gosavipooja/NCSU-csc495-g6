import MySQLdb
import urllib.request
import traceback
import re

def add_station_data(conn):
    # r = re.compile(
    #     "([\w]*)\s+" +
    #     "([\w\.]*)\s*" +
    #     "([\w\.\-]*).*"
    #     # "([\w\.]*)\s{2,}"+
    #     # "([\w\s]*)\s*"
    # )

    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS weather_stations(
                    station_name VARCHAR(300),
                    latitude FLOAT,
                    longitude FLOAT,
                    PRIMARY KEY(station_name)
                    )
                    """)

    count = 0
    with open('stations.txt') as input_file:
        for i, line in enumerate(input_file):
            line_array = line.split()
            station = line_array[0]
            lat = line_array[1]
            lon = line_array[2]

            lat_num = float(lat)
            lon_num = float(lon)

            if(lat_num < 41) or (lat_num > 42.1) or (lon_num < -88) or (lon_num > -86):
                continue

            query = "INSERT INTO weather_stations(station_name, latitude, longitude) VALUES ('{}', {}, {})".format(station, lat, lon)

            count += 1
            print(query)
            print(count)
            cur.execute(query)


def main():
   # urllib.request.urlretrieve('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt', 'stations.txt')
   # create a database connection
   conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                          user="admin",  # your username
                          passwd="admin123",  # your password
                          db="testdb")  # name of the data base
   with conn:
       print("Add weather station information")
       try:
           add_station_data(conn)
       except:
           traceback.print_exc()

   print("CLOSE CONNECTION")
   conn.close()




if __name__ == '__main__':
    main()