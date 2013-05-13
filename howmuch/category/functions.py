from howmuch.category.models import Category
from howmuch.category.categories import CATEGORIES
from howmuch.tags.models import Tag

from django.conf import settings

from indextank.client import ApiClient

#Replace category name. Example: Computacion y Accesorios To Computacion-y-Accesorios
def replace_category_name(category):
	return category.replace(' ','-')

	
#Create all categories and tags
def create_categories_and_tags():
	for category in CATEGORIES:
		new_category = Category.objects.create(name=category['name'])
		new_category.subname = category['index_name']
		new_category.save()
		for tag in category['tags']:
			new_tag = Tag.objects.create(name=tag)
			new_category.tags.add(new_tag)

def defineIndex():
    api = ApiClient('http://:rMESs36rCF83rc@8ytx3.api.searchify.com')
    index = api.get_index(settings.SEARCHIFY_INDEX)
    return({"api": api, "index": index})

def categories_matches():
	index = defineIndex()['index']
	cats = index.search('all:1')
	return cats['facets']['category'].items()

def categories_matches_query(query):
	index = defineIndex()['index']
	cats = index.search(query)
	return cats['facets']['category'].items()

def rangePrice_matches_query(query, dic, minrange, maxrange):
	index = defineIndex()['index']
	searchresults = index.search(query, category_filters=dic, fetch_fields=['text', 'img','description', 'tags','state', 'price'])
	lst=[]
	if minrange != None:
		if maxrange != None:
			for x in searchresults['results']:
				if int(x['price']) > int(maxrange) or int(x['price']) < int(minrange):
					lst.append(x)
		else:
			for x in searchresults['results']:
				if int(x['price']) < int(minrange):
					lst.append(x)
	else:
		if maxrange != None:
			for x in searchresults['results']:
				if int(x['price']) > int(maxrange):
					lst.append(x)
	for y in lst:
		searchresults['results'].remove(y)
		ind = index.search('docid:%s' % (y['docid']))
		cat_ind = ind['facets']['category'].items().pop()[0]
		for cat in searchresults['facets']['category'].items():
			if cat_ind == cat[0]:
				tmp = cat
				del searchresults['facets']['category'][cat[0]]
				searchresults['facets']['category'].update({tmp[0]:tmp[1]-1})
	return searchresults['facets']['category'].items()