from flask import render_template, g
from . import main
from utils.widget_utils import get_weather_outdoor, getPiStatus
from utils.database_utils import getDate
from datetime import datetime
from .. import flatpages
from flask_paginate import Pagination

@main.route('/')
def summary():
    return render_template('summary.html')

@main.route('/temperature')
def temperature():
    temperature_day = getDate('temperature', '24')
    temperature_month = getDate('temperature', '720')
    temperature_year = getDate('temperature', '8640')
    return render_template('temperature.html',
        values_day=temperature_day[0],labels_day=temperature_day[1],
        values_month=temperature_month[0][::3],labels_month=temperature_month[1][::3],
        values_year=temperature_year[0][::15],labels_year=temperature_year[1][::15])

@main.route('/humidity')
def humidity():
    humidity_day = getDate('humidity', '24')
    humidity_month = getDate('humidity', '720')
    humidity_year = getDate('humidity', '8640')
    return render_template('humidity.html',
        values_day=humidity_day[0],labels_day=humidity_day[1],
        values_month=humidity_month[0][::3],labels_month=humidity_month[1][::3],
        values_year=humidity_year[0][::15],labels_year=humidity_year[1][::15])

@main.route('/airquality')
def airquality():
    pm_2_5_day = getDate('pm_2_5', '24')
    pm_2_5_month = getDate('pm_2_5', '720')
    pm_2_5_year = getDate('pm_2_5', '8640')
    pm_10_day = getDate('pm_10', '24')
    pm_10_month = getDate('pm_10', '720')
    pm_10_year = getDate('pm_10', '8640')
    return render_template('airquality.html',
        values1_day=pm_2_5_day[0],labels1_day=pm_2_5_day[1],
        values1_month=pm_2_5_month[0][::3],labels1_month=pm_2_5_month[1][::3],
        values1_year=pm_2_5_year[0][::15],labels1_year=pm_2_5_year[1][::15],
        values2_day=pm_10_day[0],labels2_day=pm_10_day[1],
        values2_month=pm_10_month[0][::3],labels2_month=pm_10_month[1][::3],
        values2_year=pm_10_year[0][::15],labels2_year=pm_10_year[1][::15])

@main.route('/formaldehyde')
def formaldehyde():
    formaldehyde_day = getDate('formaldehyde', '24')
    formaldehyde_month = getDate('formaldehyde', '720')
    formaldehyde_year = getDate('formaldehyde', '8640')
    return render_template('formaldehyde.html',
        values_day=formaldehyde_day[0],labels_day=formaldehyde_day[1],
        values_month=formaldehyde_month[0][::3],labels_month=formaldehyde_month[1][::3],
        values_year=formaldehyde_year[0][::15],labels_year=formaldehyde_year[1][::15])

@main.route("/pi_status")
def pi_status():
    return render_template("widget/pi_status.html", pi_status=getPiStatus())

@main.route("/weather_indoor")
def weather_indoor():
    serial_reslut = {'status': 'uninitialized', 'tmp': 0.0, 'hum': 0.0, 'pm_2_5': 0, 'pm_10': 0, 'CH2O': 0}
    f=open('tmp','r')
    str_array = f.readline().split()
    if len(str_array) == 6:
        serial_reslut['hum'] = str_array[0]
        serial_reslut['tmp'] = str_array[1]
        serial_reslut['pm_2_5'] = str_array[2]
        serial_reslut['pm_10'] = str_array[3]
        serial_reslut['CH2O'] = str_array[4]
        serial_reslut['status'] = str_array[5]
    return render_template("widget/weather_indoor.html", weather_indoor=serial_reslut)

@main.route("/weather_outdoor")
def weather_outdoor():
    return render_template("widget/weather_outdoor.html",
        current_time=datetime.now().strftime('%y-%m-%d %H:%M:%S')
        , weather_outdoor=get_weather_outdoor())

@main.route("/weather_forcast")
def weather_forcast():
    return render_template("widget/weather_forcast.html")

PER_PAGE=10

def get_all():
    if not hasattr(g, 'all'):
        g.all = sorted([p for p in flatpages if 'title' in p.meta ], key=lambda item:item['date'], reverse=True)

@main.route('/blog')
@main.route('/blog/page/<int:page>/')
def index(page = 1):
    get_all()
    posts = g.all[PER_PAGE*(page - 1):page*PER_PAGE]
    pagination = Pagination(page=page, css_framework='bootstrap3', total=len(g.all), per_page=PER_PAGE, record_name='posts')
    return render_template('index.html', posts=posts, pagination=pagination)

@main.route('/blog/<path:path>/')
def post(path):
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)

@main.route('/blog/tag/<string:tag>/', defaults={'page': 1})
@main.route('/blog/tag/<string:tag>/page/<int:page>')
def tag(tag, page=1):
    get_all()
    posts_by_tag = [p for p in g.all if tag in p.meta.get('tags') ]
    posts = posts_by_tag[PER_PAGE*(page - 1):page*PER_PAGE]
    pagination = Pagination(page=page, css_framework='bootstrap3', total=len(posts_by_tag), per_page=PER_PAGE, record_name='tags')
    return render_template('index.html', posts=posts, pagination=pagination)

@main.route('/blog/category/<string:category>/', defaults={'page': 1})
@main.route('/blog/category/<string:category>/page/<int:page>')
def category(category, page=1):
    get_all()
    posts_by_category = [p for p in g.all if category in p.meta.get('categories') ]
    posts = posts_by_category[PER_PAGE*(page - 1):page*PER_PAGE]
    pagination = Pagination(page=page, css_framework='bootstrap3', total=len(posts_by_category), per_page=PER_PAGE, record_name='categories')
    return render_template('index.html', posts=posts, pagination=pagination)

