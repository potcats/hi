# Carrie Ko, Christine Chen, Cindy Liu, Joyce Lin
# hi
# SoftDev
# P02: Makers Makin' It, Act I
# 01/16/2026

from flask import session
import random
import sqlite3

DB_FILE = "data.db"

# party = player
# enemies = [ [species, attacks, init, hp, energy, weakness, res, drop], [], [] ]
def randomEnemy(species):
    #get enermy info from database
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    cmd = "SELECT * FROM enemies WHERE species=?"
    c.execute(cmd, (species,))
    base_info = list(c.fetchone())
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

    species = species
    attacks = [base_info[1], [0, 0, 0]]
    init = random.randint(0, 100)
    hp = base_info[2] + random.randint(-3, 3)
    weakness = base_info[3]
    res = base_info[4]
    drops = base_info[5]

    return {
        "species": species,
        "attacks": attacks,
        "cds": [0, 0, 0],
        "init": init,
        "hp": hp,
        "max_hp": hp,
        "energy": 1,
        "weakness": weakness,
        "res": res,
        "drops": drops
    }

'''
[ player, [enemies] ]

 |
 V

[
    [
        username
        [
            [
                [
                    name
                    level
                    energy
                    cd
                    scale
                    baseDamage
                    effect
                ]
                attack2
                attack3
            ]
            [0, 0, 0]
        ]
        init
        hp
        energy
        level
        str
        dex
        con
        int
        fth
        lck
    ]
    [
        [
            species
            [
                [
                    [
                        name
                        level
                        energy
                        cd
                        scale
                        baseDamage
                        effect
                    ]
                    attack2
                    attack3
                ]
                [0, 0, 0]
            ]
            init
            hp
            energy
            weakness
            res
            drops
        ]
        enemy2
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
    for i in attacks_info:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        cmd = "SELECT * FROM attacks WHERE name=?"
        c.execute(cmd, (i,))
        attack_info_array.append(c.fetchone())
        db.close()
    attacks_info = attack_info_array

    player = {
        "username": player_info[0],
        "attacks": attacks_info,
        "cds": [0, 0, 0],
        "init": random.randint(0, 100),
        "hp": player_info[3] + player_info[9],
        "max_hp": player_info[3] + player_info[9],
        "energy": 0,
        "level": player_info[2],
        "stats": {
            "str": player_info[7],
            "dex": player_info[8],
            "con": player_info[9],
            "int": player_info[10],
            "fth": player_info[11],
            "lck": player_info[12]
        }
    }

    return {"player": player, "enemies": enemies}

# attack(forest_battle1, 2, 'attack1') means that in forest_battle1, the player is attacking enemy #2 (index from 0) with attack1
def playerAttack(battle_id, defender, move):
    attack_info = []

    #get thru array of player's attacks and find the correct one
    for attack_info_temp in battle_id["player"]["attacks"]:
        if attack_info_temp[0] == move:
            attack_info = attack_info_temp

    #remove energy used to cast
    battle_id["player"]["energy"] -= attack_info[3]

    return dealDamage(battle_id, battle_id["player"], battle_id["enemies"][defender], attack_info)

# attack(forest_battle1, 2) means that enemy #2 (index from 0) is attacking
def enemyAttack(battle_id, attacker):
    attacking_enemy_stats = battle_id["enemies"][attacker]
    player_stats = battle_id["player"]

    #reduce all cd by 1
    for i in range(0,3):
        if attacking_enemy_stats["cds"][i] > 0:
            attacking_enemy_stats["cds"][i] -= 1

    #increase energy by 1
    attacking_enemy_stats["energy"] += 1

    #check available attacks and respective cooldowns, use the highest available attack
    for i in range(len(attacking_enemy_stats["attacks"][0]) - 1, -1, -1):
        #get array containing info for each attack
        attack_info = attacking_enemy_stats["attacks"][0][i]
        enemy_energy = attacking_enemy_stats["energy"]
        attack_current_cd = attacking_enemy_stats["cds"][i]
        if enemy_energy >= attack_info[3] and attack_current_cd == 0:
            #set cd
            attacking_enemy_stats["cds"][i] = attack_info[4]
            #remove energy used to cast
            attacking_enemy_stats["energy"] -= attack_info[3]

            return dealDamage(battle_id, attacking_enemy_stats, battle_id["player"], attack_info)

    return "enemy attack calculations failed"

# ['blocked', 50]
# ['', 100]
# ['crit', 200]
# ['dodged', 0]
def dealDamage(battle_id, attacker, victim, attack_info):
    status = ''
    dmg = attack_info[7]

    dodge = random.randint(0,100)
    crit = random.randint(0,100)
    block = random.randint(0,100)

    dodgeIncrease = 0
    blockIncrease = 0
    critIncrease = 0
    critDmgIncrease = 0

    #if victim is the player
    if "species" not in victim:
        strength = victim["stats"]["str"]
        dexterity = victim["stats"]["dex"]
        constitution = victim["stats"]["con"]
        dodgeIncrease = 0.175*(dexterity)
        blockIncrease = 0.375*(strength + constitution)
    #if victim is npc
    else:
        strength = attacker["stats"]["str"]
        dexterity = attacker["stats"]["dex"]
        intelligence = attacker["stats"]["int"]
        luck = attacker["stats"]["lck"]
        critIncrease = 0.125*(strength) + 0.15*(dexterity) + 0.075*(intelligence) + 0.3*(luck)
        critDmgIncrease = 0.2*(strength) + 0.25*(dexterity) + 0.15*(intelligence) + 0.5*(luck)

    if dodge <= (5 + dodgeIncrease):
        return ['dodged', 0]
    elif crit <= (5 + critIncrease):
        status = 'crit'
        dmg = dmg*(1.5 + (critDmgIncrease/100))
    if block <= (5 + blockIncrease):
        status = 'blocked'
        dmg = dmg/2

    victim["hp"] -= int(dmg)
    return [status, int(dmg)]
