from flask import jsonify, request
from app.api import bp
from app import db
import urllib.parse
from app.models import Pagination, ResultSet
from const import train, station, prov
db_name = 'china_train'

@bp.route(f"/{db_name}/{train}/", methods=["GET"], endpoint="train_list")
def get_train_list():
    ref = f"{db_name}/{train}"
    pagination = Pagination(ref, request.headers)()
    items = (
        db.child(ref)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response


@bp.route(f"/{db_name}/{station}/", methods=["GET"], endpoint="station_list")
def get_station_list():
    ref = f"{db_name}/{station}"
    pagination = Pagination(ref, request.headers)()
    items = (
        db.child(ref)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response


@bp.route(f"/{db_name}/{prov}/", methods=["GET"], endpoint="prov_list")
def get_prov_list():
    ref = f"{db_name}/{prov}"
    pagination = Pagination(ref, request.headers)()
    items = (
        db.child(ref)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response


@bp.route(f"/{db_name}/{train}/<id>/", methods=["GET"], endpoint="train")
def get_train(id):
    return jsonify(db.child(db_name).child(train).child(id).get().val())


@bp.route(f"/{db_name}/{station}/<id>/", methods=["GET"], endpoint="station")
def get_station(id):
    return jsonify(db.child(db_name).child(station).child(id).get().val())


@bp.route(f"/{db_name}/{prov}/<id>/", methods=["GET"], endpoint="prov")
def get_prov(id):
    return jsonify(db.child(db_name).child(prov).child(id).get().val())

