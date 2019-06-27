from flask import (
    Blueprint,
    render_template,
    current_app
)

from application.frontend.utils import (
    fetch_results,
    summarise_results,
    sort_results
)

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def index():
    return render_template('overview.html', data=summarise_results(current_app.config['STATUS_API']))


@frontend.route('/breakdown')
def breakdown():
    data = sort_results(fetch_results(current_app.config['STATUS_API']))
    return render_template('breakdown.html', data=data)


@frontend.route('/local-authority/<local_authority_id>/result-details')
def result_details_for_authority(local_authority_id):
    # TODO we need a url for full result for latest validation run for this planning authority with all errors
    return render_template('validation-result.html', data={'organisation': local_authority_id})


@frontend.route('/local-authority/<local_authority_id>')
def local_authority_results(local_authority_id):
    url = f"{current_app.config['STATUS_API']}?organisation={local_authority_id}"
    data = fetch_results(url)
    data['results'].sort(key=lambda x: x['date'], reverse=True)
    return render_template('breakdown-by-authority.html', local_authority_id=local_authority_id, data=data, url=url)

# set the assetPath variable for use in
# jinja templates
@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
