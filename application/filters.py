from application.data import LocalAuthorityMapping
la_mapping = LocalAuthorityMapping()

def map_la_code_to_name(id):
	return la_mapping.get_local_authority_name(id)