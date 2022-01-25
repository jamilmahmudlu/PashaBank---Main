from flask_login.mixins import UserMixin
from extensions import db
from app import app
from datetime import datetime
from controllers import *


class Queue(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    surname = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(30), nullable=True)
    date = db.Column(db.Date(), nullable=True)
    hour = db.Column(db.String(30), nullable=True)
    random_number = db.Column(db.Integer(), nullable=True, unique=True)

    def __init__(self, name, surname, phone, email, date, hour, random_number):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.date = date
        self.hour = hour
        self.random_number = random_number

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.id} {self.name} {self.surname} {self.email} {self.phone} {self.hour} {self.date} {self.random_number}'



class Hour(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.String(30), nullable=True)

    def __init__(self, time):
        self.time = time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f' {self.time}'



class Press(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=True)
    title = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    text = db.Column(db.Text(), nullable=True)
    press_id = db.Column(db.Integer(), nullable=False)

    def __init__(self, date, title, description, text, press_id):
        self.date = date
        self.title = title
        self.description = description
        self.text = text
        self.press_id = press_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.id} {self.date} {self.title} {self.description} {self.text} {self.press_id}'


class Bulleten(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=True)
    title = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    text = db.Column(db.Text(), nullable=True)
    press_id = db.Column(db.Integer(), nullable=False)

    def __init__(self, date, title, description, text, press_id):
        self.date = date
        self.title = title
        self.description = description
        self.text = text
        self.press_id = press_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.id} {self.date} {self.title} {self.description} {self.text} {self.press_id}'




class Slider(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return f'{self.image}, {self.description}'

    def __init__(self, image, description):
        self.description = description
        self.image = image

    def save(self):
        db.session.add(self)
        db.session.commit()


class Cards(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text(), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    icon = db.Column(db.String(255))                         
    is_valyuta = db.Column(db.Boolean, default = False)
    subcard = db.relationship('Subcard', backref='subcard',lazy=True)

    def __repr__(self):
        return f'{self.title}, {self.description}, {self.image}, {self.icon}, {self.is_valyuta}'

    def __init__(self, title, description, image, icon, is_valyuta):
        self.title = title
        self.description = description
        self.image = image
        self.icon = icon
        self.is_valyuta = is_valyuta

    def save(self):
        db.session.add(self)
        db.session.commit()


class Subcard(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text(), nullable=True)
    icon = db.Column(db.String(255), nullable=True)
    card_id = db.Column(db.Integer(), db.ForeignKey('cards.id'), nullable=True)

    def __repr__(self):
        return f'{self.title}, {self.description}, {self.icon}, {self.card_id}'

    def __init__(self, title, description, icon, card_id):
        self.title = title
        self.description = description
        self.icon = icon
        self.card_id = card_id
        
    def save(self):
        db.session.add(self)
        db.session.commit()

#_____#



class Services(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text(), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    subservice = db.relationship('Subservice', backref='subservice',lazy=True)

    def __repr__(self):
        return f'{self.title}, {self.description}, {self.image}'

    def __init__(self, title, description, image):
        self.title = title
        self.description = description
        self.image = image

    def save(self):
        db.session.add(self)
        db.session.commit()


class Subservice(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text(), nullable=True)
    icon = db.Column(db.String(255))
    service_id = db.Column(db.Integer(), db.ForeignKey('services.id'), nullable=True)




class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False)

    def __init__(self, id, username, password, is_active=True, is_superuser=False):
        self.id = id
        self.username = username
        self.password = password
        self.is_superuser = is_superuser
        self.is_active = is_active
    
