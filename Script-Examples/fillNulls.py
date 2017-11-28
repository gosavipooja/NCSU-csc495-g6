import MySQLdb
import traceback
import time

def fill_nulls(conn):
    cur = conn.cursor()

    select_query = """SELECT zip, `year`, week_of_year, `Primary Type` FROM testdb.final_prediction_table
                        WHERE num_lights IS NULL"""

    #print("AFTER FIRST SELECT")
    cur.execute(select_query)

    null_rows = cur.fetchall()

    if(len(null_rows) == 0):
        print(null_rows)
        return -1

    cur.close()
    count = 0
    for row in null_rows:
        #print(row)
        cur = conn.cursor()

        other_lights_query = """SELECT AVG(num_lights) FROM testdb.final_prediction_table
                            WHERE zip='{}' AND week_of_year={} AND `Primary Type`='{} AND num_lights <> -1'
                        """.format(row[0], row[2], row[3])

        #print(other_lights_query)
        cur.execute(other_lights_query)

        #print("OTHER LIGHTS QUERY")

        other_rows = cur.fetchall()
        cur.close()

        if(other_rows[0][0] is None):
            print(other_rows)
            cur = conn.cursor()
            update_query = """UPDATE testdb.final_prediction_table SET num_lights = {} 
            WHERE zip='{}' AND `year`={} AND week_of_year={} AND `Primary Type`='{}'
                            """.format(-1, row[0], row[1], row[2], row[3])
            cur.execute(update_query)
            cur.close()
            continue

        avg_num_lights = round(other_rows[0][0])

        cur = conn.cursor()
        update_query = """UPDATE testdb.final_prediction_table SET num_lights = {} 
        WHERE zip='{}' AND `year`={} AND week_of_year={} AND `Primary Type`='{}'
                        """.format(avg_num_lights, row[0], row[1], row[2], row[3])

        print(update_query)

        cur.execute(update_query)
        cur.close()


        count += 1
        print(count)
        if(count == 500):
            return 1

def main():
    # create a database connection


    status = 0
    start_time = 0
    while(status != -1):
        conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                               user="admin",  # your username
                               passwd="admin123",  # your password
                               db="testdb")  # name of the data base

        #print("MAKE CONN")
        try:
            start_time = time.time()
            status = fill_nulls(conn)
        except:
            traceback.print_exc()

        print("CLOSING CONNECTION {}".format(time.time()-start_time))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    main()