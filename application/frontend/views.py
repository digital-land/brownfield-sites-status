import json
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

    data = json.loads(resp.text)
    items = data['Items']
    items.sort(key=lambda x: x['organisation'])
    return items


@frontend.route('/')
def index():
    return render_template('index.html', data=fetch_results(current_app.config['STATUS_API']))


# set the assetPath variable for use in
# jinja templates
@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
