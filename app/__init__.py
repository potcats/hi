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

gear = ["cloth robe", "cloth veil", "cloth leggings", "iron greaves", "iron chestplate", "iron helmet", "iron leggings", "rat hide boots", "rat hide cloak", "rat hide hood", "simple sword", "excalibur", "crude club"]

statStr = [0, 0, 0, 3, 4, 2, 4, 0, 0, 0, 3, 0, 0]
statDex = [0, 0, 0, 0, 0, 0, 0, 3, 5, 2, 0, 0, 0]
statCon = [0, 0, 0, 1, 6, 2, 3, 0, 0, 0, 0, 0, 0]
statInt = [5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
statFth = [4, 8, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
statLck = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
statScl = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    buff TEXT,
    bMultiplier INTEGER,
    debuff TEXT,
    dMultiplier INTEGER,
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
    drops TEXT NOT NULL
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
    name TEXT PRIMARY KEY NOT NULL,
    type TEXT NOT NULL,
    image TEXT,
    str INTEGER,
    dex INTEGER,
    con INTEGER,
    int INTEGER,
    fth INTEGER,
    lck INTEGER,
    hpIncr INTEGER,
    energyIncr INTEGER

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

def loggedin():
    return 'username' in session

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

                c.execute("INSERT INTO user_profile VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (request.form['username'].lower(),
                        request.form['password']),
                        0, 30, "strike,cross slash", "", 0,
                        "", 0, 3, 0, 0,
                        0, 0, 0, "", "",
                        "", "", "simple sword", "", "", "")
                db.commit()

                session.clear()
                session.permanent = True
                session['username'] = request.form['username'].lower()
                return redirect(url_for('menu'))
    return render_template("register.html")

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    session['turn'] = 1
    session['inventory'] = {} # [name] {consumable?, quantity}

    return render_template("menu.html")

@app.route('/campfire', methods=['GET', 'POST'])
def campfire():
    # for testing purposes
    session['username'] = 'aaa'
    session['hp'] = 10
    session['currXP'] = 13
    session['maxXP'] = 27

    inv = session['inventory']
    stats = fetch_stats() # [level, HP, str, dex, con, int, fth, lck]
    equips = fetch_equips() # [helmet, chestplate, pants, boots, accessory1, accessory2, accessory3]

    return render_template("campfire.html",
        currTurn=session['turn'],
        username=session['username'],
        inventory=inv,
        HP=session['hp'],
        # maxHP=stats[1],
        # lvl=stats[0],
        # currXP=session['currXP'],
        # maxXP=session['maxXP'],
        # str=stats[2],
        # dex=stats[3],
        # con=stats[4],
        # int=stats[5],
        # fth=stats[6],
        # lck=stats[7],
        )

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    session.pop('battle', None)

    # if not loggedin():
    #     return redirect(url_for('login'))

    if 'battle' not in session:
        # placeholder battle state just for rendering
        session['battle'] = {
            "player": {
                "name": "tester",
                "hp": 30,
                "max_hp": 30, # changes with equipment/stats?
                "level": 1,
                "energy": 2,
                "attacks": ["Atk1", "Atk2", "Atk3"],
                "inventory": []
            },
            "enemies": [
                {"species": "goblin", "hp": 10, "max_hp": 10, "energy": 2},
                {"species": "bandit", "hp": 10, "max_hp": 10, "energy": 2},
                {"species": "pebble", "hp": 10, "max_hp": 10, "energy": 2},
            ],
            "turn": 1
        }

    #     session['battle'] = createBattle([randomEnemy('goblin'), randomEnemy('goblin')])
    #     # i change later!!!!
    #
    # if request.method == 'POST':
    #     action = request.json.get('action')
    #     if action == 'attack':
    #         move = request.json.get('move')
    #         target = request.json.get('target')
    #         # session['battle'] = attack(session['battle'], target, move)
    #     elif action == 'item':
    #         item = request.json.get('item')
    #         # session['battle'] = useItem(session['battle'], item)
    #     elif action == 'focus':
    #         # session['battle'] = focus(session['battle'])
    #
    #     return jsonify(session["battle"])

    return render_template("battle.html", battle = session['battle'])

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

# ------------------------ FLASK HELPER FUNCTIONS  ------------------------ #

def loggedin():
    return "username" in session

# ------------------------ DB HELPER FUNCTIONS  --------------------------- #

# [helmet, chestplate, pants, boots, accessory1, accessory2, accessory3]
def fetch_equips():
    c = db.cursor()
    equips = c.execute('''SELECT helmet,
        chestplate, pants, boots, weapon,
        accessory1, accessory2, accessory3
        FROM player WHERE username = ?''', (session['username'],)).fetchone()

    return equips

# [level, HP, str, dex, con, int, fth, lck]
def fetch_stats():
    c = db.cursor()
    stats = c.execute('''SELECT level, HP, str,
        dex, con, int, fth, lck
        FROM player WHERE username = ?''', (session['username'],)).fetchone()

    return stats

# [str, dex, con, int, fth, lck]
def fetch_itemStats(name):
    c = db.cursor()
    stats = c.execute('''SELECT str, dex, con, int, fth, lck
        FROM items WHERE name = ?''', (name,)).fetchone()

    return stats

# [hpIncr, energyIncr]
def fetch_itemEffects(name):
    c = db.cursor()
    effects = c.execute("SELECT hpIncr, energyIncr FROM items WHERE name = ?", (name,)).fetchone()

    return effects

def addItemToInventory(name):
    inv = session['inventory']

    if name in inv:
        inv[name][1] = str(int(inv[name][1]) + 1)
    else:
        c = db.cursor()
        info = c.execute("SELECT type FROM items WHERE name = ?", (name,)).fetchone()

        inv[name] = [info, str(1)]
        session['inventory'] = inv

# ------------------------------------------------------------------------- #


# RUN FLASK
if __name__=='__main__':
    app.debug = True
    app.run()
