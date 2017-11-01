from flask import render_template, redirect 
from models import *
from slugify import slugify

def index():
    print "here"
    return render_template('dashboard/apps.html', apps=App.query.all())

def store(request):
    name = request.form.get('app_name')
    slug = slugify(name)
    description= request.form.get('app_description')

    newApp = App(
        name=name,
        slug=slug,
        description=description
    )
    db.session.add(newApp)
    db.session.commit()
    return render_template('dashboard/apps.html', apps=App.query.all())
