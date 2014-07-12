from functools import wraps
from flask import Flask, jsonify, session
from error import error
import grubhub

app = Flask(__name__)

# helper functions
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'token' in session:
      if session['token']:
        return f(*args, **kwargs)
    return jsonify(error["NOT_LOGGED_IN"])
  return decorated_function

def get_param(param):
  return request.form[param]

# routes
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
def login():
  email = get_param('email')
  password = get_param('pass')

  user = gh.do_login(email, password)
  if user is not None:
    session['token'] = result.token
  return jsonify(error["NOT_LOGGED_IN"])

@app.route("/logout", methods=["POST"])
@login_required
def logout():
  del session['token']
  return jsonify(error["SUCCESS"])

@app.route("/search/<count>", methods=["POST"])
@login_required
def search(count=None):
  count = int(count)
  lat = float(get_param("lat"))
  lng = float(get_param("lng"))

  # spawn async search on grubhub db
  # return session id

  return jsonify(error["SUCCESS"])

@app.route("/recall", methods=["POST"])
@login_required
def recall():
  session_id = get_param('session')

  # query db and return

  return jsonify({})

@app.route("/order", methods=["POST"])
@login_required
def order():
  session_id = get_param('session')
  meal_id = get_param('id')
  address = get_param('address')
  payment = get_param('pay')

  # create order

  return jsonify({})

if __name__ == "__main__":
  app.run(port=5001)
