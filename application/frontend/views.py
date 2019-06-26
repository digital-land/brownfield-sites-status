import requests

from flask import (
    Blueprint,
    render_template,
    current_app
)

frontend = Blueprint('frontend', __name__, template_folder='templates')


def fetch_results(url):

    try:
        resp = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"

    return resp.json()


def fetch_sorted_results(url):
    data = fetch_results(url)
    data['Items'].sort(key=lambda x: x['organisation'])
    return data


def summarise_results(url):
    summary = {"total": 0, "url": 0, "csv": 0, "headers": 0, "valid": 0}
    data = fetch_results(url)
    for i in data['Items']:
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
    return render_template('overview.html', data=summarise_results(current_app.config['STATUS_API']))


@frontend.route('/breakdown')
def breakdown():
    return render_template('breakdown.html', data=fetch_sorted_results(current_app.config['STATUS_API']))


# set the assetPath variable for use in
# jinja templates
@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
