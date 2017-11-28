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
global crime_data_train;
global crime_data_test;
global raw_crime_data;
global year;
global trends_crime_data;
global ans;


ans = {}

global location_crimes_per_year;
global trend_location_data;
global arrest_crimes_per_year;
global trend_arrest_data;


trends_crime_data = {}
trend_location_data = {}
trend_arrest_data = {}

year=[]

raw_crime_data= pd.DataFrame();

crime_data_train = pd.DataFrame();
crime_data_test = pd.DataFrame();

models= {};
data_crimes_per_year = [];
location_crimes_per_year = [];
arrest_crimes_per_year = [];
crime_type = [];
zip_codes = [];


def create_model(conn, crime_type):
    #global assault, battery, bur, csa, homi, rob, theft;
    global crime_data_train
    global crime_data_test
    if(crime_data_train.empty):
        extract_weekly_crime_data(conn)
    data = crime_data_train[crime_data_train['Primary Type'] == crime_type]
    test_data = crime_data_test[crime_data_test['Primary Type'] == crime_type]
    #upper-case all DataFrame column names
    data.columns = map(str.upper, data.columns)
    # Data Management
    data_clean = data.dropna()
    # recode1 = {1:1, 2:0}
    #data_clean['MALE']= data_clean['BIO_SEX'].map(recode1)
    #select predictor variables and target variable as separate data sets  
    predvar = data_clean[[ 'POPULATION', 'AFRICAN_AMERICAN', 'AMERICAN_INDIAN', 'ASIAN', 'WHITE_POPULATION', 'YEAR', 'WEEK_OF_YEAR',
     'NUM_LIGHTS', 'NUM_HOUSES', 'UNEMPLOYMENT_RATE' ]]
    target = data_clean['NUM_CRIMES']

    # standardize predictors to have mean=0 and sd=1
    predictors=predvar.copy()
    #predictors['ZIP']=preprocessing.scale(predictors['ZIP'].astype('float64'))
    predictors['POPULATION']=preprocessing.scale(predictors['POPULATION'].astype('float64'))
    predictors['AFRICAN_AMERICAN']=preprocessing.scale(predictors['AFRICAN_AMERICAN'].astype('float64'))
    predictors['AMERICAN_INDIAN']=preprocessing.scale(predictors['AMERICAN_INDIAN'].astype('float64'))
    predictors['ASIAN']=preprocessing.scale(predictors['ASIAN'].astype('float64'))
    predictors['WHITE_POPULATION']=preprocessing.scale(predictors['WHITE_POPULATION'].astype('float64'))
    predictors['YEAR']=preprocessing.scale(predictors['YEAR'].astype('float64'))
    predictors['WEEK_OF_YEAR']=preprocessing.scale(predictors['WEEK_OF_YEAR'].astype('float64'))
    #predictors['AVG_TEMP']=preprocessing.scale(predictors['AVG_TEMP'].astype('float64'))
    predictors['NUM_LIGHTS']=preprocessing.scale(predictors['NUM_LIGHTS'].astype('float64'))
    predictors['NUM_HOUSES']=preprocessing.scale(predictors['NUM_HOUSES'].astype('float64'))
    predictors['UNEMPLOYMENT_RATE']=preprocessing.scale(predictors['UNEMPLOYMENT_RATE'].astype('float64'))

    # split data into train and test sets
    pred_train, pred_test, tar_train, tar_test = train_test_split(predictors, target, 

                                                                  test_size=.01, random_state=123)
    # specify the lasso regression model
    model=LassoCV(cv=10, precompute=False).fit(pred_train,tar_train)
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
    run_model_on(model, crime_type)
    return model


def run_model_on(model, crime_type):
    global crime_data_test
    global ans
    data = crime_data_test[crime_data_test['Primary Type'] == crime_type]
    #upper-case all DataFrame column names
    data.columns = map(str.upper, data.columns)
    # Data Management
    data_clean = data.dropna()
    # recode1 = {1:1, 2:0}
    #data_clean['MALE']= data_clean['BIO_SEX'].map(recode1)
    #select predictor variables and target variable as separate data sets 
    result = data_clean[['ZIP', 'LAT', 'LON', 'PRIMARY TYPE', 'NUM_CRIMES' ]] 
    predvar = data_clean[[ 'POPULATION', 'AFRICAN_AMERICAN', 'AMERICAN_INDIAN', 'ASIAN', 'WHITE_POPULATION', 'YEAR', 'WEEK_OF_YEAR',
     'NUM_LIGHTS', 'NUM_HOUSES', 'UNEMPLOYMENT_RATE' ]]
    target = data_clean['NUM_CRIMES']

    # standardize predictors to have mean=0 and sd=1
    predictors=predvar.copy()
    #predictors['ZIP']=preprocessing.scale(predictors['ZIP'].astype('float64'))
    predictors['POPULATION']=preprocessing.scale(predictors['POPULATION'].astype('float64'))
    predictors['AFRICAN_AMERICAN']=preprocessing.scale(predictors['AFRICAN_AMERICAN'].astype('float64'))
    predictors['AMERICAN_INDIAN']=preprocessing.scale(predictors['AMERICAN_INDIAN'].astype('float64'))
    predictors['ASIAN']=preprocessing.scale(predictors['ASIAN'].astype('float64'))
    predictors['WHITE_POPULATION']=preprocessing.scale(predictors['WHITE_POPULATION'].astype('float64'))
    predictors['YEAR']=preprocessing.scale(predictors['YEAR'].astype('float64'))
    predictors['WEEK_OF_YEAR']=preprocessing.scale(predictors['WEEK_OF_YEAR'].astype('float64'))
    #predictors['AVG_TEMP']=preprocessing.scale(predictors['AVG_TEMP'].astype('float64'))
    predictors['NUM_LIGHTS']=preprocessing.scale(predictors['NUM_LIGHTS'].astype('float64'))
    predictors['NUM_HOUSES']=preprocessing.scale(predictors['NUM_HOUSES'].astype('float64'))
    predictors['UNEMPLOYMENT_RATE']=preprocessing.scale(predictors['UNEMPLOYMENT_RATE'].astype('float64'))
    #print crime type
    print(crime_type)
    print(dict(zip(predictors.columns, model.coef_)))
    print('\n')
    result['PREDICTED_NUM_CRIMES'] = model.predict(predictors)
    ans[crime_type] = result
    # MSE from training and test data
    error = mean_squared_error(target, model.predict(predictors))
    print ('MSE while running the model')
    print(error)
    # R-square from training and test data
    rsquared=model.score(predictors,target)
    print ('R-square while running the model')
    print(rsquared)


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
    global crime_data_train
    global crime_data_test
    crime_data_train = pd.read_sql("SELECT *\
                            FROM\
                            testdb.final_prediction_table \
                            WHERE lat IS NOT NULL AND (year NOT LIKE  '2017' OR (week_of_year NOT LIKE '41' AND week_of_year NOT LIKE '41') ) \
                            ;", con=conn)
    crime_data_train =  crime_data_train.drop(['avg_temp'], axis=1)
    crime_data_test = pd.read_sql("SELECT *\
                            FROM\
                            testdb.final_prediction_table \
                            WHERE lat IS NOT NULL AND (year LIKE  '2017' AND (week_of_year LIKE '41' OR week_of_year LIKE '41') ) \
                            ;", con=conn)
    crime_data_test =  crime_data_test.drop(['avg_temp'], axis=1)



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
    global location_crimes_per_year
    global arrest_crimes_per_year
    global trend_location_data
    global trend_arrest_data

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

    if(not location_crimes_per_year):
        query_location_crimes_per_year = """SELECT * FROM testdb.crimes_by_location_description 
                                            WHERE `Location Description` IN ('ABANDONED BUILDING', 'STREET', 'ALLEY', 'SIDEWALK', 'APARTMENT', 'RESIDENCE', 'SMALL RETAIL STORE')
                                            ORDER BY record_year, `Location Description`"""
        location_crimes_per_year = extract_data(cursor, query_location_crimes_per_year)

    if(not arrest_crimes_per_year):
        query_arrest_crimes_per_year = """SELECT * FROM testdb.Arrest_Count_By_Year 
                                            ORDER BY `Year`, `Primary Type`"""
        arrest_crimes_per_year = extract_data(cursor, query_arrest_crimes_per_year)

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

    locations_list = []
    trend_location_data = {'2012': [], '2013': [], '2014': [], '2015': [], '2016': [], '2017': [] }
    #trend_location_data = {'2012': []}
    for row in location_crimes_per_year:
        if(row[1] not in locations_list):
            locations_list.append(row[1])
        if(str(row[2]) in trend_location_data):
            trend_location_data[str(row[2])].append(row[0])

    #type_list = []
    trend_arrest_data = {'ASSAULT': [], 'BATTERY': [], 'BURGULARY': [], 'CRIM SEXUAL ASSAULT': [], 'HOMICIDE': [],
                         'ROBBERY': [], 'THEFT': []}
    for row in arrest_crimes_per_year:
        if (str(row[1]) in trend_arrest_data):
            trend_arrest_data[str(row[1])].append(row[2])

    print(locations_list)
    print(trends_crime_data)
    print(trend_location_data)
    print(trend_arrest_data)
    template = loader.get_template('trends.html')
    context = {'crime_type' : crime_type, 'year': year,'weekdata': weekdata, 'crime_data': trends_crime_data, 'location_data': trend_location_data, 'locations_list': locations_list, 'arrest_data': trend_arrest_data}
    return HttpResponse(template.render(context, request))



def forecast(conn, each_crime_type):
    create_model(conn, each_crime_type)


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
        print('inside models')
        for each_crime_type in crime_type:
            models[each_crime_type] = forecast(conn, each_crime_type)
    template = loader.get_template('predict.html')
    print(ans)
    assault_lat = ans['ASSAULT']['LAT'].tolist()
    assault_lon = ans['ASSAULT']['LON'].tolist()
    assault_val = ans['ASSAULT']['PREDICTED_NUM_CRIMES'].tolist()
    assault_zip = ans['ASSAULT']['ZIP'].tolist()
    assault_len = [x for x in range(0,len(assault_lat))]

    robbery_lat = ans['ROBBERY']['LAT'].tolist()
    robbery_lon = ans['ROBBERY']['LON'].tolist()
    robbery_val = ans['ROBBERY']['PREDICTED_NUM_CRIMES'].tolist()
    robbery_len = [x for x in range(0,len(robbery_lat))]
    robbery_zip = ans['ROBBERY']['ZIP'].tolist()

    homicide_lat = ans['HOMICIDE']['LAT'].tolist()
    homicide_lon = ans['HOMICIDE']['LON'].tolist()
    homicide_val = ans['HOMICIDE']['PREDICTED_NUM_CRIMES'].tolist()
    homicide_len = [x for x in range(0,len(homicide_lat))]
    homicide_zip = ans['HOMICIDE']['ZIP'].tolist()

    theft_lat = ans['THEFT']['LAT'].tolist()
    theft_lon = ans['THEFT']['LON'].tolist()
    theft_val = ans['THEFT']['PREDICTED_NUM_CRIMES'].tolist()
    theft_len = [x for x in range(0,len(theft_lat))]
    theft_zip = ans['THEFT']['ZIP'].tolist()

    battery_lat = ans['BATTERY']['LAT'].tolist()
    battery_lon = ans['BATTERY']['LON'].tolist()
    battery_val = ans['BATTERY']['PREDICTED_NUM_CRIMES'].tolist()
    battery_len = [x for x in range(0,len(battery_lat))]
    battery_zip = ans['BATTERY']['ZIP'].tolist()

    burglary_lat = ans['BURGLARY']['LAT'].tolist()
    burglary_lon = ans['BURGLARY']['LON'].tolist()
    burglary_val = ans['BURGLARY']['PREDICTED_NUM_CRIMES'].tolist()
    burglary_len = [x for x in range(0,len(burglary_lat))]
    burglary_zip = ans['BURGLARY']['ZIP'].tolist()

    sexual_assault_lat = ans['CRIM SEXUAL ASSAULT']['LAT'].tolist()
    sexual_assault_lon = ans['CRIM SEXUAL ASSAULT']['LON'].tolist()
    sexual_assault_val = ans['CRIM SEXUAL ASSAULT']['PREDICTED_NUM_CRIMES'].tolist()
    sexual_assault_len = [x for x in range(0,len(sexual_assault_val))]
    sexual_zip = ans['CRIM SEXUAL ASSAULT']['ZIP'].tolist()

    context = {'ans': ans, 
    'assault_lat': assault_lat,  
    'assault_lon': assault_lon,  
    'assault_val': assault_val,
    'assault_len': assault_len, 
    'assault_zip': assault_zip,

    'robbery_lat': robbery_lat,  
    'robbery_lon': robbery_lon,  
    'robbery_val': robbery_val,
    'robbery_len': robbery_len,
    'robbery_zip': robbery_zip, 

    'homicide_lat': homicide_lat,  
    'homicide_lon': homicide_lon,  
    'homicide_val': homicide_val, 
    'homicide_len': homicide_len,
    'homicide_zip': homicide_zip,

    'theft_lat': theft_lat,  
    'theft_lon': theft_lon,  
    'theft_val': theft_val,
    'theft_len': theft_len, 
    'theft_zip': theft_zip,

    'battery_lat': battery_lat,  
    'battery_lon': battery_lon,  
    'battery_val': battery_val, 
    'battery_len': battery_len,
    'battery_zip': battery_zip,

    'burglary_lat': burglary_lat,  
    'burglary_lon': burglary_lon,  
    'burglary_val': burglary_val, 
    'burglary_len': burglary_len,
    'burglary_zip': burglary_zip,

    'sexual_assault_lat': sexual_assault_lat,  
    'sexual_assault_lon': sexual_assault_lon,  
    'sexual_assault_val': sexual_assault_val,
    'sexual_assault_len': sexual_assault_len,
    'sexual_zip': sexual_zip
    }
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