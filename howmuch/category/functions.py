from howmuch.category.models import Category
from howmuch.category.categories import CATEGORIES
from howmuch.tags.models import Tag

#Replace category name. Example: Computacion y Accesorios To Computacion-y-Accesorios
def replace_category_name(category):
	return category.replace(' ','-')

	
#Create all categories and tags
def create_categories_and_tags():
	for category in CATEGORIES:
		new_category = Category.objects.create(name=category['name'])
		new_category.subname = replace_category_name(new_category.name)
		new_category.save()
		for tag in category['tags']:
			new_tag = Tag.objects.create(name=tag)
			new_category.tags.add(new_tag)


	
