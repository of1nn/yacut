from datetime import datetime, timezone

from yacut import db


FROM_API_TO_MODEL = {'url': 'original', 'custom_id': 'short'}


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(256), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.now(timezone.utc)
    )

    def from_dict(self, data):
        for field in ('url', 'custom_id'):
            if field in data:
                setattr(self, FROM_API_TO_MODEL[field], data[field])
