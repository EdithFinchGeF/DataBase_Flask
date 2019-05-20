# coding=utf-8
import sqlite3
from app import app
from flask import current_app,g,session,request
import os
import click

database = app.config["DATABASE"]

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(database)
    return g.db

    

@app.teardown_request
def close_db(* args):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def table_format(table):
    table=[{"Sno":Sno.strip(),"Sname":Sname.strip(),"Cname":Cname.strip(),"Score":Score} 
        for Sno,Sname,Cname,Score in table]
    return table


def search_in_Sno():
    Sno =session["keyword"]
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        select S.Sno,Sname,C.Cname,G.Score
        from Student S,Grade G,Course C
        where S.Sno = G.Sno
        and   G.Cno = C.Cno
        and   S.sno = ?
    ''',(Sno,))
    table=table_format(cur.fetchall())
    return table


def search_in_Cname():
    Cname =session["keyword"]
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        select S.Sno,Sname,C.Cname,G.Score
        from Student S,Grade G,Course C
        where S.Sno = G.Sno
        and   G.Cno = C.Cno
        and   C.Cname = ?
    ''',(Cname,))
    table=table_format(cur.fetchall())
    return table

def search_in_Sname():
    Sname =session["keyword"]
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        select S.Sno,Sname,C.Cname,G.Score
        from Student S,Grade G,Course C
        where S.Sno = G.Sno
        and   G.Cno = C.Cno
        and   S.Sname = ?
    ''',(Sname,))
    table=table_format(cur.fetchall())
    return table

def search_all():
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        select S.Sno,Sname,C.Cname,G.Score
        from Student S,Grade G,Course C
        where S.Sno = G.Sno
        and   G.Cno = C.Cno
    ''')
    table=table_format(cur.fetchall())
    return table