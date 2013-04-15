from django.db import models

from howmuch.tags.models import Tag

class Category(models.Model):
	name = models.CharField(max_length=25)
	subname = models.CharField(max_length=35, blank=True, null=True )
	tags = models.ManyToManyField(Tag)

	def __unicode__(self):
		return u'%s' % (self.name)


