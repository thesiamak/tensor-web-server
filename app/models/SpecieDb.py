from app import db
from sqlalchemy.dialects.postgresql import JSON


class SpecieDb(db.Model):
    __tablename__ = 'specie'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    specie_all = db.Column(JSON)
    version = db.Column(db.Integer)
    schema = db.Column(db.String())

    def __init__(self, code, specie_all, schema):
        self.code = code
        self.specie_all = specie_all
        self.schema = schema
        self.version = 1

    def update(self, code, specie_all, schema):
        self.code = code
        self.specie_all = specie_all
        self.schema = schema
        self.version = self.version + 1

    def __repr__(self):
        return '<id {}>'.format(self.id)