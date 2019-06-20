from flask import (
    Blueprint,
    render_template,
    request
)

from application.data import LocalAuthorityMapping

frontend = Blueprint('frontend', __name__, template_folder='templates')

la_mapping = LocalAuthorityMapping()

@frontend.route('/')
def index():
    # TODO make call to api to fetch latest validation result
    # to look up la name from code call: la_mapping.get_local_authority_name('local-authority-eng:ADU')
    return render_template('index.html')

# set the assetPath variable for use in
# jinja templates
@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
