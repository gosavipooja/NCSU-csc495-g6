import MySQLdb
import traceback

def fill_nulls(conn):
    cur = conn.cursor()

    select_query = """SELECT zip, `year`, week_of_year, `Primary Type` FROM testdb.final_prediction_table
                        WHERE num_houses IS NULL"""

    cur.execute(select_query)

    null_rows = cur.fetchall()

    cur.close()

    if(len(null_rows) == 0):
        return -1

    count = 0
    for row in null_rows:
        #print(row)
        cur = conn.cursor()

        other_houses_query = """SELECT AVG(num_houses) FROM testdb.final_prediction_table
                            WHERE zip='{}' AND week_of_year={} AND `Primary Type`='{}'
                        """.format(row[0], row[2], row[3])

        #print(other_houses_query)
        cur.execute(other_houses_query)

        other_rows = cur.fetchall()
        cur.close()

        if(other_rows[0][0] is None):
            continue

        avg_num_houses = round(other_rows[0][0])

        cur = conn.cursor()
        update_query = """UPDATE testdb.final_prediction_table SET num_lights={}
                            WHERE zip='{}' AND `year`={} AND week_of_year={} AND `Primary Type`='{}'
                        """.format(avg_num_houses, row[0], row[1], row[2], row[3])

        print(update_query)

        cur.execute(update_query)
        cur.close()


        count += 1
        print(count)
        if (count == 1000):
            return 1

def main():
    # create a database connection


    status = 0
    while(status != -1):
        conn = MySQLdb.connect(host="csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                               user="admin",  # your username
                               passwd="admin123",  # your password
                               db="testdb")  # name of the data base
        try:
            status = fill_nulls(conn)
        except:
            traceback.print_exc()

        print("CLOSING CONNECTION")
        conn.commit()
        conn.close()


if __name__ == '__main__':
    main()