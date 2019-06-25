import json
import requests

from flask import (
    Blueprint,
    render_template
)

frontend = Blueprint('frontend', __name__, template_folder='templates')


def fetch_results():
    uri = "https://vuhjywgzu1.execute-api.eu-west-2.amazonaws.com/dev/status"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"

    data = json.loads(uResponse.text)
    items = data['Items']
    items.sort(key=lambda x: x['organisation'])
    return items


@frontend.route('/')
def index():
    return render_template('index.html', data=fetch_results())


# set the assetPath variable for use in
# jinja templates
@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
