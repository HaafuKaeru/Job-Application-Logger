from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap5
from database import db, JobListing


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job-listings.db'

Bootstrap5(app)
db.init_app(app)

with app.app_context():
    db.create_all()


# flask routes

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/stats")
def stats():
    return render_template("stats.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)