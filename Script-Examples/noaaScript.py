import requests
import MySQLdb
import traceback
import time
import sys

tb = sys.exc_info()

def month_day(day):
    day += 14
    if(day > 29):
        day = 28

    return day

def query_format(min, max, prcp, snow, zipcode, date):

    columns = ""
    values = ""

    if min is not None:
        columns += "min_temp, "
        values += str(min)
        values += ", "

    if max is not None:
        columns += "max_temp, "
        values += str(max)
        values += ", "

    if prcp is not None:
        columns += "prcp, "
        values += str(prcp)
        values += ", "

    if snow is not None:
        columns += "snow, "
        values += str(snow)
        values += ", "

    if columns.endswith(", "):
        columns = columns[:-2]

    if values.endswith(", "):
        values = values[:-2]

    query = "INSERT INTO historical_weather_data(zipcode, `date`, {}) VALUES( {}, '{}', {} )".format(columns, zipcode, date, values)
    print(query)
    return query


def add_weather(conn):

    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS historical_weather_data(
                    zipcode INT,
                    `date` DATE,
                    min_temp FLOAT,
                    max_temp FLOAT,
                    prcp FLOAT,
                    snow FLOAT,
                    PRIMARY KEY(zipcode, date)
                    )
                """)

    cur.execute("SELECT DISTINCT zip, actual_date FROM temp_crime_data_grouped WHERE actual_date > '2015-01-18' LIMIT 100") #TODO: actual_date not entirely accurate

    rows = cur.fetchall()

    for row in rows:
        zipcode = row[0]
        date = "{}-{}-{}".format(row[1].year, '%02d' % row[1].month, '%02d' % row[1].day) #2010-05-01
        end_date = "{}-{}-{}".format(row[1].year, '%02d' % row[1].month, '%02d' % month_day(row[1].day))

        url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&locationid=ZIP:{}&startdate={}&enddate={}&units=standard".format(zipcode, date, end_date)
        print(url)

        r = requests.get(url, headers={'token' : 'xXlsLUUMyPeUxzjDfcvBxTxBTDcrSHsx'})

        print(r.text)
        r = r.json()
        if not r:
            print("EMPTY RESPONSE")
            time.sleep(1)
            continue

        min_temp = None
        max_temp = None
        prcp = None
        snow = None

        print(r)
        for result in r['results']:
            if(result['datatype'] == 'TMIN'):
                min_temp = result['value']
                continue

            if(result['datatype'] == 'TMIN'):
                max_temp = result['value']
                continue

            if(result['datatype'] == 'PRCP'):
                prcp = result['value']
                continue

            if(result['datatype'] == 'SNOW'):
                snow = result['value']

        sql_query = query_format(min_temp, max_temp, prcp, snow, zipcode, date)

        try:
            cur.execute(sql_query)
        except:
            traceback.print_exc()



def main():
    # create a database connection
    conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                           user="admin",  # your username
                           passwd="admin123",  # your password
                           db="testdb")  # name of the data base
    with conn:
        print("Add historical weather information")
        try:
            add_weather(conn)
        except:
            traceback.print_exc()

    print("CLOSE CONNECTION")
    conn.close()


if __name__ == '__main__':
    main()