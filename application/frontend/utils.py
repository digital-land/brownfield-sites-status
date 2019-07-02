import requests

from datetime import datetime
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound
from application.extensions import db
from application.models import Cache


def get_cached_result(url, for_date=None):
    if for_date is not None:
        return db.session.query(Cache).filter(Cache.url == url, Cache.created_date == for_date).one()
    else:
        return db.session.query(Cache).filter(Cache.url == url).order_by(Cache.created_date).one()


def cache_result(url, data):
    if db.session.query(Cache).filter(Cache.url == url, Cache.created_date == datetime.today().date()).first() is not None:
        current_app.logger.info('Already have cached data for today')
    else:
        try:
            cache = Cache(url=url, data=data)
            db.session.add(cache)
            db.session.commit()
        except Exception as e:
            current_app.logger.exception('Could not cache results')


def fetch_results(url):
    try:
        cache = get_cached_result(url, for_date=datetime.today().date())
        return cache.data
    except NoResultFound as e:
        current_app.logger.exception(e)
        current_app.logger.info('No cached results')
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        cache_result(url, data)
        return data
    except Exception as e:
        print(e)
        return {}


def sort_results(data):
    if data.get('Items') is not None:
        data['Items'].sort(key=lambda x: x['organisation'])
    return data


def summarise_results(url):
    summary = {"total": 0, "url": 0, "csv": 0, "headers": 0, "valid": 0}
    data = fetch_results(url)
    if data.get('Items') is not None:
        for i in data['Items']:
            if i['validated'] is not None:
                summary['total'] += 1
                if i['validated']['statusCode'] is 200:
                    summary['url'] += 1
                if i['validated']['isCsv'] is True:
                    summary['csv'] += 1
                if i['validated']['hasRequiredHeaders'] is True:
                    summary['headers'] += 1
                if i['validated']['isValid'] is True:
                    summary['valid'] += 1
    return {"last_updated": data.get('last_updated', datetime.today().date()), "summary": summary}