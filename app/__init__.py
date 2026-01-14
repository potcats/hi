# Carrie Ko, Christine Chen, Cindy Liu, Joyce Lin
# hi
# SoftDev
# P02: Makers Makin' It, Act I
# 01/16/2026

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from combat import *
from json import dumps
import random

app = Flask(__name__)
app.secret_key = 'wahhhhhhhhhhhhhhhhh'

# ------------------------ DATABASING  ------------------------ #

# ITEMS
items = ["honey", "cookie", "healing potion", "magical vial of water", "cloth robe", "cloth veil", "cloth leggings", "iron greaves", "iron chestplate", "iron helmet", "iron leggings", "rat hide boots",
        "rat hide cloak", "rat hide hood", "stinger pendant", "ring of goblin ears", "simple sword", "excalibur", "crude club", "noble's sabre"]
img = ["", "", "", "", "/app/static/images/gear/chestplate/cloth.png", "/app/static/images/gear/helmet/cloth.png", "/app/static/images/gear/pants/cloth.png", "/app/static/images/gear/boots/iron.png",
       "/app/static/images/gear/chestplate/iron.png", "/app/static/images/gear/helmet/iron.png", "/app/static/images/gear/pants/iron.png", "/app/static/images/gear/boots/rathide.png",
       "/app/static/images/gear/chestplate/rathide.png", "/app/static/images/gear/helmet/rathide.png", "/app/static/images/gear/accessory/", "/app/static/images/gear/accessory/",
       "/app/static/images/gear/weapon/", "/app/static/images/gear/weapon/", "/app/static/images/gear/weapon/", "/app/static/images/gear/weapon/"]
statStr = [0, 0, 0, 0, 0, 0, 3, 4, 2, 4, 0, 0, 0, 0, 5, 3, 16, 12, 10, 0]
statDex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 2, 0, 5, 0, 0, 0, 0, 0]
statCon = [0, 0, 0, 0, 0, 0, 1, 6, 2, 3, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0]
statInt = [0, 0, 0, 6, 0, 3, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0]
statFth = [0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0]
statLck = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hpInc = [5, 3, 18, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
gold = [5, 5, 20, 10, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 20, 20, 5, 30, 30, 30]
type = ["consumable", "consumable", "consumable", "consumable", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear"]
gearType = ["", "", "", "", "chestplate", "helmet", "pants", "shoes", "chestplate", "helmet", "pants", "shoes", "chestplate", "helmet", "accessory", "accessory", "weapon", "weapon", "weapon", "weapon"]

# ENEMIES
species = ["bandit", "bee", "dwarf", "dwarfchief", "goblin", "grandma", "pebble", "pixie", "rat", "wizard"]
attacks = ["", "", "", "", "", "", "", "", "", ""]

# ENCOUNTERS
name = ["Travelling Merchant", "Elven Camp", "Wanderer's Wares", "Busted Caravan", "Grandma's house", "Wizard Tower",
       "The Sword in the Stone", "Potion Seller"]
dialogue = []
background = ["/static/images/bgs/caravanshop.jpg",
              "/static/images/bgs/dwarvencamp.jpg",
              "/static/images/bgs/forestshop.jpg",
              "/static/images/bgs/tippedcaravan.jpg",
              "/static/images/bgs/grandmahouse.jpg",
              "/static/images/bgs/insidetower.jpg",
              "/static/images/bgs/swordstone.jpg",
              "/static/images/bgs/witchhouse.jpg"]
desc = ["A merchant with a well-worn wagon waves you down (shop)",
        "You see a bunch of sad, depressed elves in a sad, depressed camp",
        "You spot a friendly person with a strange stand in the middle of the woods (shop)",
        "You spot a tipped caravan",
        "You spot the home of an old woman",
        "You spot a wizard tower in the woods",
        "You spot a familiar sword plunged into a rock",
        "You spot a strange hut in the woods"]
diff = [1, 2, 1, 3, 2, 2, 1, 1]

# ATTACKS

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS player (
    username TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    level INTEGER NOT NULL,
    hp INTEGER NOT NULL,
    attacks TEXT NOT NULL,
    buff TEXT,
    debuff TEXT,
    str INTEGER,
    dex INTEGER,
    con INTEGER,
    inte INTEGER,
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
    species TEXT PRIMARY KEY NOT NULL,
    attacks TEXT NOT NULL,
    hp INTEGER NOT NULL,
    weakness TEXT,
    res TEXT,
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
    inte INTEGER,
    fth INTEGER,
    lck INTEGER,
    hpInc INTEGER,
    gold INTEGER,
    gearType TEXT
);
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS attacks (
    name TEXT PRIMARY KEY NOT NULL,
    level INTEGER NOT NULL,
    energy TEXT,
    cd INTEGER NOT NULL,
    scale TEXT,
    statusEffects TEXT,
    baseDamage INTEGER
);
""")

for i in range(len(items)):
    q = "INSERT OR REPLACE INTO items(name, type, image, str, dex, con, inte, fth, lck, hpInc, gold, gearType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    d = (items[i], type[i], img[i], statStr[i], statDex[i], statCon[i], statInt[i], statFth[i], statLck[i], hpInc[i], gold[i], gearType[i])
    c.execute(q, d)
    db.commit()

# test test test!!!!!!!!!!!!!!!!!!)
# c.execute("""
# INSERT or REPLACE INTO enemies
# (species, attacks, hp, weakness, res, drops)
# VALUES (?, ?, ?, ?, ?, ?)
# """, (
#     "goblin",
#     "slash,stab",
#     12,
#     "help",
#     "help",
#     "gold"
# ))
# db.commit()
#
# c.execute("""
# INSERT or REPLACE INTO player
# (username, password, level, hp, attacks, weapon)
# VALUES (?, ?, ?, ?, ?, ?)
# """, (
#     "tester",
#     "pass",
#     1,
#     12,
#     "slash, hit",
#     "help",
# ))
# db.commit()

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

                c.execute("INSERT INTO player VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (request.form['username'].lower(),
                        request.form['password'],
                        0, 30, "strike,cross slash", "",
                        "", 0, 3, 0, 0,
                        0, 0, "", "",
                        "", "", "simple sword", "", "", ""))
                db.commit()

                session.clear()
                session.permanent = True
                session['username'] = request.form['username'].lower()
                return redirect(url_for('menu'))
    return render_template("register.html")

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    session['turn'] = 1
    session['inventory'] = {} # [name] {name, type, quantity, gold}
    session['gold'] = 0

    return render_template("menu.html")

@app.route('/campfire', methods=['GET', 'POST'])
def campfire():
    # for testing purposes
    session['hp'] = 10
    session['currXP'] = 13
    session['maxXP'] = 27
    addItemToInventory("rat hide cloak")

    inv = session['inventory'] # [name] {name, type, quantity, gold}
    stats = fetch_stats() # [level, HP, str, dex, con, int, fth, lck]
    equips = fetch_equips() # [gearType] {name}

    # AJAX INTERACTIONSSSSSSSSSSSSSS
    if request.method == "POST":
        data = request.headers

        if 'select' in data:
            info = data['select'].split(",") # [type, name]

            if info[0] == "consumable":
                results = fetch_itemEffects(info[1])
            elif info[0] == "gear":
                results = fetch_itemStats(info[1])

            return dumps(results)

        # if 'sell' in data:
        #
        #
        # if 'use' in data:


        if 'equip' in data:
            itm = data['equip']

            stats = fetch_itemStats(itm)
            updateStats(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5])
            equipGear(itm)

            equips = fetch_equips()
            return dumps(equips)

        if 'unequip' in data:
            itm = data['unequip']
            gear = equips[itm]

            stats = fetch_itemStats(gear)
            updateStats(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], False)
            unEquipGear(itm)

            equips = fetch_equips()
            return dumps(equips)

    return render_template("campfire.html",
        currTurn=session['turn'],
        username=session['username'],
        inventory=inv,
        equips=equips,
        HP=session['hp'],
        maxHP=stats[1],
        lvl=stats[0],
        currXP=session['currXP'],
        maxXP=session['maxXP'],
        str=stats[2],
        dex=stats[3],
        con=stats[4],
        int=stats[5],
        fth=stats[6],
        lck=stats[7],
        )

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    if not loggedin():
        session['username'] = 'tester'
    #     return redirect(url_for('login'))

    if 'battle' not in session:
        session['battle'] = createBattle([randomEnemy('goblin'), randomEnemy('goblin')])
    #     # placeholder battle state just for rendering
    #     session['battle'] = {
    #         "player": {
    #             "name": "tester",
    #             "hp": 30,
    #             "max_hp": 30, # changes with equipment/stats?
    #             "level": 1,
    #             "energy": 2,
    #             "attacks": ["Atk1", "Atk2", "Atk3"],
    #             "inventory": []
    #         },
    #         "enemies": [
    #             {"species": "goblin", "hp": 10, "max_hp": 10, "energy": 2},
    #             {"species": "bandit", "hp": 10, "max_hp": 10, "energy": 2},
    #             {"species": "pebble", "hp": 10, "max_hp": 10, "energy": 2},
    #         ],
    #         "turn": 1
    #     }

    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        turn_over = False

        if action == 'attack':
            move = data.get('move')
            target = data.get('target')
            session['battle'] = playerAttack(session['battle'], target, move)
            turn_over = True
        elif action == 'item':
            item = data.get('item')
            # session['battle'] = useItem(session['battle'], item)
            # turn_over = True
        elif action == 'focus':
            # session['battle'] = focus(session['battle'])
            # turn_over = True
            pass

        # Enemy Turn
        if turn_over and session['battle']['enemies']:
            session['battle'] = enemyTurn(session['battle'])

        # Player Death Check
        if session['battle']['player']['hp'] <= 0:
            session.pop('battle')
            return jsonify({"redirect": "/menu"})

        return jsonify(session["battle"])

    return render_template("battle.html", battle = session['battle'])

@app.route('/encounters', methods=['GET', 'POST'])
def encounters():
    if not loggedin():
        return redirect(url_for('login'))
    # testttttt
    encounters = []
    for i in range(len(name)):
        encounters.append({
            "id": i,
            "name": name[i],
            "background": background[i],
            "desc": desc[i],
            "diff": diff[i]
        })
    rd = random.sample(encounters, 3)

    return render_template("encounters.html", encounters=rd, turn=session.get("turn", 1))

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

# [helmet, chestplate, pants, boots, weapon, accessory1, accessory2, accessory3]
def fetch_equips():
    gearTypes = ["helmet", "chestplate", "pants", "boots", "weapon", "accessory1", "accessory2", "accessory3"]
    equipDict = {}

    c = db.cursor()
    equips = c.execute('''SELECT helmet,
        chestplate, pants, boots, weapon,
        accessory1, accessory2, accessory3
        FROM player WHERE username = ?''', (session['username'],)).fetchone()

    for i in range(0,len(gearTypes)):
        equipDict[gearTypes[i]] = equips[i]

    return equipDict

def fetch_images(items):
    c = db.cursor()
    images = []

    for item in items:
        image = c.execute("SELECT image FROM items WHERE name = ?", (item,)).fetchone()
        images.append(image)

    return images

# [level, HP, str, dex, con, int, fth, lck]
def fetch_stats():
    c = db.cursor()
    stats = c.execute('''SELECT level, HP, str,
        dex, con, inte, fth, lck
        FROM player WHERE username = ?''', (session['username'],)).fetchone()

    return stats

# [str, dex, con, int, fth, lck]
def fetch_itemStats(name):
    c = db.cursor()
    stats = c.execute('''SELECT str, dex, con, inte, fth, lck
        FROM items WHERE name = ?''', (name,)).fetchone()

    return stats

# [hpIncr, energyIncr]
def fetch_itemEffects(name):
    c = db.cursor()
    effects = c.execute("SELECT hpIncr, energyIncr FROM items WHERE name = ?", (name,)).fetchone()

    return effects

# [name] {name, type, quantity, gold, image}
def addItemToInventory(name):
    inv = session['inventory']

    if name in inv:
        inv[name][2] = str(int(inv[name][2]) + 1)
    else:
        c = db.cursor()
        info = c.execute("SELECT type, gold FROM items WHERE name = ?", (name,)).fetchone()

        inv[name] = [name, info[0], str(1), info[1]]
        session['inventory'] = inv

# sets player stats with new gear
def updateStats(str, dex, con, int, fth, lck, increase=True):
    statTypes = ["str", "dex", "con", "inte", "fth", "lck"]
    addedStats = [str, dex, con, int, fth, lck]
    currStats = fetch_stats()

    user = session['username']
    c = db.cursor()
    for type in statTypes:
        i = statTypes.index(type)
        if addedStats[i] != 0:
            if increase:
                c.execute(f"UPDATE player SET {type} = ? WHERE username = ?",
                    (currStats[2+i] + addedStats[i], user))
            else:
                c.execute(f"UPDATE player SET {type} = ? WHERE username = ?",
                    (currStats[2+i] - addedStats[i], user))

    db.commit()

# sets new piece of gear in player db
def equipGear(gear):
    c = db.cursor()

    type = c.execute("SELECT gearType FROM items WHERE name = ?", (gear,)).fetchone()[0]
    c.execute(f"UPDATE player SET {type} = ? WHERE username = ?",
        (gear, session['username'],))

    db.commit()

# removes gear from player db
def unEquipGear(gearType):
    c = db.cursor()

    c.execute(f"UPDATE player SET {gearType} = '' WHERE username = ?",
        (session['username'],))

    db.commit()

# ------------------------------------------------------------------------- #


# RUN FLASK
if __name__=='__main__':
    app.debug = True
    app.run()
