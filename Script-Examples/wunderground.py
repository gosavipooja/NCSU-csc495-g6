import traceback
import MySQLdb
import urllib.request
import time
from ast import literal_eval

def query_format(avg, min, max, prcp, snow, zipcode, date):

    columns = ""

    if avg is not None:
        columns += "avg_temp="
        columns += str(avg)
        columns += ", "

    if min is not None:
        columns += "min_temp="
        columns += str(min)
        columns += ", "

    if max is not None:
        columns += "max_temp="
        columns += str(max)
        columns += ", "

    if prcp is not None:
        columns += "prcp="
        columns += str(prcp)
        columns += ", "

    if snow is not None:
        columns += "snow="
        columns += str(snow)
        columns += ", "

    if columns.endswith(", "):
        columns = columns[:-2]

    query = "UPDATE historical_weather_data SET {} WHERE zipcode = {} AND `date`='{}'".format(columns,zipcode, date)
    print(query)
    return query

def add_wunder_data(conn):
    cur = conn.cursor()

    cur.execute("SELECT zipcode, `date` FROM historical_weather_data WHERE avg_temp is NULL LIMIT 110") #TODO: actual_date not entirely accurate

    rows = cur.fetchall()

    for row in rows:
        zip = row[0]
        date = "{}-{}-{}".format(row[1].year, '%02d' % row[1].month, '%02d' % row[1].day)  # 20100501

        f = urllib.request.urlopen('http://api.wunderground.com/api/2293f254e240bdc5/history_{}/q/{}.json'.format(date, zip)).read()
        result = literal_eval(f.decode('utf8'))

        #print(result['history']['dailysummary'])

        daily_result =  result['history']['dailysummary'][0]

        avg_temp = daily_result['meantempi']

        min_temp = daily_result['mintempi']

        max_temp = daily_result['maxtempi']

        snow = daily_result['snowfalli']

        prcp = daily_result['rain']


        query = query_format(avg_temp, min_temp, max_temp, prcp, snow, zip, date)

        # print(query)
        cur.execute(query)
        time.sleep(7)

def main():
    # create a database connection
    conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                           user="admin",  # your username
                           passwd="admin123",  # your password
                           db="testdb")  # name of the data base
    with conn:
        print("Add historical weather information")
        try:
            add_wunder_data(conn)
        except:
            traceback.print_exc()

    print("CLOSE CONNECTION")
    conn.close()


if __name__ == '__main__':
    main()