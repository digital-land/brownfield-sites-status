from flask import (
    Blueprint,
    render_template,
    current_app
)

from application.frontend.utils import (
    data_standard_headers,
    fetch_results,
    fetch_validation_result,
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
    url = current_app.config['STATUS_API'] + '/?organisation=' + local_authority_id
    result_data = fetch_validation_result(url)
    return render_template('validation-result.html', data={'organisation': local_authority_id, 'url': url, 'result': result_data})


def _check(given, expected):
    checked = []
    for field in given:
        if field in expected:
            checked.append((field, True))
        else:
            checked.append((field, False))
    checked_expected = []
    for field in expected:
        if field in given:
            checked_expected.append((field, True))
        else:
            checked_expected.append((field, False))
    return checked, checked_expected

@frontend.route('/local-authority/<local_authority_id>/header-details')
def header_details_for_authority(local_authority_id):
    url = current_app.config['STATUS_API'] + '/?organisation=' + local_authority_id
    result_data = fetch_validation_result(url)
    if bool(result_data):
        headers_given = result_data.get('headers').get('given', [])
        checked, checked_data_standard_headers = _check(headers_given, data_standard_headers)
        return render_template(
            'header-results.html',
            expected_headers=checked_data_standard_headers,
            checked=checked,
            data={'organisation': local_authority_id, 'url': url, 'result': result_data})
    else:
        return render_template(
            'header-results.html',
            data={'organisation': local_authority_id, 'url': url, 'result': result_data})


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
