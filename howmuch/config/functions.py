def has_changes(request):
	if request.GET.__contains__('change_config') and request.GET['change_config']:
		return True
	return False
