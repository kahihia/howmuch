import json
import urllib


from django.http import HttpResponse
from django.core import serializers


from howmuch.category.models import Category
from howmuch.tags.models import Tag


def tags_json(request):
	query = urllib.unquote(request.GET.get('query', '')) 
	query = query.strip()
	categoryID = urllib.unquote(request.GET.get('category_id',''))
	categoryID = categoryID.strip()

	category = Category.objects.get(pk=int(categoryID))

	tags = serializers.serialize('python', category.tags.filter(name__contains=query))
	tags_dict = [x['fields'] for x in tags]

	return HttpResponse(json.dumps(tags_dict))


def input_to_words(var):
	words = var.split(",")
	return words

def add_tags(words, id_category, article):
	category = Category.objects.get(pk=id_category)
	names = [tag.name for tag in category.tags.all()]
	for word in words:
		if word not in names:
			tag = Tag.objects.create(name=word)
		else:
			tag = Tag.objects.filter(name=word)[0]
			tag.usage+=1
			tag.save()
		article.tags.add(tag)








