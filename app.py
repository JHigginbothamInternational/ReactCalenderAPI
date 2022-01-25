from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://gqejerzwvxploc:4fb8b6ecc338728e97443d0e3439e1adadff84951c95692cb0500b01813efc9a@ec2-3-216-113-109.compute-1.amazonaws.com:5432/da0d05h0s7grat"

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    days_in_month = db.Column(db.Integer, nullable=False)
    days_in_previous_month = db.Column(db.Integer, nullable=False)
    start_day = db.Column(db.Integer, nullable=False)

    def __init__(self, name, year, days_in_month, days_in_previous_month, start_day):
        self.name = name
        self.year = year
        self.days_in_month = days_in_month
        self.days_in_previous_month = days_in_previous_month
        self.start_day = start_day

if __name__ == "__main__":
    app.run(debug=True)