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
items = ["honey", "cookie", "healing potion", "magical vial of water", "cloth robe", "cloth veil", "cloth leggings", "iron greaves", 
         "iron chestplate", "iron helmet", "iron leggings", "rat hide boots",
        "rat hide cloak", "rat hide hood", "stinger pendant", "ring of goblin ears", 
         "simple sword", "excalibur", "crude club", "noble's sabre"]
img = ["", "", "", "", "/app/static/images/gear/chestplate/cloth.png", "/app/static/images/gear/helmet/cloth.png", "/app/static/images/gear/pants/cloth.png", "/app/static/images/gear/boots/iron.png",
       "/app/static/images/gear/chestplate/iron.png", "/app/static/images/gear/helmet/iron.png", "/app/static/images/gear/pants/iron.png", "/app/static/images/gear/boots/rathide.png",
       "/app/static/images/gear/chestplate/rathide.png", "/app/static/images/gear/helmet/rathide.png", "/app/static/images/gear/accessory/", "/app/static/images/gear/accessory/",
       "/app/static/images/gear/weapon/", "/app/static/images/gear/weapon/", "/app/static/images/gear/weapon/", "/app/static/images/gear/weapon/"]
statStr = [0, 0, 0, 0, 0, 0, 0, 3, 4, 2, 4, 0, 0, 0, 0, 5, 3, 16, 12, 10]
statDex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 2, 0, 5, 0, 0, 0, 0]
statCon = [0, 0, 0, 0, 0, 0, 0, 1, 6, 2, 3, 0, 0, 0, 0, 0, 0, 0, 6, 0]
statInt = [0, 0, 0, 0, 6, 0, 3, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0]
statFth = [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0]
statLck = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hpInc = [5, 3, 18, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
gold = [5, 5, 20, 10, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 20, 20, 5, 30, 30, 30]
type = ["consumable", "consumable", "consumable", "consumable", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear", "gear"]
gearType = ["", "", "", "", "chestplate", "helmet", "pants", "boots", "chestplate", "helmet", "pants", "boots", "chestplate", "helmet", "accessory", "accessory", "weapon", "weapon", "weapon", "weapon"]

# ENEMIES
species = ["bandit", 
           "bee",
           "dwarf",
           "dwarfchief",
           "goblin",
           "grandma",
           "pebble",
           "pixie",
           "rat",
           "wizard"]
attacks = ["fire bomb,quick slash,light stab",
           "sting,stinger burst",
           "fire bomb,fire thunderbuss",
           "small shieldbreaker,club bash",
           "tiny strike,jugg",
           "pie throw,granny kick,granny kick barrage",
           "boulder bump",
           "dust bolt,wondrous light,magic dust",
           "gnaw,rat flip",
           "spell scroll:magic missile,flame bolt,fireball"]
enemyHP = [16, 17, 25, 35, 15, 55, 12, 17, 7, 60]
weakness = ["str", "", "", "", "str", "str", "", "", "str", "str"]
enemyRes = ["", "", "", "str", "", "", "str", "str", "", ""]
drops = ["cloth veil",
         "honey,stinger pendant",
         "iron greaves,iron helmet",
         "iron chestplate,iron leggings,crude club",
         "cloth robe,cloth leggings,ring of goblin ears,noble's sabre",
         "iron greaves,iron helmet,iron chestplate,iron leggings",
         "healing potion,magical vial of water",
         "rat hide cloak,rat hide hood,rat hide boots",
         "healing potion,magical vial of water,cloth veil,cloth robe,cloth leggings"]

# ENCOUNTERS
name = ["Travelling Merchant",
        "Elven Camp",
        "Wanderer's Wares",
        "Busted Caravan",
        "Grandma's house",
        "Wizard Tower",
        "The Sword in the Stone",
        "Potion Seller",
        "Short Rest",
        "Scavenge"]
background = ["/static/images/bgs/caravanshop.jpg",
              "/static/images/bgs/dwarvencamp.jpg",
              "/static/images/bgs/forestshop.jpg",
              "/static/images/bgs/tippedcaravan.jpg",
              "/static/images/bgs/grandmahouse.jpg",
              "/static/images/bgs/insidetower.jpg",
              "/static/images/bgs/swordstone.jpg",
              "/static/images/bgs/witchhouse.jpg",
              "",
              ""]
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
attackName = ["pie throw", "granny kick", "granny kick barrage",
              "spell scroll: magic missile", "flame bolt", "fireball",
              "fire bomb", "quick slash", "light stab", 
              "tiny strike", "jugg", 
              "fire thunderbuss", "hook slash", "small shieldbreaker",
              "boulder bump",
              "sting", "stinger burst",
              "dust bolt", "wondrous light", "magic dust",
              "boop", "swipe", "bark", "nom",
              "gnaw", "rat flip"
              "strike", "cross slash", "rally", "heavy strike", "guard"]
hits =   [1, 1, 4, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1 ,2, 0, 1, 0]
energy = [1, 0, 2, 1, 0, 2, 1, 0, 1, 0, 1, 0, 0, 2, 0, 0, 2, 0, 2, 1, 1, 0, 2, 2, 0, 2, 0, 2, 3, 1, 0]
level =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 0]
cd =     [2, 0, 3, 4, 0, 3, 0, 0, 2, 0, 0, 0, 0, 4, 0, 0, 3, 0, 2, 5, 3, 0, 2, 4, 0, 4, 0, 4, 6, 5, 0]
scale = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "str", "str", "str", "str", ""]
statusEff = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "dmgUP", "", "defUP"]
baseDmg = [12, 8, 4, 3, 6, 8, 6, 4, 5, 4, 7, 8, 10, 14, 3, 3, 4, 6, 9, 0, 6, 14, 8, 17, 3, 6, 6, 9, 0, 15, 0]

# DIALOGUE
scene = ["Busted Caravan",
         "Busted Caravan",
         "Busted Caravan",
         "Busted Caravan",
         "Busted Caravan",
         "Busted Caravan",
         "Busted Caravan",
         "Busted Caravan",
         "Busted Caravan",
         "Busted Caravan",
         "Busted Caravan",
         "Busted Caravan"]
dialogueType = ["desc", "choice", "choice", "choice", 
                "desc", "choice", "choice",
                "desc", "desc", "choice", "desc", "choice"]
dlg = ["You find yourselves peeking through the trees towards a caravan that seems to have been stranded in the middle of the forest. What will you do?",
       "Battle the goblins for their goods",
       "Approach the goblin caravan",
       "Walk away from the scene",
       "A goblin walks up to stand between you and the caravan. ‘Hello, traveler. Our caravan tipped over, but we have to deliver these goods by nightfall. We would be grateful for your help.’",
       "Help the goblins repair the caravan (STR)",
       "Nah, they got it", 
       "The goblins cheer and get ready to go. ‘You have our gratitude. Here, have this.’",
       "The goblins look at you impatiently. ‘You’re just here to hold us up, aren’t you?’",
       "Fight the goblins",
       "Fine! We'll make it work...",
       "Move on from the scene"]
ord = [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3]
prevChoice = ["", "", "", "", "B", "B", "B", "A", "A", "A", "B", "B"]
currChoice = ["", "A", "B", "C", "", "A", "B", "", "", "", "", ""]
stat = ["", "", "", "", "", "str", "", "pass", "fail", "", "", ""]
statReq = [0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0]
reward = ["", "", "", "", "", "", "", "gold", "", "", "", 0]

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
    background TEXT NOT NULL,
    desc TEXT NOT NULL,
    diff INTEGER NOT NULL
);
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS dialogue (
    scene TEXT NOT NULL,
    type TEXT NOT NULL,
    dlg TEXT NOT NULL,
    ord INTEGER,
    prevChoice TEXT,
    currChoice TEXT,
    stat TEXT,
    statReq INTEGER,
    reward TEXT
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
    hits INTEGER NOT NULL,
    level INTEGER NOT NULL,
    energy INTEGER,
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
         
for i in range(len(species)):
    q = "INSERT OR REPLACE INTO enemies(species, attacks, hp, weakness, res, drops) VALUES (?, ?, ?, ?, ?, ?)"
    d = (species[i], attacks[i], enemyHP[i], weakness[i], enemyRes[i], drops[i])
    c.execute(q, d)
    db.commit()

for i in range(len(attackName)):
    q = "INSERT OR REPLACE INTO attacks(name, hits, level, energy, cd, scale, statusEffects, baseDamage) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    d = (attackName[i], hits[i], level[i], energy[i], cd[i], scale[i], statusEff[i], baseDmg[i])
    c.execute(q, d)
    db.commit()

for i in range(len(name)):
    q = "INSERT OR REPLACE INTO encounters(type, background, desc, diff) VALUES (?, ?, ?, ?)"
    d = (name[i], background[i], desc[i], diff[i])
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
                    return render_template("register.html", invalid="Duplicate username")
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
                        "", 3, 0, 0, 0,
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
    session['hp'] = fetch_stats()[1]
    session['statPoints'] = 0

    addItemToInventory("simple sword")

    return render_template("menu.html")

@app.route('/campfire', methods=['GET', 'POST'])
def campfire():
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

        if 'sell' in data:
            item = data['sell']
            session['gold'] = session['gold'] + inv[item][3]

            inv[item][2] = str(int(inv[item][2]) - 1)

            if int(inv[item][2]) == 0:
                inv.pop(item)

            newGold = session['gold']
            return str(newGold)

        if 'use' in data:
            consumable = data['use']
            session['hp'] = session['hp'] + fetch_itemEffects(consumable)
            if session['hp'] > stats[1] + stats[4]:
                session['hp'] = stats[1] + stats[4]

            inv[consumable][2] = str(int(inv[consumable][2]) - 1)

            if int(inv[consumable][2]) == 0:
                inv.pop(consumable)

        if 'equip' in data:
            itm = data['equip']

            itemStats = fetch_itemStats(itm)
            updateStats(itemStats[0], itemStats[1], itemStats[2], itemStats[3], itemStats[4], itemStats[5])

            equipGear(itm)

            equips = fetch_equips()
            return dumps(equips)

        if 'unequip' in data:
            itm = data['unequip']
            gear = equips[itm]

            itemStats = fetch_itemStats(gear)
            updateStats(itemStats[0], itemStats[1], itemStats[2], itemStats[3], itemStats[4], itemStats[5], False)

            unEquipGear(itm)

            equips = fetch_equips()
            return dumps(equips)

        if 'stats' in data:
            currStats = list(fetch_stats())
            currStats[1] = session['hp']

            return dumps(currStats)

        if 'points' in data:
            newStats = data['points'].split(",")
            updateStats(newStats[0], newStats[1], newStats[2], newStats[3], newStats[4], newStats[5])

    return render_template("campfire.html",
        currTurn=session['turn'],
        username=session['username'],
        inventory=inv,
        equips=equips,
        HP=session['hp'],
        maxHP=stats[1],
        lvl=stats[0],
        gold=session['gold'],
        str=stats[2],
        dex=stats[3],
        con=stats[4],
        int=stats[5],
        fth=stats[6],
        lck=stats[7],
        statPoints = session['statPoints'],
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

@app.route('/shop/<string:type>', methods=['GET', 'POST'])
def shop(type):
    bg = fetch_bg(type)

    return render_template("shop.html",
        bg=bg,)

@app.route('/dialogue', methods=['GET', 'POST'])
def dialogue():

    return render_template("dialogue.html", )

@app.route('/scavenge', methods=['GET', 'POST'])
def scavenge():
    consumables = ["honey", "cookie", "healing potion", "magical vial of water"]
    gear = [ "cloth robe", "cloth veil", "cloth leggings",
            "iron greaves", "iron chestplate", "iron helmet", "iron leggings",
            "rat hide boots", "rat hide cloak", "rat hide hood" ]
    number = random.randint(1, 100)

    if request.method == "POST":
        if number < 96:
            item = random.choice(consumables)
        else:
            item = random.choice(gear)

        addItemToInventory(item)
        return item

    return render_template("scavenge.html")

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
        image = c.execute("SELECT image FROM items WHERE name = ?", (item,)).fetchone()[0]
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

# [hpInc, energyIncr]
def fetch_itemEffects(name):
    c = db.cursor()
    effects = c.execute("SELECT hpInc FROM items WHERE name = ?", (name,)).fetchone()

    return effects[0]

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
    currEquips = fetch_equips()

    type = c.execute("SELECT gearType FROM items WHERE name = ?", (gear,)).fetchone()[0]
    if currEquips[type] != "":
        itemStats = fetch_itemStats(currEquips[type])
        updateStats(itemStats[0], itemStats[1], itemStats[2], itemStats[3], itemStats[4], itemStats[5], False)

    c.execute(f"UPDATE player SET {type} = ? WHERE username = ?",
        (gear, session['username'],))

    db.commit()

# removes gear from player db
def unEquipGear(gearType):
    c = db.cursor()

    c.execute(f"UPDATE player SET {gearType} = '' WHERE username = ?",
        (session['username'],))

    db.commit()

# fetches encounter background
def fetch_bg(name):
    c = db.cursor()
    name = " ".join(name.split("%20"))

    bg = c.execute("SELECT background FROM encounters WHERE type = ?", (name,)).fetchone()[0]
    return bg

# leveling up!!!!!!!!!!!!!!!!!!!!
def lvlup(battle, currlvl):
    c = db.cursor()

    diffMultiplier = c.execute("SELECT diff FROM encounters WHERE type = ?", (battle,)).fetchone()
    if diffMultiplier is not None:
        diffMultiplier = diffMultiplier[0]
    else:
        diffMultiplier = 1

    session['statPoints'] = session['statPoints'] + (3 * diffMultiplier)

    c.execute("UPDATE player SET level = ? WHERE username = ?",
        (currlvl + diffMultiplier, session['username']))

# ------------------------------------------------------------------------- #


# RUN FLASK
if __name__=='__main__':
    app.debug = True
    app.run()
