from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Date
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