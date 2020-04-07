from flask import jsonify, request
from app.api import bp
from app import db
import urllib.parse
from app.models import Pagination, ResultSet
from const import city, country, countrylanguage


@bp.route("/city/", methods=["GET"], endpoint="city_list")
def get_city_list():
    pagination = Pagination(city, request.headers)()
    items = (
        db.child(city)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response


@bp.route("/country/", methods=["GET"], endpoint="country_list")
def get_station_list():
    pagination = Pagination(country, request.headers)()
    items = (
        db.child(country)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response


@bp.route("/countrylanguage/", methods=["GET"], endpoint="countrylanguage_list")
def get_prov_list():
    pagination = Pagination(countrylanguage, request.headers)()
    items = (
        db.child(countrylanguage)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response


@bp.route("/city/<id>/", methods=["GET"], endpoint="city")
def get_train(id):
    return jsonify(db.child(city).child(id).get().val())


@bp.route("/country/<id>/", methods=["GET"], endpoint="country")
def get_station(id):
    return jsonify(db.child(country).child(id).get().val())


@bp.route("/countrylanguage/<id>/", methods=["GET"], endpoint="countrylanguage")
def get_prov(id):
    return jsonify(db.child(countrylanguage).child(id).get().val())
