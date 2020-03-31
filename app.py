#!/usr/bin/python -W ignore::DeprecationWarning

from app import app

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="5.253.25.228", port=8080)
