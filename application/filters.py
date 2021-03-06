from application.data import LocalAuthorityMapping
la_mapping = LocalAuthorityMapping()


def map_la_code_to_name(id):
	if la_mapping.get_local_authority_name(id) is not None:
		return la_mapping.get_local_authority_name(id)
	return id


def strip(s, chars):
	return s.strip(chars)


def display_error_message(error):
	if 'Date' in error['dataPath'] and error['keyword'] == 'pattern':
		return "should be in format YYYY-MM-DD"

	if 'OwnershipStatus' in error['dataPath'] and error['keyword'] == 'pattern':
		return "should be one of <code>owned by a public authority</code>, <code>not owned by a public authority</code>, <code>unknown ownership</code> or <code>mixed ownership</code>"

	if 'PlanningStatus' in error['dataPath'] and error['keyword'] == 'pattern':
		return "should be one of <code>permissioned</code>, <code>not permissioned</code> or <code>pending decision</code>"

	return error['message']


def count_row_errors(row):
	count = 0
	if len(row['validator']['rowErrors']) > 0:
		for error in row['validator']['rowErrors']:
			if 'params' not in error.keys() or 'format' not in error['params'].keys():
				count += 1
			else:
				if not (error['params']['format'] and error['params']['format'] == 'date'):
					count += 1
				
	return count
