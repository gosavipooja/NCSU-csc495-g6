import traceback
import MySQLdb

def add_zip_date_rows(conn):
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

    cur.execute("SELECT DISTINCT zip, actual_date FROM temp_crime_data_grouped") #TODO: actual_date not entirely accurate

    rows = cur.fetchall()

    for row in rows:
        zip = row[0]
        ac_date = row[1]

        query = "INSERT INTO historical_weather_data(zipcode, `date`) VALUES ({}, '{}')".format(zip, ac_date)

        print(query)
        cur.execute(query)

def main():
    # create a database connection
    conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                           user="admin",  # your username
                           passwd="admin123",  # your password
                           db="testdb")  # name of the data base
    with conn:
        print("Add historical weather information")
        try:
            add_zip_date_rows(conn)
        except:
            traceback.print_exc()

    print("CLOSE CONNECTION")
    conn.close()


if __name__ == '__main__':
    main()