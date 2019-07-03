from application.data import LocalAuthorityMapping
la_mapping = LocalAuthorityMapping()


def map_la_code_to_name(id):
	if la_mapping.get_local_authority_name(id) is not None:
		return la_mapping.get_local_authority_name(id)
	return id


def strip(s, chars):
	return s.strip(chars)


def display_error_message(error):
	print("ERROR")
	print(error)
	if 'Date' in error['dataPath'] and error['keyword'] == 'pattern':
		return "should be in format YYYY-MM-DD"
	return error['message']
