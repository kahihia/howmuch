import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from howmuch.pictures.thumbs import ImageWithThumbsField

def make_upload_path(instance, filename):
    file_root, file_ext = os.path.splitext(filename)
    dir_name = '{module}/{model}'.format(module=instance._meta.app_label, model=instance._meta.module_name)
    file_root = unicode(uuid.uuid4())
    name = os.path.join(settings.MEDIA_ROOT, dir_name, file_root + file_ext.lower())
    # Delete existing file to overwrite it later
    if instance.pk:
        while os.path.exists(name):
            os.remove(name)

    return os.path.join(dir_name, file_root + file_ext.lower())

class Picture(models.Model):
    picture = ImageWithThumbsField(upload_to=make_upload_path, sizes=((100,100),(250,250),(250,500),(200,450),(300,450),(250,400),(500,250),(450,200)))
    owner = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.picture.url

    def get_url_100x100(self):
        return str(self.picture.url_100x100).split("?")[0]

    def get_url_250x250(self):
        return str(self.picture.url_250x250).split("?")[0]