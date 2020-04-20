#!/usr/bin/python -W ignore::DeprecationWarning

from app import app
from app import SpecieDb, db

if __name__ == '__main__':
    #
    # for record in SpecieDb.SpecieDb.query.all():
    #     record.update(record.code, record.code_name, "", record.schema)
    #     db.session.commit()

    from waitress import serve
    serve(app, host="37.152.183.65", port=8080)
