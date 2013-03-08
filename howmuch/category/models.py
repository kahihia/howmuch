from django.db import models

from howmuch.tags.models import Tag

class Category(models.Model):
	name = models.CharField(max_length=25)
	tags = models.ManyToManyField(Tag)

	def __unicode__(self):
		return u'%s' % (self.name)


