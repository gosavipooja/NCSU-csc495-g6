import MySQLdb
import traceback

def add_ghnc_data():

    create_sql = """
        CREATE TABLE IF NOT EXISTS testdb.ghcn_data(
            station VARCHAR(100),
            record_date VARCHAR(100),
            obs_type VARCHAR(50),
            obs_value FLOAT
        );
    """

    for year in range(2011, 2016):
        load_query = """
        LOAD DATA LOCAL INFILE 'C:/Users/santosh/Desktop/495_Work/ghcn_csvs/unzipped/{}.csv' 
        INTO TABLE testdb.ghcn_data 
        FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n';
        """.format(year)

        print(load_query)

        drop_query = """
        DELETE FROM testdb.ghcn_data 
        WHERE

        YEAR(STR_TO_DATE(record_date, '%Y%m%d')) = {}

        AND

        (station NOT IN (SELECT station_name FROM testdb.weather_stations WHERE zipcode is NOT NULL)
        OR
        obs_type NOT IN ('PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN', 'TAVG', 'TOBS'));
        """.format(year)

        print(drop_query)


def main():
    add_ghnc_data()


if __name__ == '__main__':
    main()