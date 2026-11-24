from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, create_engine
from flask_sqlalchemy import SQLAlchemy




# create database
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# configure table
class JobListing(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    site: Mapped[str] = mapped_column(String)
    cv_stage: Mapped[str] = mapped_column(String, nullable=True)
    interview_stage: Mapped[str] = mapped_column(String, nullable=True)



# from flask import Flask, render_template, url_for, request, redirect
# from flask_bootstrap import Bootstrap5
#
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job-listings.db'
#
# Bootstrap5(app)
# db.init_app(app)
#
# with app.app_context():
#     db.create_all()
#
#
# import sqlite3
# import csv
#
# con = sqlite3.connect('job-listings.db')
# outfile = open('job_applications.csv', 'w', newline='') # before Py 3.1 use 'wb' **
# outcsv = csv.writer(outfile)
#
# cursor = con.execute('select * from job-listing')
#
# # dump column titles (optional)
# # outcsv.writerow(x[0] for x in cursor.description)
# # dump rows
# outcsv.writerows(cursor.fetchall())
#
# outfile.close()
#
#
#
# # app.run(debug=True)