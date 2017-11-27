from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
import MySQLdb as mysql
from .forms import ZipcodeForm

#from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LassoLarsCV, LassoCV
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
 


global data_crimes_per_year;
global crime_type;
global zip_codes;
global models;
global crime_data;
global raw_crime_data;
global year;
global trends_crime_data;


trends_crime_data = {}

year=[]

raw_crime_data= pd.DataFrame();

crime_data = pd.DataFrame();

models= {};
data_crimes_per_year = [];
crime_type = [];
zip_codes = [];


def create_model(conn, crime_type):
    #global assault, battery, bur, csa, homi, rob, theft;
    global crime_data
    if(crime_data.empty):
        extract_weekly_crime_data(conn)
    data = crime_data[crime_data['Primary Type']==crime_type]
    #upper-case all DataFrame column names
    data.columns = map(str.upper, data.columns)
    # Data Management
    data_clean = data.dropna()
    # recode1 = {1:1, 2:0}
    #data_clean['MALE']= data_clean['BIO_SEX'].map(recode1)
    #select predictor variables and target variable as separate data sets  
    predvar = data_clean[[ 'POPULATION', 'AFRICAN_AMERICAN', 'AMERICAN_INDIAN', 'ASIAN', 'WHITE_POPULATION']]
    target = data_clean['NUM_CRIMES']

    # standardize predictors to have mean=0 and sd=1
    predictors=predvar.copy()
    #predictors['ZIP']=preprocessing.scale(predictors['ZIP'].astype('float64'))
    #predictors['YEAR']=preprocessing.scale(predictors['YEAR'].astype('float64'))
    #predictors['WEEK_OF_YEAR']=preprocessing.scale(predictors['WEEK_OF_YEAR'].astype('float64'))
    predictors['POPULATION']=preprocessing.scale(predictors['POPULATION'].astype('float64'))
    predictors['AFRICAN_AMERICAN']=preprocessing.scale(predictors['AFRICAN_AMERICAN'].astype('float64'))
    predictors['AMERICAN_INDIAN']=preprocessing.scale(predictors['AMERICAN_INDIAN'].astype('float64'))
    predictors['ASIAN']=preprocessing.scale(predictors['ASIAN'].astype('float64'))
    predictors['WHITE_POPULATION']=preprocessing.scale(predictors['WHITE_POPULATION'].astype('float64'))
    # split data into train and test sets
    pred_train, pred_test, tar_train, tar_test = train_test_split(predictors, target, 

                                                                  test_size=.3, random_state=123)
    # specify the lasso regression model
    model=LassoLarsCV(cv=10, precompute=False).fit(pred_train,tar_train)
    # print variable names and regression coefficients
    print(crime_type)
    print(dict(zip(predictors.columns, model.coef_)))
    print('\n')
    # MSE from training and test data
    #ans[crime_type] = tar_test
    #ans[crime_type+'predicted'] = model.predict(pred_test)
    train_error = mean_squared_error(tar_train, model.predict(pred_train))
    test_error = mean_squared_error(tar_test, model.predict(pred_test))
    print ('training data MSE')
    print(train_error)
    print ('test data MSE')
    print(test_error)
    # R-square from training and test data
    rsquared_train=model.score(pred_train,tar_train)
    rsquared_test=model.score(pred_test,tar_test)
    print ('training data R-square')
    print(rsquared_train)
    print ('test data R-square')
    print(rsquared_test)
    return model



def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ZipcodeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            data = form.cleaned_data
            #data['zipcode']
            return HttpResponseRedirect(data['zipcode'] + '/results/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ZipcodeForm()

    return render(request, 'index.html', {'form': form})

def db_conn():
    conn = mysql.connect(host = 'csc591.c4mshtea0mhl.us-east-2.rds.amazonaws.com',port = 3306, user = 'admin', passwd = 'admin123', db = 'testdb')
    cursor = conn.cursor()
    return cursor,conn

def extract_data(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def extract_weekly_crime_data(conn):
    global crime_data
    crime_data = pd.read_sql('SELECT a.*, b.population, b.african_american, b.american_indian, b.asian, b.white_population\
                            FROM\
                            testdb.temp_crime_data_grouped_weekly as a\
                            inner join testdb.zipcode_population_data as b\
                            on a.zip = b.zipcode;', con=conn)


def extract_raw_crime_data(conn):
    global raw_crime_data
    raw_crime_data = pd.read_sql('SELECT * FROM testdb.raw_crime_data limit 1000', con=conn)



def extract_zip_codes():
    global zip_codes
    cursor, conn = db_conn()
    query = 'SELECT distinct zip from testdb.temp_crime_data_grouped_weekly'
    data = extract_data(cursor, query)
    for each_zip in data:
        if each_zip not in zip_codes:
            zip_codes.append(each_zip)



def trends(request):
    global data_crimes_per_year
    global crime_type
    global raw_crime_data
    global year
    global trends_crime_data
    cursor,conn = db_conn()
    # if(raw_crime_data.empty):
    #     extract_raw_crime_data(conn)
    #     raw_crime_data['year'] = raw_crime_data['Date'].str[6:10]
    #     raw_crime_data['month'] = raw_crime_data['Date'].str[:2]
    #     raw_crime_data['day'] = raw_crime_data['Date'].str[3:5]
    #     raw_crime_data['time'] = raw_crime_data['Date'].str[11:]
    if(not data_crimes_per_year):
        query_crimes_per_year = "SELECT `Primary Type`, year, SUM(num_crimes) as NUM_CRIMES \
                                 FROM testdb.temp_crime_data_grouped_weekly \
                                 WHERE year NOT LIKE '2001'\
                                 GROUP BY `Primary Type`, year\
                                 ORDER BY year"
        data_crimes_per_year = extract_data(cursor, query_crimes_per_year)
    weekdata = ['first', 'second']

    for row in data_crimes_per_year:
        if(row[0] not in crime_type):
            crime_type.append(row[0])
        if(row[1] not in year):
            year.append(row[1])
        if(row[1] in trends_crime_data):
            trends_crime_data[row[1]][row[0]] = row[2]
        else:
            trends_crime_data[row[1]] = {row[0] : row[2]}
    print(trends_crime_data)
    template = loader.get_template('trends.html')
    context = {'crime_type' : crime_type, 'year': year,'weekdata': weekdata, 'crime_data': trends_crime_data}
    return HttpResponse(template.render(context, request))



def predict(request):
    global crime_type
    cursor,conn = db_conn()
    if(not crime_type):
        query_crime_type = 'SELECT distinct `Primary Type` as primary_type \
                            FROM testdb.temp_crime_data_grouped_weekly \
                            GROUP BY `Primary Type`'
        result_crime_type = extract_data(cursor, query_crime_type)
        for row in result_crime_type:
            if(row[0] not in crime_type):
                crime_type.append(row[0])

    if(not models):
        for each_crime_type in crime_type:
            models[each_crime_type] = create_model(conn, each_crime_type)


    template = loader.get_template('predict.html')
    context = {}
    return HttpResponse(template.render(context, request))









def results(request, zipcode):
    cursor = db_conn()
    query = "select  `Primary Type`,  SUM(num_crimes) AS NUM_CRIMES, zip from testdb.temp_crime_data_grouped_weekly where `Primary Type` like 'ASSAULT' OR `Primary Type` like 'BURGLARY' OR `Primary Type` like 'WEAPONS VIOLATION' OR `Primary Type` like 'CRIM SEXUAL ASSAULT'  group by `Primary Type` limit 100;"
    data = extract_data(cursor, query)
    crime_type = []
    num_crimes = []
    zipcode = []
    for row in data:
        crime_type.append(row[0])
        num_crimes.append(int(row[1]))
        if row[2] not in zipcode:
            zipcode.append(row[2])
    template = loader.get_template('results.html')
    weeks = []
    for i in range(1,6,1):
        weeks.append(20 * i)
    context = { "zipcode" : zipcode, "weekdata" : weeks}
    return HttpResponse(template.render(context, request))