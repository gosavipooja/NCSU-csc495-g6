import MySQLdb
import traceback

def add_ghnc_data(conn, year):

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS testdb.ghcn_data(
            station VARCHAR(100),
            record_date VARCHAR(100),
            obs_type VARCHAR(50),
            obs_value FLOAT
        );
    """)

    print(year)
    load_query = """
    LOAD DATA LOCAL INFILE 'C:/Users/santosh/Desktop/495_Work/ghcn_csvs/unzipped/{}.csv' 
    INTO TABLE testdb.ghcn_data 
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n';
    """.format(year)

    cur.execute(load_query)

    print(load_query)

    drop_query ="""
    DELETE FROM testdb.ghcn_data 
    WHERE
        
    YEAR(STR_TO_DATE(record_date, '%Y%m%d')) = {}
    
    AND

    (station NOT IN (SELECT station_name FROM testdb.weather_stations WHERE zipcode is NOT NULL)
    OR
    obs_type NOT IN ('PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN', 'TAVG', 'TOBS'));
    """.format(year)

    cur.execute(drop_query)

    print(drop_query)


def db_connect(year):
    # create a database connection
    conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                           user="admin",  # your username
                           passwd="admin123",  # your password
                           db="testdb")  # name of the data base
    with conn:
        add_ghnc_data(conn, year)

    print("CLOSE CONNECTION")
    conn.close()

def main():
    for x in range(2011, 2018):
        try:
            db_connect(x)
        except:
            traceback.print_exc()

if __name__ == '__main__':
    main()