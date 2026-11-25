from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from database import db

from data_manager import data, db_count_all, db_count_ghosted, db_count_cv_accepted, db_count_interviews


app = Flask(__name__)
app.register_blueprint(data)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job-listings.db'

Bootstrap5(app)
db.init_app(app)

with app.app_context():
    db.create_all()


# flask routes

@app.route("/")
def home():
    total = db_count_all()
    ghosted = db_count_ghosted()
    cv_accepted = db_count_cv_accepted()
    interviews = db_count_interviews()
    info = {
        "total": total,
        "ghosted": ghosted,
        "cv_accepted": cv_accepted,
        "interviews": interviews,
    }
    return render_template("index.html", **info)


@app.route("/stats")
def stats():
    return render_template("stats.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tools")
def tools():
    return render_template("tools.html")


if __name__ == '__main__':
    app.run(debug=True)