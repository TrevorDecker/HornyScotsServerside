#!/usr/bin/env python
import urllib, urllib2, xml2dict

class Grubhub(object):
  """docstring for Grubhub"""
  def __init__(self, api_key, token=None):
    super(Grubhub, self).__init__()
    self.key = api_key
    self.protocol = "https://"
    self.host = "qa2.ghbeta.com"
    self.format = "xml"
    self.version = "1.0"
    self.token = token


  def get_url(self, url, params):
    params["format"] = self.format
    params["version"] = self.version
    params["apiKey"] = self.key

    if self.token is not None:
      params["token"] = self.token
    data = urllib.urlencode(params)
    print "self.protocol",self.protocol,"\n"
    print "self.host",self.host,"\n"
    print "url",url,"\n"
    print "data",data,"\n"
    f = urllib.urlopen(self.protocol + self.host + url + "?" + data)
    print "hi \n"
    x = xml2dict.parse(f.read())
    return x[x.keys()[0]]

  def search(self, lat, lng, pickup=False):
    params = {
      "lat": lat,
      "lng": lng,
    }
    if pickup:
      params["restaurantType"] = "Pickup"
      params["pickupRadius"] = "1.0"
    return self.get_url("/services/search/results", params)

  def rest_details(self, rest_id, lat, lng):
    params = {
      "restaurantId": rest_id,
      "lat": lat,
      "lng": lng,
    }
    return self.get_url("/services/restaurant/details", params)

  def rest_review(self):
    # todo
    return self.get_url("/services/restaurant/reviews", params)

  def rest_menu(self, rest_id, lat, lng):
    params = {
      "restaurantId": rest_id,
      "lat": lat,
      "lng": lng,
    }
    return self.get_url("/services/restaurant/menu", params)

  def sign_up(self, email, password, firstName, lastName):
    params = {
      "email": email,
      "password": password,
      "firstName": firstName,
      "lastName": lastName,
    }
    return self.get_url("/services/account/create", params)

  def login(self, email, password):
    params = {
      "email": email,
      "password": password,
    }
    return self.get_url("/services/account/details", params)

  def account_edit(self):
    # todo
    return self.get_url("/services/account/edit", params)

  # choiceOptions, subOptions, pickup
  def order_create(self, gen_date, address, rest_id, item_id, options = {}):
    params = {
      "generationDate": gen_date,
      "address1": address["street"],
      "city": address["city"],
      "state": address["state"],
      "zip": address["zip"],
      "lat": address["lat"],
      "lng": address["lng"],
      "restaurantId": rest_id,
      "menuItemId": item_id,
      "quantity": 1,
    }
    for k in options:
      params[k] = options[k]
    return self.get_url("/services/order/new", params)

  def order_get(self, order_id):
    params = {"orderId": order_id}
    return self.get_url("/services/order/retrieve", params)

  # choiceOptions, subOptions
  def order_add_item(self, gen_date, order_id, item_id, options = {}):
    params = {
      "generationDate": gen_date,
      "orderId": order_id,
      "menuItemId": item_id,
      "quantity": 1,
    }
    for k in options:
      params[k] = options[k]
    return self.get_url("/services/order/additem", params)

  def order_update_item(self):
    # todo
    return self.get_url("/services/order/updateitem", params)

  # specialInstructions
  def order_finalize(self, order_id, payment, phone, total, tip, options = {} ):
    params = {
      "orderId": order_id,
      "phone": phone,
      "total": total,
      "tip": tip,
      "tipMethod": payment["method"],
      "payment": payment["method"]
    }
    if payment["method"] == "creditcard":
      params["ccnumber"] = payment["ccnumber"]
      params["ccexpiration"] = payment["ccexpiration"]
      params["cczip"] = payment["cczip"]
    return self.get_url("/services/order/finalize", params)

  def order_reorder(self):
    # todo
    return self.get_url("/services/order/reorder", params)

  def order_change_address(self):
    # todo
    return self.get_url("/services/order/changeAddress", params)
