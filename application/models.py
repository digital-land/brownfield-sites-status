import uuid

from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB

from application.extensions import db


def _generate_uuid():
    return uuid.uuid4()


class Cache(db.Model):

    id = db.Column(UUID(as_uuid=True), default=_generate_uuid, primary_key=True, nullable=False)
    url = db.Column(db.String, nullable=False)
    data = db.Column(JSONB, nullable=False)
    created_date = db.Column(db.Date(), default=datetime.today, nullable=False)
