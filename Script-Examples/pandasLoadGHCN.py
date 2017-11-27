import pandas as pd
import numpy as np
import MySQLdb
import traceback


def add_ghcn_data(conn, year):
    cur = conn.cursor()

    create_sql = """
        CREATE TABLE IF NOT EXISTS testdb.ghcn_data_new(
            station VARCHAR(100),
            record_date VARCHAR(100),
            obs_type VARCHAR(50),
            obs_value FLOAT
        );
    """

    cur.execute(create_sql)

    cur.close()
    cur = conn.cursor()

    cur.execute("SELECT station_name FROM testdb.weather_stations WHERE zipcode is NOT NULL")
    station_rows = cur.fetchall()
    station_list  = []

    for row in station_rows:
        station_list.append(row[0])

    obs_list = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN', 'TAVG', 'TOBS']
    filename = 'C:/Users/santosh/Desktop/495_Work/ghcn_csvs/unzipped/{}.csv'.format(year)

    cur.close()

    chunksize = 1000000
    count = 0
    for chunk in pd.read_csv(filename, chunksize=chunksize, header=None,usecols=[0,1,2,3]):
        cur = conn.cursor()
        print(chunk.shape)

        chunk.columns = ['station_name', 'date', 'obs_type', 'obs_value']
        chunk = chunk[chunk['obs_type'].isin(obs_list)]
        chunk =  chunk[chunk['station_name'].isin(station_list)]

        print(chunk.shape)
        for index, row in chunk.iterrows():
            #print(row)
            #print(row[0])

            insert_query = """INSERT INTO ghcn_data_new (station, record_date, obs_type, obs_value) 
            VALUES ('{station}', '{date}', '{type}', {value})""".format(
                station=row['station_name'],
                date=row['date'],
                type=row['obs_type'],
                value=row['obs_value']
            )

            print(insert_query)
            cur.execute(insert_query)


        #break
        count += 1
        print(count)
        cur.close()

def main():

    for year in range(2012, 2017):
        conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                               user="admin",  # your username
                               passwd="admin123",  # your password
                               db="testdb")  # name of the data base
        try:
            with conn:
                add_ghcn_data(conn, year)
            conn.close()
        except:
            traceback.print_exc()

if __name__ == '__main__':
    main()