import json
import urllib

from django.http import HttpResponse
from django.core import serializers

from howmuch.article.models import Article

def tags_json(request):
	query = urllib.unquote(request.GET.get('query', '')) 
	query = query.strip()
	tags = serializers.serialize('python', Article.tags.filter(name__contains=query))
	tags_dict = [x['fields'] for x in tags]
	return HttpResponse(json.dumps(tags_dict))

