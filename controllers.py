from flask import render_template, request, redirect, flash
from app import app
from models import *
from flask_login.utils import login_user, logout_user
import requests
import pymysql.cursors
from forms import QueueForm, RemoveForm
import random
from datetime import datetime
import xmltodict


def getCurrencyData(day):
    resp = requests.get(f'https://www.cbar.az/currencies/{day}.xml')
    result = xmltodict.parse(resp.content)
    print(f'https://www.cbar.az/currencies/{day}.xml')
    return result


@app.route("/exchange",  methods = ['GET','POST'])
def valyuta():
    day = datetime.today().strftime('%d.%m.%Y')
    currency_data = getCurrencyData(day)
    if request.method=='POST':
        picked_data = request.form['picked_data']
        # print(picked_data)
        brand_new_date = f'{picked_data[8:]}.{picked_data[5]}{picked_data[6]}.{picked_data[:4]}'
        currency_data = getCurrencyData(brand_new_date)
        # print(currency_data)
        return render_template("exchange.html", currency_data=currency_data)

    return render_template("exchange.html", currency_data=currency_data)



@app.route('/online-queue', methods = ['GET', 'POST'])
def queue():
    array_number = []
    arr_num = Queue.query.all()
    for i in arr_num:
        array_number.append(i.random_number)
    data = request.form
    form = QueueForm()
    random_number = random.sample(range(1000000, 9999999), 1)
    if random_number not in array_number:
        context = {
            "form": form,
            "random_number": random_number
        }
        if request.method == 'POST':
            form = QueueForm(data=data)
            if form.validate_on_submit():
                user = Queue(name=form.name.data, surname=form.surname.data, email=form.email.data, phone=form.phone.data, date=form.date.data, hour=form.hour.data, random_number=random_number)
                user.save()
                message = f'Sizin növbə kodunuz: "{random_number[0]}". Xahiş olunur, kodu itirməyin!'
                return render_template("new_queue.html", message=message , **context)
    else:
        return redirect('/online-queue')
    return render_template('new_queue.html', **context)



@app.route('/queue', methods=['GET', 'POST'])
def delete():
    data = request.form
    form = RemoveForm()
    if request.method == 'POST':
        form = RemoveForm(data=data)
        if form.validate_on_submit():
            user = Queue.query.filter_by(random_number=data.get('random_number')).first()
            if user:
                user.delete()
                active = True
                return redirect('/queue')
    return render_template('queue.html', form=form)


@app.route('/news', methods=['GET', 'POST'])
def news():
    return render_template('news.html')


@app.route('/press', methods=['GET', 'POST'])
def press():
    press = Press.query.all()
    return render_template('press.html', press=press)


@app.route('/press/<int:ind>', methods=['GET', 'POST'])
def press_ind(ind):
    press = Press.query.all()
    lastpress = Press.query.order_by("date")[-1]
    day = datetime.today().strftime('%d.%m.%Y')
    currency_data = getCurrencyData(day)
    return render_template('press.html', press=press, ind=ind, lastpress=lastpress, currency_data = currency_data)


@app.route('/press-detail/<int:ind>', methods=['GET', 'POST'])
def allpress(ind):
    press = Press.query.filter_by(id = ind)
    lastpress = Press.query.order_by("date")[-1]
    day = datetime.today().strftime('%d.%m.%Y')
    currency_data = getCurrencyData(day)
    return render_template('press_detail.html', press=press, ind=ind, lastpress=lastpress, currency_data = currency_data)


@app.route('/bulleten-detail/<int:ind>', methods=['GET', 'POST'])
def allbulleten(ind):
    bulleten = Bulleten.query.filter_by(id = ind)
    lastpress = Press.query.order_by("date")[-1]
    day = datetime.today().strftime('%d.%m.%Y')
    currency_data = getCurrencyData(day)
    return render_template('bulleten_detail.html', bulleten=bulleten, ind=ind, lastpress=lastpress, currency_data=currency_data)


@app.route('/bulleten', methods=['GET', 'POST'])
def bulleten():
    bulleten = Bulleten.query.all()
    return render_template('bulleten.html', bulleten=bulleten)


@app.route('/bulleten/<int:ind>', methods=['GET', 'POST'])
def bulleten_ind(ind):
    bulleten = Bulleten.query.all()
    lastpress = Press.query.order_by("date")[-1]
    day = datetime.today().strftime('%d.%m.%Y')
    currency_data = getCurrencyData(day)
    return render_template('bulleten.html', bulleten=bulleten, ind=ind, lastpress=lastpress, currency_data=currency_data)


@app.route("/admin/login",  methods = ['GET','POST'])
def index():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if(username=="admin" and password == "123456"):
            user = User(id=1, username="admin", password="123456")
            login_user(user)
            return redirect("/admin") 
        else:
            return render_template("admin-logout.html")
    else:
        return render_template("admin-login.html")


@app.route("/admin/logout",  methods = ['GET'])
def logout():
    logout_user()
    return redirect("/admin/login")


@app.route("/main")
def home():
    slider = Slider.query.all()
    cards = Cards.query.all()
    services = Services.query.all()
    day = datetime.today().strftime('%d.%m.%Y')
    currency_data = getCurrencyData(day)
    print(currency_data)
    return render_template('main.html', slider = slider, cards = cards, services = services, currency_data=currency_data)

    

@app.route("/card/<int:id>")
def card(id):
    card = Cards.query.get(id)
    subcard = Subcard.query.filter_by(card_id = id)
    return render_template('subcard.html', card = card, subcard = subcard)



@app.route("/service/<int:id>")
def service(id):
    service = Services.query.get(id)
    subservice = Subservice.query.filter_by(service_id = id)
    return render_template('subservice.html', service = service, subservice = subservice)



@app.route("/search", methods = ['GET','POST'])
def search():
    lastpress = Press.query.order_by("date")[-1]
    day = datetime.today().strftime('%d.%m.%Y')
    currency_data = getCurrencyData(day)
    if(request.method == 'POST'):           
        keyword = request.form['search']
        print(keyword)
        # press = Press.query.filter(Press.title.contains(keyword)).all()
        press = Press.query.filter((Press.title.contains(keyword)) | (Press.description.contains(keyword))).all()
        return render_template('search.html', press=press,keyword=keyword, lastpress=lastpress, currency_data=currency_data)
    return render_template('search.html', lastpress=lastpress, currency_data=currency_data)







