"""
Main Python file from which the Flask app is to be run. The app is hosted on localhost, port 5000.
"""
from datetime import timedelta

from flask import Flask

from health_warehouse.blueprints.account import account

try:
    # Windows implementation to open the HTML documentation file in the browser.
    from os import startfile

    os_ = 'windows'

except ImportError:
    # MacOS or Linux implementation to open the HTML documentation file in the browser.
    from subprocess import call

    os_ = 'unix'

app = Flask(__name__)
app.secret_key = '238746bq2837o64478e6o'
app.permanent_session_lifetime = timedelta(minutes=10)

app.register_blueprint(account, url_prefix='/account')


@app.route('/')
def homepage():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
