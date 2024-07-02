from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(message='Что-то не так с ссылкой', require_tld=False),
        ],
    )
    custom_id = StringField(
        'Укороченная ссылка',
        validators=[
            Optional(),
            Length(1, 16),
            Regexp(r'^[a-zA-Z0-9]+$', message='Неправильный шаблон ссылки'),
        ],
    )
    submit = SubmitField('Укоротить')
