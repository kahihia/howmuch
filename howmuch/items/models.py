from django.db import models

class ItemsCatA(models.Model):
    name =  models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class ItemsCatB(models.Model):
    itemsCatA = models.ForeignKey(ItemsCatA)
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class ItemsCatC(models.Model):
    itemsCatB = models.ForeignKey(ItemsCatB)
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name    