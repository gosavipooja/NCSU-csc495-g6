from sklearn import linear_model
import os
import pandas as pd
import MySQLdb as mysql
import numpy as np
import matplotlib.pyplot as plt


'''
connect to db and extract the information
'''

'''
def db_conn():
    conn = mysql.connect(host = 'csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com',port = 3306, user = 'admin', passwd = 'admin123', db = 'test_db')
    cursor = conn.cursor()
    return cursor

def extract_data(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return data

#example of a query: 'SELECT * FROM crim_data_with_date limit 10')

rows = cursor.fetchall()
for row in rows:
    print(row)
'''

def lin_regression(X,Y):
    model = linear_model.LinearRegression()
    model.fit(X,Y)
    return model

def predict(model, test_data):
    f = model.predict(test_data).flatten()
    print(f)


def visualize(x, f, data):
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(x, f, 'r', label='Prediction')
    ax.scatter(data.population , data.crime_type, label='Traning Data')
    ax.legend(loc=2)
    ax.set_xlabel('population')
    ax.set_ylabel('crime_type')
    ax.set_title('Crime_type vs. Size')
    #plt.show()
    
'''
import re
line = "Cats  are  smarter  than  dogs"

matchObj = re.match( r'(.*)\s{2,}(.*)\s{2,}(.*)', line)

if matchObj:
   print("matchObj.group() : ", matchObj.group())
   print("matchObj.group(1) : ", matchObj.group(1))
   print("matchObj.group(2) : ", matchObj.group(2))
else:
   print("No match!!")
'''
if  __name__ == '__main__':
    #cursor = db_conn()
    #query = ''
    #extract_data(cursor, query)
    path = os.getcwd() + '\\data_sample.txt'
    data = pd.read_csv(path, header=None, names=['population', 'abandoned_houses', 'crime_type'])
    data.insert(0, 'Ones', 1)
    cols = data.shape[1]
    X = data.iloc[:,0:cols-1]
    Y = data.iloc[:,cols-1:cols]
    X = np.matrix(X.values)
    Y = np.matrix(Y.values)
    model = lin_regression(X,Y)
    predict(model, X)
    x = np.array(X[:,1].A1)
    f = model.predict(X).flatten()

