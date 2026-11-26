from flask import Blueprint, redirect, url_for, render_template, request
from sql import JobListing, db, db_sort_by
import csv
import datetime as dt


data = Blueprint("data", __name__)


@data.route("/import_csv")
def import_csv():
    filename = "job_applications.csv"
    with open(filename, newline="") as csvfile:
        file_reader = csv.reader(csvfile)
        header = next(file_reader, None)
        for line in file_reader:
            entry = JobListing(
                **{header[i]: line[i] for i in range(len(line))}
            )
            entry.date = dt.datetime.strptime(entry.date, "%d/%m/%Y")
            db.session.add(entry)
            db.session.commit()
    return redirect(url_for("tools"))


@data.route("/tools/database")
def database():
    sort_by = request.args.get("sort_by")
    table = []
    if sort_by == "date":
        table = db_sort_by(JobListing.date)
    if sort_by == "company":
        table = db_sort_by(JobListing.company)
    if sort_by == "role":
        table = db_sort_by(JobListing.role)
    return render_template("database.html", table=table, sort_by=sort_by)


@data.route("/tools/add")
def add():
    return render_template("add.html")


@data.route("/tools/delete")
def delete():
    JobListing.query.delete()
    db.session.commit()
    return redirect(url_for("tools"))