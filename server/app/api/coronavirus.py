from flask import jsonify, request
from app.api import bp
from app import db
import urllib.parse
from app.models import Pagination, ResultSet
from const import daily, area, date

db_name = "coronavirus"


@bp.route(f"/{db_name}/{daily}/", methods=["GET"], endpoint="daily_list")
def get_daily_release_list():
    ref = f"{db_name}/{daily}"
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


@bp.route(f"/{db_name}/{area}/", methods=["GET"], endpoint="area_list")
def get_area_list():
    ref = f"{db_name}/{area}"
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


@bp.route(f"/{db_name}/{date}/", methods=["GET"], endpoint="date_list")
def get_statisic_list():
    ref = f"{db_name}/{date}"
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


@bp.route(f"/{db_name}/{daily}/<id>/", methods=["GET"], endpoint="daily")
def get_daily_release(id):
    return jsonify(db.child(db_name).child(daily).child(id).get().val())


@bp.route(f"/{db_name}/{area}/<id>/", methods=["GET"], endpoint="area")
def get_area(id):
    return jsonify(db.child(db_name).child(area).child(id).get().val())


@bp.route(f"/{db_name}/{date}/<id>/", methods=["GET"], endpoint="date")
def get_statisc(id):
    return jsonify(db.child(db_name).child(date).child(id).get().val())
