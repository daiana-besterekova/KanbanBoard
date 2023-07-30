# Project description 
## 📝 Overview of "Your Ultimate Task Manager" 

The web application helps you manage your day and create tasks to track your progress throughout the day. Add, delete, and move your tasks around when they are done!

## 🛠️ Main functionalities: 
- Create your own account 
- Create a new task 
- Move tasks around  
- Delete tasks


## 📍 Where to find the project parts? 

**HTML files**
- Login page: flask-tutorial/flaskr/templates/auth/login.html 
- Logout page: flask-tutorial/flaskr/templates/auth/logout.html 
- Create task page: flask-tutorial/flaskr/templates/blog/create.html 
- Main page: flask-tutorial/flaskr/templates/blog/index.html 
- Update task page: flask-tutorial/flaskr/templates/blog/update.html 
- Base page: flask-tutorial/flaskr/templates/base.html

**CSS file**
- Style file: flask-tutorial/flaskr/static/style.css

**Python files**
- Creating app: flask-tutorial/flaskr/__init__.py
- Authorization: flask-tutorial/flaskr/auth.py
- Collection of all function: flask-tutorial/flaskr/blog.py
- Work with database: flask-tutorial/flaskr/db.py

**SQLite file**
- flask-tutorial/flaskr/instance/flaskr.sqlite

**SQL file**
- flask-tutorial/flaskr/schema.sql

## 👩🏽‍💻 User Guide: How to use the Application 
```
$ pip3 install virtualenv
$ virtualenv env
$ source env/bin/activate

```
You'll see a new folder in your main folder called "env". To run the application write the following: 
```
$ pip3 install flask 
$ pip3 install -r requirements.txt
$ flask --app flaskr run --debug
```
You’ll see output similar to this:
```
* Serving Flask app "flaskr"
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: nnn-nnn-nnn
```
