# Carrie Ko, Christine Chen, Cindy Liu, Joyce Lin
# hi
# SoftDev
# P02: Makers Makin' It, Act I
# 01/16/2026

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from combat import *
from db import *

app = Flask(__name__)
app.secret_key = 'wahhhhhhhhhhhhhhhhh'

@app.route('/', methods=['GET', 'POST'])
def login():

    return render_template("login.html", )

@app.route('/menu', methods=['GET', 'POST'])
def menu():

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
def dialogue():

    return render_template("scavenge.html", )

# RUN FLASK
if __name__=='__main__':
    app.debug = True
    app.run()
