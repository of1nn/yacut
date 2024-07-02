import exrex
from flask import render_template, request, flash, redirect

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_short_id():
    return exrex.getone('[a-zA-Z0-9]{6}')


def get_unique_short_id():
    short = get_short_id()
    while URLMap.query.filter_by(short=short).first() is not None:
        short = get_short_id()
    return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
        else:
            opinion = URLMap(original=form.original_link.data, short=short)
            db.session.add(opinion)
            db.session.commit()
            url = request.base_url + short
            flash(url)
    return render_template('index.html', form=form)


@app.route('/<string:url>')
def short_redirect(url):
    full_url = URLMap.query.filter_by(short=url).first_or_404().original
    return redirect(full_url)
