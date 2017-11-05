from flask import render_template, redirect 
from models import *
import helpers, jwt
from slugify import slugify
from Admin.AppRepository import AppRepository

def index():
    return render_template('dashboard/apps.html', apps=App.query.all())

def find(app_id):
    app = App.query.get(app_id)
    return render_template('dashboard/app.html', app=app)

def store(request):
    name = request.form.get('app_name')
    slug = slugify(name)
    description = request.form.get('app_description')
    token = jwt.encode({'app_name': slug}, 'feed_engine', algorithm='HS256')
    existing_app = App.query.filter(App.slug.ilike(r"%{}%".format(slug))).first()
    if existing_app:
        return render_template('dashboard/app_create.html', error="App already exists")
    newApp = App(
        id=helpers.generate_unique_code(),
        name=name,
        slug=slug,
        token=token,
        description=description
    )
    db.session.add(newApp)
    db.session.commit()
    return render_template('dashboard/apps.html', apps=App.query.all())

def edit_page(app_id):
    app = App.query.get(app_id)
    return render_template('dashboard/app_update.html', app=app)

def update(request, app_id):
    existing_app = App.query.filter(App.slug.ilike(r"%{}%".format(slugify(request.form.get('app_name'))))).count()
    if existing_app > 1:
        return render_template('dashboard/app_update.html', error="App already exists")
    data = {
        'name' : request.form.get('app_name'),
        'slug' : slugify(request.form.get('app_name')),
        'description' : request.form.get('app_description'),
        'token' : jwt.encode({'app_name': slugify(request.form.get('app_name'))}, 'feed_engine', algorithm='HS256')
    }
    AppRepository().update_app(App, app_id, data)
    return redirect('admin/apps')

def delete_app(app_id):
    AppRepository().delete_app(App, app_id)
    return redirect('admin/apps')

def get_app_feeds(app_id):
    return Feed.query.filter(Feed.app_id == app_id).all()
