#!/usr/bin/python -W ignore::DeprecationWarning

from app import app

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="37.152.183.65", port=8080)
