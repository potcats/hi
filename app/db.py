# Carrie Ko, Christine Chen, Cindy Liu, Joyce Lin
# hi
# SoftDev
# P02: Makers Makin' It, Act I
# 01/16/2026

import sqlite3

DB_FILE = "data.db"

def init_db():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS player (
        username TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        level INTEGER NOT NULL,
        energy INTEGER NOT NULL,
        hp INTEGER NOT NULL,
        class TEXT NOT NULL,
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
        id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
        type TEXT NOT NULL,
        attacks TEXT NOT NULL,
        maxInit INTEGER NOT NULL,
        hp INTEGER NOT NULL,
        maxEnergy INTEGER,
        weakness TEXT,
        advantage TEXT
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
        type TEXT NOT NULL,
        baseEnergy INTEGER NOT NULL,
        maxInit INTEGER NOT NULL,
        hp INTEGER NOT NULL,
        weaponType TEXT NOT NULL
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS encounters (
        id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
        type TEXT NOT NULL,
        dialogue TEXT NOT NULL,
        background TEXT NOT NULL,
        description TEXT NOT NULL,
        prereq TEXT
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
        type TEXT NOT NULL,
        recipe TEXT NOT NULL,
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level INTEGER NOT NULL,
        reqEnergy INTEGER NOT NULL,
        cooldown INTEGER NOT NULL,
        scale TEXT NOT NULL,
        effects TEXT,
        baseDamage INTEGER NOT NULL
    );
    """)

    db.commit()
    db.close()
