from functools import wraps
from flask import Flask, jsonify, g
from error import error
import grubhub

app = Flask(__name__)

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not hasattr(g, 'user'):
      return jsonify(error["NOT_LOGGED_IN"])
    return f(*args, **kwargs)
  return decorated_function

@app.route("/")
def hello():
  return "This is not accessble to the public"

@app.route("/status", methods=["POST"])
def status():
  return jsonify({"status": True})

@app.route("/signup", methods=["POST"])
def signup(email=None, password=None, first_name=None, last_name=None):
  return gh.do_signup(email, password, first_name, last_name)

@app.route("/login", methods=["POST"])
@login_required
def login(email=None, password=None):
  return gh.do_login(email, password)

@app.route("/logout", methods=["POST"])
@login_required
def logout():
  return

@app.route("/search", methods=["POST"])
@login_required
def search():
  return

@app.route("/recall", methods=["POST"])
@login_required
def recall():
  return

@app.route("/order", methods=["POST"])
@login_required
def order():
  return

if __name__ == "__main__":
  app.run(port=5001)
