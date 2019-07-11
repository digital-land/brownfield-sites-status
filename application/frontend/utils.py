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


def make_empty_or_yes_error(field_name):
    return {
        'preprocessed': True,
        'dataPath': field_name,
        'message': 'should be either empty or <code>yes</code>. Is case senstive.'
    }


def check_for_empty_and_yes_type(row):
    looking_for = [
        ('maxLength', 'should NOT be longer than 0 characters'),
        ('pattern', 'should match pattern "(yes)"'),
        ('anyOf', 'should match some schema in anyOf')]

    # summarise errors by field
    # check if errors match above
    summary = dict()
    for idx, error in enumerate(row['validator']['rowErrors']):
        currentField = error['dataPath'].strip('.')

        if currentField not in summary:
            summary[currentField] = []

        if (error['keyword'], error['message']) in looking_for:
            summary[currentField].append(idx)

    # if encountered fields have all 3 errors
    # make new error to replace
    new_error_list = []
    to_remove = []
    for field in summary.keys():
        if len(summary[field]) == 3:
            to_remove = to_remove + summary[field]
            new_error_list.append(make_empty_or_yes_error(field))

    # keep all errors not flattened
    errors_to_keep = list(set(range(len(row['validator']['rowErrors']))) - set(to_remove))
    for idx in errors_to_keep:
        new_error_list.append(row['validator']['rowErrors'][idx])
    
    row['validator']['rowErrors'] = new_error_list

    return row


def preprocess_validation_results(data):
    data['_preprocessed'] = False
    if len(data['latestValidationResult']) > 0:
        data['_preprocessed'] = True
        for idx, row in enumerate(data['latestValidationResult']):
            if not row['validator']['isRowValid']:
                data['latestValidationResult'][idx] = check_for_empty_and_yes_type(row)
    return data


def fetch_validation_result(url):
    try:
        resp = requests.get(url)
        data = resp.json()
        return preprocess_validation_results(data)
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
    for item in data:
        if item.get('validated') is not None:
            summary['total'] += 1
            if item['validated']['statusCode'] is 200:
                summary['url'] += 1
            if item['validated']['isCsv'] is True:
                summary['csv'] += 1
            if item['validated']['hasRequiredHeaders'] is True:
                summary['headers'] += 1
            if item['validated']['isValid'] is True:
                summary['valid'] += 1

    return {"last_updated": datetime.today().date(), "summary": summary}


data_standard_headers = [
    "OrganisationURI",
    "OrganisationLabel",
    "SiteReference",
    "PreviouslyPartOf",
    "SiteNameAddress",
    "SiteplanURL",
    "CoordinateReferenceSystem",
    "GeoX",
    "GeoY",
    "Hectares",
    "OwnershipStatus",
    "Deliverable",
    "PlanningStatus",
    "PermissionType",
    "PermissionDate",
    "PlanningHistory",
    "ProposedForPIP",
    "MinNetDwellings",
    "DevelopmentDescription",
    "NonHousingDevelopment",
    "Part2",
    "NetDwellingsRangeFrom",
    "NetDwellingsRangeTo",
    "HazardousSubstances",
    "SiteInformation",
    "Notes",
    "FirstAddedDate",
    "LastUpdatedDate"
]
