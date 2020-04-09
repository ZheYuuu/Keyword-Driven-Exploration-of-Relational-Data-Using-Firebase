from flask import jsonify, request
from app.api import bp
from app import db
import urllib.parse
from app.models import Pagination, ResultSet
from const import city, country, countrylanguage

db_name = "world"


@bp.route(f"/{db_name}/{city}/", methods=["GET"], endpoint="city_list")
def get_city_list():
    ref = f"{db_name}/{city}"
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


@bp.route(f"/{db_name}/{country}/", methods=["GET"], endpoint="country_list")
def get_station_list():
    ref = f"{db_name}/{country}"
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


@bp.route(
    f"/{db_name}/{countrylanguage}/", methods=["GET"], endpoint="countrylanguage_list"
)
def get_prov_list():
    ref = f"{db_name}/{countrylanguage}"
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


@bp.route(f"/{db_name}/{city}/<id>/", methods=["GET"], endpoint="city")
def get_train(id):
    return jsonify(db.child(db_name).child(city).child(id).get().val())


@bp.route(f"/{db_name}/{country}/<id>/", methods=["GET"], endpoint="country")
def get_station(id):
    return jsonify(db.child(db_name).child(country).child(id).get().val())


@bp.route(
    f"/{db_name}/{countrylanguage}/<id>/", methods=["GET"], endpoint="countrylanguage"
)
def get_prov(id):
    return jsonify(db.child(db_name).child(countrylanguage).child(id).get().val())

@bp.route(f"{db_name}/index", methods=['GET'], endpoint='world_index')
def search():
    keywords = request.args.get('keyword').split(' ')
    ref = f"{db_name}/index"
    mapping = {kw:{} for kw in keywords}
    entrys = set()
    for kw in keywords:
        items = db.child(ref).child(kw).get().val()
        if not items:
            return jsonify([])
        for item in items:
            tmp = item['table']+'/'+item['pk']
            entrys.add(tmp)
            mapping[kw][tmp] = True
    result = []
    for entry in entrys:
        weight = 0
        for kw in keywords:
            weight += 1 if entry in mapping[kw] else 0
        table, pk = entry.split('/')
        link = f"/api/{entry}.json"
        result.append({"table":table, "pk":pk, "_link":link, "weight":weight})
    
    result = sorted(result, key=lambda d: d['weight'], reverse=True)
    return jsonify(result)
