import MySQLdb
import urllib.request
import traceback
import re

def add_zipcode_data(conn):

    cur = conn.cursor()

    cur.execute("SELECT * FROM weather_stations")

    rows = cur.fetchall()
    cur.close()

    count = 0
    for row in rows:
        count += 1
        print(count)

        station_name = row[0]
        lat = row[1]
        lon = row[2]

        query = """
                #SET @lat = {lat};
                #SET @lon = {lon};
    
                SELECT DISTINCT zip
                FROM    temp_crime_data as t
                WHERE   MBRContains
                    (
                    LineString
                            (
                            Point (
                                    {lon} + {dist} / ( 111.1 / COS(RADIANS({lat}))),
                                    {lat} + {dist} / 111.1
                                  ),
                            Point (
                                    {lon} - {dist} / ( 111.1 / COS(RADIANS({lat}))),
                                    {lat} - {dist} / 111.1
                                  ) 
                            ),
                    Point(t.longitude, t.latitude)
                    )
        """.format(
            lat=lat,
            lon=lon,
            dist='5'
        )

        cur = conn.cursor()

        # print(query)
        cur.execute(query)

        zip_rows = cur.fetchall()
        cur.close()
        #print(zip_rows)

        if not zip_rows:
            continue

        cur = conn.cursor()

        cur.execute("SELECT DISTINCT zipcode FROM weather_stations")

        unique_zip = cur.fetchall()
        unique_zip_list = []

        for x in range(len(unique_zip)):
            if unique_zip[x][0] is not None:
                unique_zip_list.append(unique_zip[x][0])

        zip_idx = 0
        i = 0
        for zip in zip_rows:
            if(zip[0] not in unique_zip_list):
                zip_idx = i
                break
            i += 1

        update_query = "UPDATE weather_stations SET zipcode='{}' WHERE station_name='{}'".format(zip_rows[zip_idx][0], station_name)
        print(update_query)
        cur.execute(update_query)

        cur.close()







def main():
   # urllib.request.urlretrieve('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt', 'stations.txt')
   # create a database connection
   conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                          user="admin",  # your username
                          passwd="admin123",  # your password
                          db="testdb")  # name of the data base
   with conn:
       print("Add zipcode data to stations information")
       try:
           add_zipcode_data(conn)
       except:
           traceback.print_exc()

   print("CLOSE CONNECTION")
   conn.close()




if __name__ == '__main__':
    main()