from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)
import requests
import json

from application.data import LocalAuthorityMapping

frontend = Blueprint('frontend', __name__, template_folder='templates')

la_mapping = LocalAuthorityMapping()

def extract_result_json(items):
	for i in items:
		if 'NULL' not in i['validated'].keys():
			i['validated']['S'] = json.loads(i['validated']['S'])

	return items

def fetch_results():
	uri = "https://vuhjywgzu1.execute-api.eu-west-2.amazonaws.com/dev/status"
	try:
		uResponse = requests.get(uri)
	except requests.ConnectionError:
		return "Connection Error"

	data = json.loads(uResponse.text)
	items = data['Items']
	items.sort(key=lambda x:x['organisation']['S'])
	return extract_result_json(items)


@frontend.route('/')
def index():
    # TODO make call to api to fetch latest validation result
    # to look up la name from code call: la_mapping.get_local_authority_name('local-authority-eng:ADU')
	json_string = '{"organisation":"local-authority-eng:OLD","latest":"2019-06-21T11:25:40.769Z","results":[{"register-url":"https://www.oldham.gov.uk/downloads/file/4805/oldham_brownfieldregister_2017_12_22_1","validated":{"isValid":false,"isCsv":false,"hasRequiredHeaders":false,"statusCode":200}},{"register-url":"https://www.oldham.gov.uk/downloads/file/4805/oldham_brownfieldregister_2017_12_22_1","validated":{"isValid":false,"isCsv":false,"hasRequiredHeaders":false,"statusCode":200}}]}'

	return render_template('index.html', data=fetch_results())


# set the assetPath variable for use in
# jinja templates
@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
