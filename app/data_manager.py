from flask import Blueprint, redirect, url_for, render_template, request
from sql import JobListing, db, db_sort_by
from forms import AutoEntry, ManualEntry
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


@data.route("/tools/add", methods=['POST'])
def add_auto():
    auto_form = AutoEntry()
    # if auto_form.scrape.data and auto_form.validate():
    #     print("ok this works")
    if auto_form.validate_on_submit():
        print("auto validated")
        return redirect(url_for("data.database", sort_by="date"))
    return render_template("add.html", auto_form=auto_form, manual_form=ManualEntry())


@data.route("/tools/add", methods=['POST'])
def add_manual():
    manual_form = ManualEntry()
    if manual_form.validate_on_submit():
        print("manual validated")
        return redirect(url_for("data.database", sort_by="date"))
    return render_template("add.html", auto_form=AutoEntry(), manual_form=manual_form)


@data.route("/tools/delete")
def delete():
    JobListing.query.delete()
    db.session.commit()
    return redirect(url_for("tools"))