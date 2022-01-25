from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, IntegerField, DateField
from wtforms.fields.html5 import DateField, TimeField, TelField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from extensions import db
from models import Queue, Hour


def hour_query():
    return Hour.query


class QueueForm(FlaskForm):
    name = StringField('Adınız:', validators=[DataRequired(), Length(min=3, max=30)])
    surname = StringField('Soyadınız:', validators=[DataRequired(), Length(min=3, max=30)])
    phone = TelField('Telefon:', validators=[DataRequired(), Length(min=10, max=12)])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    date = DateField('Tarix:', format='%Y-%m-%d', validators=[DataRequired()])
    # hour = SelectField('Saat:', choices=hour)

    hour = QuerySelectField(u'Saat:',      
                               validators=[DataRequired()],
                               query_factory=hour_query)


class RemoveForm(FlaskForm):
    random_number = StringField('Rezervasiya kodunuz:', validators=[DataRequired(), Length(min=7, max=7)])


