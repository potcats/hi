# Carrie Ko, Christine Chen, Cindy Liu, Joyce Lin
# hi
# SoftDev
# P02: Makers Makin' It, Act I
# 01/16/2026

from flask import session
import random
import sqlite3
from flask import session

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
    init = random.randint(0,9)
    hp = base_info[2] + random.randint(-3, 3)
    weakness = base_info[3]
    res = base_info[4]
    drops = base_info[5]

    return {
        "species": species,
        "attacks": attacks,
        "cds": [0] * len(base_info[1]),
        "init": init,
        "hp": hp,
        "max_hp": hp,
        "energy": 1,
        "max_energy": 6,
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
        guard
        focus
    ]
    [
        [
            species
            [
                [
                    [
                        name
                        hits
                        level
                        energy
                        cd
                        scale
                        statusEffects
                        baseDamage
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
    True (True = player alive, False = player dead)
]
'''
def turn_order(battle_id):
    player_init = battle_id[0][2]
    enemy_init = []
    order = ['player']

    for i in range(0, len(battle_id[1])):
        enemy_init.append([i, battle_id[1][i][2]])
    #uh oh now what

def game_lost(battle_id):
    return not battle_id[3]

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
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    for i in attacks_info:
        cmd = "SELECT * FROM attacks WHERE name=?"
        c.execute(cmd, (i,))
        attack_info_array.append(c.fetchone())
    db.close()
    attacks_info = attack_info_array

    player = {
        "username": player_info[0],
        "attacks": attacks_info,
        "cds": [0, 0],
        "init": random.randint(0, 100),
        "hp": player_info[3] + player_info[9],
        "max_hp": player_info[3] + player_info[9],
        "energy": 0,
        "max_energy": 6,
        "level": player_info[2],
        "stats": {
            "str": player_info[7],
            "dex": player_info[8],
            "con": player_info[9],
            "int": player_info[10],
            "fth": player_info[11],
            "lck": player_info[12]
        },
        "guarding": False,
        "focused": False
    }

    return {
        "turn": "player",
        "turnNum": 1,
        "player": player,
        "enemies": enemies,
        "actions": [],
        "ended": False
    }

def player_startTurn(battle_id):
    player = battle_id["player"]

    #guard and focus wear off
    player["guarding"] = False
    player["focused"] = False

    #reduce all cd by 1
    for i in range(3):
        if player["cds"][i] > 0:
            player["cds"][i] -= 1

    #increase energy by 1
    player["energy"] = min(player["energy"] + 1, player["max_energy"])
    return battle_id

#enemy indexed by 0 pls
def enemy_startTurn(battle_id, idx):
    enemy = battle_id["enemies"][idx]
    #reduce all cd by 1
    for i in range(len(enemy["cds"])):
        if enemy["cds"][i] > 0:
            enemy["cds"][i] -= 1

    #increase energy by 1
    enemy["energy"] = min(enemy["energy"] + 1, enemy["max_energy"])
    return battle_id

def guard(battle_id):
    battle_id["player"]["guarding"] = True
    return battle_id

def focus(battle_id):
    player = battle_id["player"]
    player["focused"] = True
    #increase energy by 1
    player["energy"] = min(player["energy"] + 1, player["max_energy"])
    return battle_id

# attack(forest_battle1, 2, 'attack1') means that in forest_battle1, the player is attacking enemy #2 (index from 0) with attack1
def player_attack(battle_id, defender, move):
    attack_info = []

    #get thru array of player's attacks and find the correct one
    for attack_info_temp in battle_id["player"]["attacks"]:
        if attack_info_temp[0] == move:
            attack_info = attack_info_temp

    #remove energy used to cast
    battle_id["player"]["energy"] -= attack_info[3]

    result = dealDamage(battle_id, battle_id["player"], battle_id["enemies"][defender], attack_info)

    #do the hp reduction
    for i in result:
        battle_id["enemies"][defender]["hp"] -= i[1]

    #check for kills
    battle_id = killCheck(battle_id)

    battle_id["actions"] = [{
        "source": "player",
        "target": defender,
        "result": result
    }]
    battle_id["turn"] = "enemy"
    return battle_id

# attack(forest_battle1, 2) means that enemy #2 (index from 0) is attacking
def enemy_attack(battle_id, attacker):
    attacking_enemy_stats = battle_id["enemies"][attacker]
    player_stats = battle_id["player"]
    result = []

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
            result = dealDamage(battle_id, attacking_enemy_stats, battle_id["player"], attack_info)

    #do the hp reduction
    for i in result:
        battle_id["player"]["hp"] -= i[1]

    #check for death
    if deathCheck(battle_id):
        battle_id["ended"] = True

    return result

# [['blocked', 50], ['', 100], ['crit', 200], ['dodged', 0]]
# [['', 400]]
def dealDamage(battle_id, attacker, victim, attack_info):
    num_of_hits = attack_info[1]
    all_hits =[]
    for i in range(0,num_of_hits):
        all_hits.append(hit(battle_id, attacker, victim, attack_info))
    return all_hits

# ['blocked', 50]
# ['', 100]
# ['crit', 200]
# ['dodged', 0]
def hit(battle_id, attacker, victim, attack_info):
    status = ''
    #have yet to figure out what 'scale' is and how to use it
    dmg = attack_info[7]/attack_info[1]

    dodge = random.randint(0,100)
    crit = random.randint(0,100)
    block = random.randint(0,100)

    dodgeIncrease = 0
    blockIncrease = 0
    critIncrease = 0
    critDmgIncrease = 0
    dmgMultiplier = 1

    #if victim is the player
    if "species" not in victim:
        strength = victim["stats"]["str"]
        dexterity = victim["stats"]["dex"]
        constitution = victim["stats"]["con"]
        dodgeIncrease = 0.175*(dexterity)
        blockIncrease = 0.375*(strength + constitution)
        if victim["guarding"]:
            dmgMultiplier = 0.5
        elif victim["focused"]:
            dmgMultiplier = 1.3
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
        dmg *= (1.5 + (critDmgIncrease/100))
    if block <= (5 + blockIncrease):
        status = 'blocked'
        dmg /= 2
    dmg *= dmgMultiplier
    return [status, dmg]

def killCheck(battle_id):
    #for enemies
    for i in range(len(battle_id["enemies"]) - 1, -1, -1):
        if battle_id["enemies"][i]["hp"] <= 0:
            battle_id["enemies"].pop(i)
    return battle_id

def deathCheck(battle_id):
    #for player
    if battle_id["player"]["hp"] <= 0:
        return True
    return False

def advance_turn(battle):
    battle["actions"] = []

    # Enemy Turn
    if battle["turn"] == "enemy":
        for i, enemy in enumerate(battle["enemies"]):
            if enemy["hp"] > 0:
                battle = enemy_startTurn(battle, i)
                result = enemy_attack(battle, i)
                battle["actions"].append({
                    "source": "enemy",
                    "enemy_idx": i,
                    "result": result
                })
                if deathCheck(battle):
                    battle["ended"] = True
                    return battle

        battle["turn"] = "player"
        battle["turnNum"] += 1
        return battle

    else:
        # start of player turn
        battle = player_startTurn(battle)
        battle["turn"] = "player"
        return battle
