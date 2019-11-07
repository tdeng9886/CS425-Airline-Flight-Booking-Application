from app import app
from flask import Flask, request, send_from_directory


@app.route('/<path:path>')
def static(path):
    return send_from_directory('frontend', path)

