from flask import Flask,request,flash,render_template,redirect,url_for,g,current_app,session
from app.db import search_in_Cname,search_in_Sname,search_in_Sno,search_all
from app import app
import math

PAGESIZE = app.config["PAGESIZE"]


@app.before_request
def get_info():
    if 'page' not in session or session["keyword"] != request.args.get("keyword",None):
        session["page"] = 1
    session["mode"] = request.args.get("mode","all")
    session["keyword"] = request.args.get("keyword",None)
    session["page"] += int(request.args.get("rsvpage",0))
    if 'pages' in session and session["page"] > session['pages']:
        session["page"] = session['pages']
    if session["page"] <=0:
        session["page"] = 1

def table_slice():
    size = len(current_app.table) - PAGESIZE * session["page"]
    if size >= 0:
        return current_app.table[PAGESIZE * (session["page"]-1):PAGESIZE *session["page"]]
    else:
        return current_app.table[PAGESIZE * (session["page"]-1):]

def get_table():
    mode = session["mode"]
    if mode == "all":
        table=search_all()
    elif mode == 'Sno':
        table = search_in_Sno()
    elif mode == 'Sname':
        table = search_in_Sname();
    else:
        table = search_in_Cname()
    return table

@app.route("/",methods=["GET"])
@app.route("/search",methods=["GET"])
def index():
    error =None
    if session["keyword"] is None and session["mode"] !="all":
        error = 'please input keyword'
    if error is not None:
        flash(error)
        return render_template("index.html")
    current_app.table = get_table()
    session["pages"] = math.ceil(len(current_app.table)/PAGESIZE)
    return render_template("index.html",table=table_slice())

@app.route("/hello")
def hello():
    return "hello world"


@app.route("/change",methods=["POST","GET"])
def change():
    return redirect("/")
