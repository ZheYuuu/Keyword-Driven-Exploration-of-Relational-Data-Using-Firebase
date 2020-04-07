from flask import jsonify, request
from app.api import bp
from app import db
import urllib.parse
from app.models import Pagination, ResultSet
from const import train, station, prov


@bp.route("/train/", methods=["GET"], endpoint="train_list")
def get_train_list():
    pagination = Pagination(train, request.headers)()
    items = (
        db.child(train)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response


@bp.route("/station/", methods=["GET"], endpoint="station_list")
def get_station_list():
    pagination = Pagination(station, request.headers)()
    items = (
        db.child(station)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response


@bp.route("/prov/", methods=["GET"], endpoint="prov_list")
def get_prov_list():
    pagination = Pagination(prov, request.headers)()
    items = (
        db.child(prov)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response


@bp.route("/train/<id>/", methods=["GET"], endpoint="train")
def get_train(id):
    return jsonify(db.child(train).child(id).get().val())


@bp.route("/station/<id>/", methods=["GET"], endpoint="station")
def get_station(id):
    return jsonify(db.child(station).child(id).get().val())


@bp.route("/prov/<id>/", methods=["GET"], endpoint="prov")
def get_prov(id):
    return jsonify(db.child(prov).child(id).get().val())

