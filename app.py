import csv
import os
import io
import psycopg2
import requests
from flask import Flask,flash, render_template, request, session, redirect, url_for
from flask_session import Session
from flask import Flask, render_template, request  
from sqlalchemy import func


from models import * 



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/")
def index():
    clients=[] 
    try:
        Clients = Client.query.all()
        for client in Clients:
            clients.append(client)
        session['initalized'] = True
    except:
        session['initalized'] = False
    
    return render_template("index.html", clients= clients)

@app.route("/initialze" , methods=["POST"])
def initialze():
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@localhost/postgres".format(username, password)
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        app.secret_key =  os.getenv("SECRET_KEY")
        db.create_all()
        session['initalized'] = True
        flash('Database connection initialzed Successfully')
        return redirect(url_for('index'))

    except:
        session['initalized'] = False
        flash('Database connection initialization failed')
        return redirect(url_for('index'))

@app.route("/reset" , methods=["POST"])
def reset():
    if session['initalized']:
        db.drop_all()
        db.create_all()
        flash('Database reset Successful')
        return redirect(url_for('index'))
    else:
        flash('Database connection not initialized')
        return redirect(url_for('index'))

@app.route("/upload" , methods=["POST"])
def upload():
    if session['initalized']:
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file imported')
            return redirect(url_for('index'))
        # if user does not select file, browser also
        # submit an empty part without filename
        file = request.files['file']
        if file.filename == '':
            flash('No file imported')
            return redirect(url_for('index'))

        if file.filename.rsplit('.', 1)[1].lower() == 'csv':

            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            reader =csv.reader(stream)
            next(reader, None)
            for client,deal,date,accepted,refused in reader:        
                client_obj= Client()
                client_obj.client_name = client.split('@')[0]
                client_obj.client_id = int(client.split('@')[1])
                client_obj.deal_name = deal.split('#')[0]
                client_obj.deal_id = int(deal.split('#')[1])
                client_obj.date = date
                client_obj.accepted = accepted
                client_obj.refused = refused

                db.session.add(client_obj) 
                db.session.commit()
            
            
            flash('Data Imported Successfully')
            return redirect(url_for('index'))
    
    else:
        flash('Database connection not initialized')
        return redirect(url_for('index'))




