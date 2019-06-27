import requests

from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    current_app
)

from sqlalchemy.orm.exc import NoResultFound
from application.extensions import db
from application.models import Cache

frontend = Blueprint('frontend', __name__, template_folder='templates')


def _get_cached_result(url, for_date=None):
    if for_date is not None:
        return db.session.query(Cache).filter(Cache.url == url, Cache.created_date == for_date).one()
    else:
        return db.session.query(Cache).filter(Cache.url == url).order_by(Cache.created_date).one()


def _cache_result(url, data):
    if db.session.query(Cache).filter(Cache.url == url, Cache.created_date == datetime.today().date()).first() is not None:
        current_app.logger.info('Already have cached data for today')
    else:
        try:
            cache = Cache(url=url, data=data)
            db.session.add(cache)
            db.session.commit()
        except Exception as e:
            current_app.logger.exception('Could not cache results')


def _fetch_results(url):

    try:
        cache = _get_cached_result(url, for_date=datetime.today().date())
        return cache.data
    except NoResultFound as e:
        current_app.logger.exception(e)
        current_app.logger.info('No cached results')

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        _cache_result(url, data)

    except Exception as e:

        data = _get_cached_result(url)

    return data


def _fetch_sorted_results(url):
    data = _fetch_results(url)
    data['Items'].sort(key=lambda x: x['organisation'])
    return data


def _get_result_for_org(data, organisation_id):
    for item in data['Items']:
        if item['organisation'] == organisation_id:
            return item
    return {}


def _summarise_results(url):
    summary = {"total": 0, "url": 0, "csv": 0, "headers": 0, "valid": 0}
    data = _fetch_results(url)
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
    return {"last_updated": data['last_updated'], "summary": summary}


@frontend.route('/')
def index():
    return render_template('overview.html', data=(_summarise_results(current_app.config['STATUS_API'])))


@frontend.route('/breakdown')
def breakdown():
    return render_template('breakdown.html', data=_fetch_sorted_results(current_app.config['STATUS_API']))


@frontend.route('/local-authority/<local_authority_id>/result-details')
def result_details_for_authority(local_authority_id):
    # TODO we need a url for full result for latest validation run for this planning authority with all errors
    return render_template('validation-result.html', data={'organisation': local_authority_id})


@frontend.route('/local-authority/<local_authority_id>')
def local_authority_results(local_authority_id):
    url = f"{current_app.config['STATUS_API']}?organisation={local_authority_id}"
    data = _fetch_results(url)
    data['results'].sort(key=lambda x: x['date'], reverse=True)
    return render_template('breakdown-by-authority.html', local_authority_id=local_authority_id, data=data, url=url)

# set the assetPath variable for use in
# jinja templates
@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
