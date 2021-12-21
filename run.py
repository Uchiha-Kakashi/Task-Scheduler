import os
from typing import Hashable, MutableMapping
from flask import Flask, render_template, redirect, flash, request
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

from sqlalchemy.sql.elements import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tasks(db.Model):
    task_ID = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    Desc = db.Column(db.String(500), nullable = False)
    scheduled_at = db.Column(db.DateTime, nullable = False)
    completionNotes = db.Column(db.String(500), nullable = True)
    repeatTime = db.Column(db.DateTime, nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.now())
    Missed = db.Column(db.Boolean, default = False)
    Completed = db.Column(db.Boolean, default = False)

    def __repr__(self) -> str:
        return '{} to be done at {}'.format(self.title, self.scheduled_at)
    

@app.route('/welcome', methods = ['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        Title = request.form['Title']
        Description = request.form['Description']
        Scheduled_Str = request.form['Schedule']

        if Scheduled_Str:
            ListDateTime = Scheduled_Str.split(':')
            YYYY = int(ListDateTime[0].strip())
            MM = int(ListDateTime[1].strip())
            DD = int(ListDateTime[2].strip())

            HH = int(ListDateTime[3].strip())
            mm = int(ListDateTime[4].strip())
            ss = int(ListDateTime[5].strip())

            scheduled_at = datetime(YYYY, MM, DD, HH, mm, ss)

        TaskObject = Tasks(title = Title, Desc = Description, scheduled_at = scheduled_at)
        db.session.add(TaskObject)
        db.session.commit()

    return render_template('homepage.html')

@app.route('/alltasks', methods = ['GET', 'POST'])
def getAllTasks():
    AllTasks = Tasks.query.all()
    return render_template('allTasks.html', AllTasks = AllTasks)

@app.route('/missedtasks')
def getMissedTasks():
    timeNow = datetime.now()
    missedTasks = Tasks.query.filter(and_(Tasks.scheduled_at < timeNow, Tasks.Completed == False))
    return render_template('missedTasks.html', missedTasks = missedTasks)

@app.route('/scheduledtasks')
def getScheduledTasks():
    timeNow = datetime.now()
    scheduledTasks = Tasks.query.filter(Tasks.scheduled_at > (timeNow))
    return render_template('scheduledTasks.html', scheduledTasks = scheduledTasks)
    
@app.route('/completedtasks')
def getCompletedTasks():
    completedTasks = Tasks.query.filter(Tasks.Completed == True)
    return render_template('completedTasks.html', completedTasks = completedTasks)

@app.route('/markcomplete/<int:id>')
def CompleteTask(id):
    taskComplete = Tasks.query.get(id)
    taskComplete.Completed = True

    db.session.commit()

    return redirect('/alltasks')


if __name__ == '__main__':
    app.run(port = 80)