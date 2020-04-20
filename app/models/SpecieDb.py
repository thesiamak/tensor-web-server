from app import db
from sqlalchemy.dialects.postgresql import JSON
import json


class SpecieDb(db.Model):
    __tablename__ = 'specie'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    code_name = db.Column(db.String())
    specie_all = db.Column(JSON)
    version = db.Column(db.Integer)
    schema = db.Column(db.String())

    def __init__(self, code, code_name, specie_all, schema):
        self.code = code
        self.code_name = code_name
        self.specie_all = specie_all
        self.schema = schema
        self.version = 1

    def update(self, code, code_name, specie_all, schema):
        if code is not None: self.code = code
        if code_name is not None: self.code_name = code_name
        if specie_all is not None: self.specie_all = specie_all
        if schema is not None: self.schema = schema
        self.version = self.version + 1

    def serialize(self):
        return {"code": self.code, "code_name": self.code_name, "schema": self.schema, "version": self.version,
                "data": json.loads(self.specie_all)}

    def __repr__(self):
        return '<id %i , code %s : %s>' % (self.id, self.code, self.code_name)
