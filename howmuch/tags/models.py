from django.db import models

class Tag(models.Model):
	name = models.CharField(max_length=50)
	usage = models.IntegerField(default=1)

	def __unicode__(self):
		return u'%s' % (self.name)
