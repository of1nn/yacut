import re

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    if not request.data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' in data and data['custom_id'] != '':
        short = data['custom_id']
        if not re.match(r'^[a-zA-Z0-9]+$', short) or len(short) > 16:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URLMap.query.filter_by(short=short).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        data['custom_id'] = get_unique_short_id()
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return (
        jsonify(
            {
                'url': urlmap.original,
                'short_link': url_for(
                    'short_redirect', url=urlmap.short, _external=True
                ),
            }
        ),
        201,
    )


@app.route('/api/id/<string:short_id>/')
def get_id(short_id):
    full_url = URLMap.query.filter_by(short=short_id).first()
    if not full_url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': full_url.original})
