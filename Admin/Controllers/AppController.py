from flask import render_template, redirect 
from models import *
from slugify import slugify

def index():
    return render_template('dashboard/apps.html', apps=App.query.all())

def find(app_id):
    app = App.query.get(app_id)
    return render_template('dashboard/app.html', app=app)

def store(request):
    name = request.form.get('app_name')
    slug = slugify(name)
    description= request.form.get('app_description')

    existing_app = App.query.filter(App.slug.ilike(r"%{}%".format(slug))).first()
    if existing_app:
        return render_template('dashboard/app_create.html', error="App already exists")
    newApp = App(
        name=name,
        slug=slug,
        description=description
    )
    db.session.add(newApp)
    db.session.commit()
    return render_template('dashboard/apps.html', apps=App.query.all())

def get_app_feeds(app_id):
    return Feed.query.filter(Feed.app_id == app_id).all()
