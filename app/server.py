from functools import wraps
from flask import Flask, jsonify, session, request
from error import error
from grubhub import Grubhub
import config

app = Flask(__name__)

# helper functions
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'token' in session:
      return f(*args, **kwargs)
    return jsonify(error["NOT_LOGGED_IN"])
  
  return decorated_function

def get_error_code(data):
  print data
  if "ns2:messages" in data:
    if "ns2:message" in data["ns2:messages"]:
      content = data["ns2:messages"]["ns2:message"]
      if content["@type"] == "error":
        return content["@msgCode"]
  return None

# routes
@app.route("/")
def hello():
  return "This is not accessble to the public"

@app.route("/status", methods=["POST"])
def status():
  return jsonify({"status": True})

@app.route("/signup", methods=["POST"])
def signup():
  email = request.form['email']
  password = request.form['pass']
  first_name = request.form['firstName']
  last_name = request.form['lastName']

  user = Grubhub(config.key).sign_up(email, password, first_name, last_name)
  error_code = get_error_code(user)
  if error_code:
    return jsonify(error[error_code])
  return jsonify(user)

@app.route("/login", methods=["POST"])
def login():
  email = request.form['email']
  password = request.form['pass']

  user = Grubhub(config.key).login(email, password)
  error_code = get_error_code(user)
  if error_code:
    return jsonify(error[error_code])

  session['token'] = user["token"]
  return jsonify(error["SUCCESS"])

@app.route("/logout", methods=["POST"])
@login_required
def logout():
  del session['token']
  return jsonify(error["SUCCESS"])

@app.route("/search/<count>", methods=["POST"])
@login_required
def search(count=None):
  count = int(count)
  lat = float(request.form["lat"])
  lng = float(request.form["lng"])
  gh = Grubhub(config.key, session["token"])

  # spawn async search on grubhub db
  # return session id

  return jsonify(error["SUCCESS"])

@app.route("/recall", methods=["POST"])
@login_required
def recall():
  session_id = request.form['session']
  gh = Grubhub(config.key, session["token"])

  # query db and return

  return jsonify({})

@app.route("/order", methods=["POST"])
@login_required
def order():
  session_id = request.form['session']
  meal_id = request.form['id']
  address = request.form['address']
  payment = request.form['pay']
  gh = Grubhub(config.key, session["token"])

  # create order

  return jsonify({})

app.secret_key = config.secret_key

if __name__ == "__main__":
  app.run(port=5001, debug=True)
