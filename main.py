from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column('photo_id', db.Integer, primary_key=True)
    caption = db.Column(db.Text)
    date = db.Column(db.DateTime)
    category = db.Column(db.String(80))
    url = db.Column(db.Text)
    homepage = db.Column(db.Boolean)

    def __init__(self, caption, category, url, homepage):
        self.caption = caption
        self.category = category
        self.url = url
        self.date = datetime.now()
        self.homepage = homepage


@app.route('/')
def show_all():
    categories = get_categories()
    photo_dict = {}
    for category in categories:
        photos = Photo.query.filter_by(category = category)
        photo_dict[category] = photos

    print photo_dict
    return render_template('show_all.html',photo_dict = photo_dict, categories = get_categories())

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['caption']:
            flash('caption is required', 'error')
        elif not request.form['url']:
            flash('url is required', 'error')
        elif not request.form['category']:
            flash('category is required', 'error')
        else:
            homepage = True
            if request.form.get('homepage') == None:
                homepage = False

            photo = Photo(request.form['caption'], request.form['category'], request.form['url'], homepage)
            db.session.add(photo)
            db.session.commit()
            flash('Photo was successfully created')
            return redirect(url_for('show_all'))
    return render_template('new.html')

@app.route("/delete/<id>")
def delete(id):
    photo = Photo.query(filter_by(id = id).get(1))
    db.session.delete(photo)
    db.session.commit()
    return render_template('show_all.html')

##helper functions

def get_categories():
    photos = Photo.query.all()
    categories = []
    for photo in photos:
        if photo.category not in categories:
            categories.append(photo.category)
    return categories

def get_photos(category):
    photos = Photo.query.filter_by(category = category)
    return photos

def get_homepage_photos():
    photos = Photo.query.filter_by(homepage = True)
    return photos
    
if __name__ == '__main__':
    db.create_all()
    app.run()