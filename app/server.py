from functools import wraps
from flask import Flask, jsonify, session, request
from error import error
from grubhub import Grubhub, start_search
import config
from db import DB

app = Flask(__name__)
db = DB()

# helper functions
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

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
@crossdomain(origin='*')
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
@crossdomain(origin='*')
def login():
  email = request.form['email']
  password = request.form['pass'] 

  user = Grubhub(config.key).login(email, password)
  print "user: ", user
  error_code = get_error_code(user)
  if error_code:
    return jsonify(error[error_code])
    #make jason request  
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

  search_id = str(db.make_search(lat, lng, count))
  gh = Grubhub(config.key, session["token"])
  # spawn async search on grubhub db
  # return session id
  r = gh.search(lat, lng)
  rest_list = [parseRest(rest) for rest in r["restaurants"]["restaurant"]]
  start_search(gh, count, search_id, lat, lng, rest_list)

  result = error["SUCCESS"]
  result["id"] = search_id

  return jsonify(result)

def parseRest(rest):
  return {
    "id": rest["@id"],
    "name": rest["name"],
    "rating": float(rest.get("rating", 3.0)),
    "deliveryFee": float(rest.get("delivery-fee", 0.0)),
    "orderMin": float(rest.get("orderMin", 0.0)),
    "phone": rest.get("phone", "No contact"),
  }

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
  app.run(port=5005, host='0.0.0.0', debug=True)
