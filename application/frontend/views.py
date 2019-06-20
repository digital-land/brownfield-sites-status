from flask import (
    Blueprint,
    render_template,
    request
)

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    # TODO make call to api to fetch latest validation result
    return render_template('index.html')

# set the assetPath variable for use in
# jinja templates
@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
