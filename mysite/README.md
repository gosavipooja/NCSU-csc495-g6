# Setup 
1. Copy the repo
2. Open `<repo>/mysite` in PyCharm (I promise Django development will be MUCH easier and its free to students)
3. Open a terminal and type `npm install` to install the dependencies in package.json
4. You should be able to run `python manage.py runserver` and the application should be served.

# Viewing Database In Database View of PyCharm
1. Hit shift twice to bring up the type menu to open something.
2. Type `Database` and hit enter.
3. Hit the `+` > `Data Source` > `Sqllite`
4. Install plugins for it if you have to IF it prompts you.
5. On the page it you cilck the `...`
6. Navigate to the repo and select `mysite/db.sqlite3`
7. Click `Test Connection` and it should be successful.
8. Click apply
9. You should now be able to see db.sqlite3 inside of the Database view.
  
# Django Commands
### Base Command
* `python manage.py ____`

### Run the Server
* `python manage.py runserver` - runs the server

### Create a new app
* `python manage.py startapp <name>` - creates a new application of that name

### Database Commands
* `python manage.py makemigrations <app name>` - migrates an app's models
* `python manage.py migrate`   - migrates python models into the sqllite database
* `python manage.py shell` - access to an interactive shell where you can work with the db

### Creating an Admin
* `python manage.py createsuperuser` - create an admin user for the admin interface


# How to Create an App (a page)
1. Run `python manage.py <app name>`
2. A new folder is created call <app name>
3. Open `mysite/mysite/settings.py`
4. Scroll down to `INSTALLED_APPS` and add to the top `<app name>.apps.<App name>Config`
 
 # How to import CSV files into Sqlite
1. Use [django-csvimport](https://github.com/edcrewe/django-csvimport) by installing it with `pip install django-csvimport` and `pip install messytables`
2. `python manage.py inspectcsv "<path_to_csv" > models.py`
    - This will create a model file that you MAY have to change (double check it).
    - Once you're happy with it copy the model to the relevant app.
3. Run `python manage.py makemigrations`
4. Run `python manage.py migrate` 
    - This will create the new table based off the modal 
4. `python manage.py importcsv --mappings='' --model='<app>.<model class name>' --delimiter=',' "<path_to_csv>"`
    - This will add the content to the table
