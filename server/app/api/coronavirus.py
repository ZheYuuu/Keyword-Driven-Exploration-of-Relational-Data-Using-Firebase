from flask import jsonify, request
from app.api import bp
from app import db
import urllib.parse
from app.models import Pagination, ResultSet

daily = "daily_situation"
area = "area"
date = "statisic"


@bp.route("/daily_situation/", methods=["GET"], endpoint="daily_list")
def get_daily_release_list():
    pagination = Pagination(daily, request.headers)()
    items = (
        db.child(daily)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response 


@bp.route("/area/", methods=["GET"], endpoint="area_list")
def get_area_list():
    pagination = Pagination(area, request.headers)()
    items = (
        db.child(area)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response  


@bp.route("/statisic/", methods=["GET"], endpoint="date_list")
def get_statisic_list():
    pagination = Pagination(date, request.headers)()
    items = (
        db.child(date)
        .order_by_key()
        .start_at(pagination.start)
        .limit_to_first(pagination.page_size)
        .get()
    )
    last = next(reversed(items.val()))
    response = ResultSet(items.val(), pagination, last).response()
    return response 


@bp.route("/daily_situation/<id>/", methods=["GET"], endpoint="daily")
def get_daily_release(id):
    return jsonify(db.child(daily).child(id).get().val())


@bp.route("/area/<id>/", methods=["GET"], endpoint="area")
def get_area(id):
    return jsonify(db.child(area).child(id).get().val())


@bp.route("/statisic/<id>/", methods=["GET"], endpoint="date")
def get_statisc(id):
    return jsonify(db.child(date).child(id).get().val())
