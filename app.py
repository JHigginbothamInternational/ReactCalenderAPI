from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://rvtkktuigkomfv:53e9c6d28c24ee7ce964381485ea8bfd6eca6ff4ad123feb167cadfe3ab47fa7@ec2-35-153-35-94.compute-1.amazonaws.com:5432/d8bfqo72lhellv"

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

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self, day, month, year, text):
        self.day = day
        self.month = month
        self.year = year
        self.text = text

class MonthSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "year", "days_in_month", "days_in_previous_month", "start_day")

month_schema = MonthSchema()
multiple_month_schema = MonthSchema(many=True)

class ReminderSchema(ma.Schema):
    class Meta:
        fields = ("id", "day", "month", "year", "text")

reminder_schema = ReminderSchema()
multiple_reminder_schema = ReminderSchema(many=True)

month_schema = MonthSchema()
multiple_month_schema = MonthSchema(many=True)


@app.route('/month/add', methods=(["POST"]))
def add_month():
    post_data = request.get_json()
    name = post_data["name"]
    year = post_data["year"]
    days_in_month = post_data["days_in_month"]
    days_in_previous_month = post_data["days_in_previous_month"]
    start_day = post_data["start_day"]

    record = Month(name, year, days_in_month, days_in_previous_month, start_day )
    db.session.add(record)
    db.session.commit()

    return jsonify("Month Added")

@app.route('/month/add/multiple', methods=(["POST"]))
def add_multiple_months():
    post_data = request.get_json()

    for month_data in post_data:
        record_check = db.session.query(Month).filter(Month.name == month_data["name"]).filter(Month.year == month_data["year"]).first()

        if record_check is None:
            name = month_data["name"]
            year = month_data["year"]
            days_in_month = month_data["days_in_month"]
            days_in_previous_month = month_data["days_in_previous_month"]
            start_day = month_data["start_day"]

            record = Month(name, year, days_in_month, days_in_previous_month, start_day )
            db.session.add(record)
            db.session.commit()

    return jsonify("Months Added")

@app.route('/month/get', methods=(["GET"]))
def get_all_months():
    records = db.session.query(Month).all()
    return jsonify(multiple_month_schema.dump(records))

@app.route("/month/get/<year>", methods=(["GET"]))
def get_months_by_year(year):
    records = db.session.query(Month).filter(Month.year == year).all()
    return jsonify(multiple_month_schema.dump(records))

if __name__ == "__main__":
    app.run(debug=True)