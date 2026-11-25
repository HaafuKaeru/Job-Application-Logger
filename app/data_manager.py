from flask import Blueprint, redirect, url_for, render_template, request
from database import JobListing, db
from sqlalchemy import or_
import csv
import datetime as dt


# helper functions

def db_sort_by(key) -> list[JobListing]:
    table = []
    for entry in db.session.query(JobListing).order_by(key):
        table.append(entry)
    return table

def db_count_all() -> int:
    return db.session.query(JobListing.id).count()

def db_count_ghosted() -> int:
    results = db.session.execute(
        db.select(JobListing).where(
            or_(
                JobListing.cv_stage == "",
                JobListing.cv_stage.contains("?")
            )
        )
    )
    return len(list(results.scalars()))

def db_count_cv_accepted() -> int:
    results = db.session.execute(db.select(JobListing).where(JobListing.cv_stage == "Yes")).scalars()
    return len(list(results))

def db_count_interviews() -> int:
    results = db.session.execute(db.select(JobListing).where(JobListing.interview_stage == "Yes")).scalars()
    return len(list(results))


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


@data.route("/tools/view")
def view():
    sort_by = request.args.get("sort_by")
    table = []
    if sort_by == "date":
        table = db_sort_by(JobListing.date)
    if sort_by == "company":
        table = db_sort_by(JobListing.company)
    if sort_by == "role":
        table = db_sort_by(JobListing.role)
    return render_template("view.html", table=table, sort_by=sort_by)


@data.route("/tools/add")
def add():
    return render_template("add.html")


@data.route("/tools/delete")
def delete():
    JobListing.query.delete()
    db.session.commit()
    return redirect(url_for("tools"))