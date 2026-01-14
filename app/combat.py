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

    #process attack names to get array with attack information
    attack_info = []
    for i in base_info[1]:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        cmd = "SELECT * FROM attacks WHERE name=?"
        c.execute(cmd, (i,))
        attack_info.append(c.fetchone())
        db.close()
    base_info[1] = attack_info

    species = type
    attacks = [base_info[1], [0, 0, 0]]
    init = random.randInt(0, 100)
    hp = base_info[3] + random.randInt(-3, 3)
    weakness = base_info[3]
    res = base_info[4]
    drop = base_info[5]

    return [species, attacks, init, hp, 0, weakness, res, drops]

'''
[ player, [enemies] ]

 |
 V

[
    [username, level, [ [ [name, level, energy, cd, scale, baseDamage, effect], attack2, attack3], [0, 0, 0] ], init, hp, energy, str, dex, con, int, fth, lck, [cd0, cd1, cd2]],
    [
        [
            species,
            [
                [
                    [
                        name,
                        level,
                        energy,
                        cd, <-- max cooldown
                        scale,
                        baseDamage,
                        effect
                    ]
                    attack2,
                    attack3
                ]
                [0, 0, 0]
            ]
            init,
            hp,
            energy,
            weakness,
            res,
            drops
        ]
        enemy2,
        enemy3
    ]
]
'''

# forest_battle1 = createBattle( [randomEnemy('goblin'), randomEnemy('bee')] )
def createBattle(enemies):
    #get player info from database
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    cmd = "SELECT * FROM player WHERE username=?"
    c.execute(cmd, (session['username'],))
    player_info = c.fetchone()
    db.close()

    #make attacks array
    attacks_info = player_info[4].split(',')

    #process attack names to get array with attack information
    attack_info_array = []
    for i in attacks_info[1]:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        cmd = "SELECT * FROM attacks WHERE name=?"
        c.execute(cmd, (i,))
        attack_info_array.append(c.fetchone())
        db.close()
    attacks_info = attack_info_array

    player = [player_info[0],
            player_info[2],
            [attacks_info, [0, 0, 0]],
            random.randInt(0, 100),
            player_info[3] + player_info[11],
            0,
            player_info[9],
            player_info[10],
            player_info[11],
            player_info[12],
            player_info[13],
            player_info[14]
        ]

    return [player, enemies]


# attack(forest_battle1, 2, 'attack1') means that in forest_battle1, the player is attacking enemy #2 (index from 0) with attack1
def attack(battle_id, defender, move):
    att

# attack(forest_battle1, 2) means that enemy #2 (index from 0) is attacking
def attack(battle_id, attacker):
    attacking_enemy_stats = battle_id[1][attacker]
    player_stats = battle_id[0]

    #reduce all cd by 1
    for i in attacking_enemy_stats[1][1]:
        if i != 0:
            i -= 1
    #increase energy by 1
    attacking_enemy_stats[4] += 1

    #check available attacks and respective cooldowns, use the highest available attack
    for i in range(2, -1, -1):
        if attacking_enemy_stats[1][0][i][2] >= attacking_enemy_stats[4] and attacking_enemy_stats[1][1][i] == 0:
            #set cd
            attacking_enemy_stats[1][1][i] = attacking_enemy_stats[1][0][i][3]

#
def dealDamage(attacker, victim, attack_info):
    dodgeChance = random.randInt(0,100)
    # if dodgeChance > 95:

    #flat dodge chance
    #base dmg
    #crit chance -> base dmg x multiplier
    #block change -> base dmg x multiplier / 2
