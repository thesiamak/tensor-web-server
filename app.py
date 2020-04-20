#!/usr/bin/python -W ignore::DeprecationWarning

from app import app
from app import SpecieDb, db

if __name__ == '__main__':
    #
    # for record in SpecieDb.SpecieDb.query.all():
    #     record.update(record.code, record.code_name, "", record.schema)
    #     db.session.commit()

    app.run(debug=True)