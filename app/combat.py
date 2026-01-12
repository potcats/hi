# Carrie Ko, Christine Chen, Cindy Liu, Joyce Lin
# hi
# SoftDev
# P02: Makers Makin' It, Act I
# 01/16/2026

# party = player
# enemies = [ [species, attacks, init, hp, energy, weakness, res, drop], [], [] ]
def randomEnemy(type):
    #get enermy info from database
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    cmd = "SELECT * FROM enemies WHERE species=?"
    c.execute(cmd, (type,))
    base_info = c.fetchone()
    db.close()
    base_info[1] = base_info[1].split(',')

    species = type
    attacks = base_info[1]
    init = random.randInt(0, 100)
    hp = base_info[3] + random.randInt(-3, 3)
    energy = 0
    weakness = base_info[3]
    res = base_info[4]
    drop = base_info[5]

    return [species, attacks, init, hp, energy, weakness, res, drop]

'''
[
   [username, level, [attack1, attack2, attack3], init, HP, energy, str, dex, con, int, fth, lck]

   [
        [
            [
                species
                [
                    attack1
                    attack2
                    attack3
                ]
                init
                hp
                energy
                weakness
                res
                drop
            ]
        ]
        [enemy2]
        [enemy3]
    ]
]
'''

# forest_battle1 = createBattle( [randomEnemy('goblin')], [randomEnemy('bee')] )
def createBattle(enemies):
    #get player info from database
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    cmd = "SELECT * FROM player WHERE username=?"
    c.execute(cmd, (session['username'],))
    player_info = c.fetchone()
    db.close()

    #make attacks array
    attacks = player_info[4].split(',')

    player = [player_info[0],
            player_info[2],
            attacks,
            player_info[3] + player_info[7],
            player_info
        ]


# attack(forest_battle1, 2, 'attack1') means that in forest_battle1, the player is attacking enemy #2 (index from 0) with attack1
def attack (battle_id, defender, move):
    att

# attack(forest_battle1, 2) means that enemy #2 (index from 0) is attacking
def attack (battle_id, attacker):
    att
