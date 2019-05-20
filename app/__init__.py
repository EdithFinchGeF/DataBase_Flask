from flask import Flask
from config import Config
import os
import click
app= Flask(__name__)
app.config.from_object(Config)

@app.cli.command()
def init_db():
    from .db import get_db
    with app.app_context():
        db = get_db()
        with open(os.path.join(app.root_path,"schema.sql"),encoding="utf-8") as f:
            db.executescript(f.read())
        db.commit()
    click.echo("init successfully")

from . import routes
