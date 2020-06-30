from flask import Flask, render_template, Response
import employee_db, event_db, oldperson_db, user_db, volunteer_db

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/employee')
def employee():
    return employee_db.getEmployees()


@app.route('/event')
def event():
    return event_db.getEvents()


@app.route('/volunteer')
def volunteer():
    return volunteer_db.getVolunteers()


@app.route('/oldperson')
def oldperson():
    return oldperson_db.getOlds()


@app.route('/user')
def user():
    return user_db


if __name__ == '__main__':
    app.run()
