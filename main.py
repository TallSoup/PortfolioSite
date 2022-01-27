from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer
import os
import datetime as dt
from sqlalchemy.sql.expression import func
from wtforms import Form, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
import smtplib

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL", "sqlite:///portdb1.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Portfolio(db.Model):
    id = Column(Integer, primary_key=True)
    filter = Column(String(120), nullable=False)
    img = Column(String(500), nullable=False)
    alt = Column(String(500), nullable=True)
    h4_desc_title = Column(String(250), nullable=False)
    category = Column(String(500), nullable=False)
    lightbox_desc = Column(String(500), nullable=False)
    link = Column(String(500), nullable=False)


# class ContactForm(FlaskForm):
#     name = StringField("Name", validators=[DataRequired()])
#     email = StringField("Email", validators=[DataRequired(), Email()])
#     message = TextAreaField("Message", validators=[DataRequired()], render_kw={"rows": 10})
#     submit = SubmitField("Send")


# creates the table and database
db.create_all()


# def send_email(name, email, message):
#     with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
#         connection.starttls()
#         connection.login(user=os.environ.get("FROM_EMAIL"), password=os.environ.get("FROM_PASSWORD"))
#         connection.sendmail(
#             from_addr=os.environ.get("FROM_EMAIL"),
#             to_addrs=os.environ.get("MY_EMAIL"),
#             msg=f"Subject:New Email from Portfolio Site\n\nFrom: {name}, Email: {email}, Message: {message}")


@app.route('/')
def home():
    all_portfolio = db.session.query(Portfolio).order_by(func.random())
    filters = list(set([x.filter for x in all_portfolio if x.filter]))
    # form = ContactForm()
    # if form.validate_on_submit():
    #     name = form.name.data
    #     email = form.email.data
    #     message = form.message.data
    #     send_email(name, email, message)
    #     flash("Thanks for the message! I'll be in touch soon!")
    #     return redirect(url_for('home'))
    return render_template('index.html', portfolio=all_portfolio, filters=filters)


# footer year
@app.context_processor
def inject_year():
    year = dt.datetime.now().strftime("%Y")
    return {"year": year}


if __name__ == "__main__":
    app.run(debug=True)
