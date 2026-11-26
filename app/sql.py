from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Date, or_
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
    date: Mapped[str] = mapped_column(Date)
    site: Mapped[str] = mapped_column(String)
    cv_stage: Mapped[str] = mapped_column(String, nullable=True)
    interview_stage: Mapped[str] = mapped_column(String, nullable=True)


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
        db.select(JobListing).where(or_(JobListing.cv_stage == "", JobListing.cv_stage.contains("?")))
    )
    return len(list(results.scalars()))

def db_count_cv_accepted() -> int:
    results = db.session.execute(db.select(JobListing).where(JobListing.cv_stage == "Yes")).scalars()
    return len(list(results))

def db_count_interviews() -> int:
    results = db.session.execute(db.select(JobListing).where(JobListing.interview_stage == "Yes")).scalars()
    return len(list(results))