# Carrie Ko, Christine Chen, Cindy Liu, Joyce Lin
# hi
# SoftDev
# P02: Makers Makin' It, Act I
# 01/16/2026

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from combat import *

app = Flask(__name__)
app.secret_key = 'wahhhhhhhhhhhhhhhhh'

# ------------------------ DATABASING  ------------------------ #

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS player (
    username TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    level INTEGER NOT NULL,
    HP INTEGER NOT NULL,
    attacks TEXT NOT NULL,
    buff INTEGER,
    debuff INTEGER,
    str INTEGER,
    dex INTEGER,
    con INTEGER,
    int INTEGER,
    fth INTEGER,
    lck INTEGER,
    helmet TEXT,
    chestplate TEXT,
    pants TEXT,
    boots TEXT,
    weapon TEXT NOT NULL,
    accessory1 TEXT,
    accessory2 TEXT,
    accessory3 TEXT
);
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS enemies (
    type TEXT PRIMARY KEY NOT NULL,
    attacks TEXT NOT NULL,
    HP INTEGER NOT NULL,
    weakness TEXT,
    wMultiplier INTEGER,
    res TEXT,
    resMultiplier INTEGER,
    drop TEXT NOT NULL, 
);
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS encounters (
    type TEXT PRIMARY KEY NOT NULL,
    dialogue TEXT NOT NULL,
    background TEXT NOT NULL,
    desc TEXT NOT NULL,
    diff INTEGER NOT NULL
);
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS items (
    type TEXT PRIMARY KEY NOT NULL,
    image TEXT,
    scale TEXT,
    str INTEGER,
    dex INTEGER,
    con INTEGER,
    int INTEGER,
    fth INTEGER,
    lck INTEGER
);
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS attacks (
    name TEXT PRIMARY KEY NOT NULL,
    level INTEGER NOT NULL,
    energy TEXT,
    cd INTEGER NOT NULL,
    scale TEXT NOT NULL,
    statusEffects TEXT,
    baseDamage INTEGER
);
""")

#  ------------------------------------------------------------ #

@app.route('/', methods=['GET', 'POST'])
def login():
    if loggedin():
        return redirect(url_for('menu'))

    if request.method == 'POST':
        session.clear()
        session.permanent = True
        with sqlite3.connect(DB_FILE) as db:
                c = db.cursor()
                rows = c.execute("SELECT * FROM player WHERE username = ?;", (request.form['username'],))
                result = rows.fetchone()
                
                if result is None:
                    return render_template("login.html", "Username does not exist")
                elif (request.form['password'] != result[1]):
                    return render_template("login.html", "Your password was incorrect")

                session['username'] = request.form['username'].lower()
                return redirect(url_for('menu'))
    else:
        return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if loggedin():
        return redirect(url_for('menu'))
    else:
        if request.method == 'POST':
            with sqlite3.connect(DB_FILE) as db:
                c = db.cursor()
                
                rows = c.execute("SELECT username FROM player WHERE username = ?", (request.form['username'].lower(),))
                result = rows.fetchone()
                if result:
                    return render_template("register.html", "Duplicate username")
                session.permanent = True

                # for invalid requests / empty form responses
                t = ""
                if(request.form['username'] == "" or request.form['password'] == ""):
                    t = "Please enter a valid "
                    if(request.form['username'] == ""):
                        t = t + "username "
                    if(request.form['password'] == ""):
                        t = t + "password "
                    return render_template("register.html", t)

                c.execute("INSERT INTO user_profile VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (request.form['username'].lower(), request.form['password']), 0, 30, "strike,cross slash", 3, 0, 0, 0, 0, 0, "", "", "", "", "basic sword", "", "", "")
                db.commit()
                
                session.clear()
                session.permanent = True
                session['username'] = request.form['username'].lower()             
                return redirect(url_for('menu'))
    return render_template("register.html")

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    # # SETS DEFAULT SETTINGS
    # difficulties = ['checked', '', '']
    # cache=''
    #
    # # CHECKS FOR PREVIOUS SETTINGS
    # if len(session) > 0:
    #     if 'difficulty' in session:
    #         difficulties[0] = ''
    #         difficulties[session['difficulty']] = 'checked'
    #
    #     if 'cache' in session:
    #         cache = 'checked'

    # CREATES NEW GAME
    if request.method == 'POST':
        session.clear()
        data = request.form

        # # ADDS SETTINGS TO SESSION
        # if 'difficulty' in data:
        #     session['difficulty'] = int(data['difficulty'])
        #
        # if 'cache' in data:
        #     session['cache'] = 'checked'

        return redirect(url_for('battle'))

    return render_template("menu.html", )

@app.route('/campfire', methods=['GET', 'POST'])
def campfire():

    return render_template("campfire.html", )

@app.route('/battle', methods=['GET', 'POST'])
def battle():

    return render_template("battle.html", )

@app.route('/encounters', methods=['GET', 'POST'])
def encounters():

    return render_template("encounters.html", )

@app.route('/shop', methods=['GET', 'POST'])
def shop():

    return render_template("shop.html", )

@app.route('/dialogue', methods=['GET', 'POST'])
def dialogue():

    return render_template("dialogue.html", )

@app.route('/scavenge', methods=['GET', 'POST'])
def scavenge():

    return render_template("scavenge.html", )

# RUN FLASK
if __name__=='__main__':
    app.debug = True
    app.run()
