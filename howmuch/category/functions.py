from howmuch.category.models import Category
from howmuch.category.categories import CATEGORIES
from howmuch.tags.models import Tag

def create_categories_and_tags():
	for category in CATEGORIES:
		new_category = Category.objects.create(name=category['name'])
		for tag in category['tags']:
			new_tag = Tag.objects.create(name=tag)
			new_category.tags.add(new_tag)


	
