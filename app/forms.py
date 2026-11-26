from flask_wtf import FlaskForm
from wtforms import StringField, URLField,SelectField, SubmitField
from wtforms.validators import InputRequired, URL


class AutoEntry(FlaskForm):
    url_auto = URLField("Job Posting Link", validators=[InputRequired(), URL()])
    is_recruiting_auto = SelectField("Is this from a Recruiting company?", choices=["No", "Yes"], default="No")
    scrape = SubmitField("Scrape")


class ManualEntry(FlaskForm):
    company = StringField("Company Name", validators=[InputRequired()])
    role = StringField("Role Title", validators=[InputRequired()])
    location_choices = ["Glasgow", "Edinburgh", "Remote"]
    location = SelectField("Job Location", choices=[*location_choices], validators=[InputRequired()])
    website_choices = ["Direct", "Linkedin", "Indeed", "totaljobs", "WTTJ", "Reed"]
    website = SelectField("Job Board Website", choices=[*website_choices], validators=[InputRequired()])
    url_manual = URLField("Job Posting Link", validators=[InputRequired(), URL()])
    is_recruiting_manual = SelectField("Is this from a Recruiting company?", choices=["No", "Yes"], default="No")
    submit = SubmitField("Submit")