import urllib

#Return query in format 'juan AND text:carlos AND text:cayetano'
def convert_query(query):
	q=urllib.unquote(query)
	q=q.strip()
	query_list = q.split('-')
	new_query = ' AND text:'.join(query_list)
	return new_query
	

#Return a dict with filter paramenters
def convert_filters(filters):
	f=urllib.unquote(filters)
	f=f.strip()

	filters_list = filters.split('_')
	filters_dic = {}

	try:
		index_cat=filters_list.index('category')
	except ValueError:
		pass
	else:
		filters_dic.update({'category':filters_list[index_cat+1]})

	try:
		index_range=filters_list.index('rangePrice')
	except ValueError:
		pass
	else:
		filters_dic.update({'rangePrice':filters_list[index_range+1]})

	try:
		index_state=filters_list.index('state')
	except ValueError:
		pass
	else:
		filters_dic.update({'state':filters_list[index_state+1]})

	return filters_dic


#Return Value of state key
def get_state_filter(filters):
	try:
		state = filters['state']
	except KeyError:
		state = None
	return state


#Return Value of rangePrice key
def get_rangePrice_filter(filters):
	try:
		rangePrice = filters['rangePrice']
	except KeyError:
		rangePrice = None
	return rangePrice


#Return Value of category key
def get_category_filter(filters):
	try:
		category = filters['category']
	except KeyError:
		category = None
	return category