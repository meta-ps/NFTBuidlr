from django.db import models

from django.contrib.auth.models import User
from crm1.settings import BASE_DIR
import uuid
import os

# Create your models here.

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    print(instance,type(instance))
    print(instance.user.id)
    layerPath = BASE_DIR + '/' + str(instance.user.id) + '/images/'+str(instance)
    filename_start = filename.replace('.'+ext,'')

    filename = "%s.%s" % (filename_start, ext)
    return os.path.join(layerPath, filename)


class LayersModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    layer_name = models.CharField(max_length=255,null=True,blank=True)
    img_num =  models.CharField(max_length=3,null=True,blank=True)
    def __str__(self):
        return self.layer_name

class Image(models.Model):
    layer = models.ForeignKey(LayersModel, on_delete=models.CASCADE)
    #img_name = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to=get_file_path,verbose_name=(u'File'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rarity = models.FloatField(default = 0.25)

    def __str__(self):
        return self.layer.layer_name

class ProjectDesc(models.Model):
    user = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    proj_name = models.CharField(max_length=255,null=True,blank=True)
    proj_desc = models.TextField(null=True,blank=True)
    total = models.CharField(max_length=6,null=True,blank=True)
    stats =  models.TextField(null=True,blank=True)
    img_hash = models.CharField(max_length=255,null=True,blank=True)
    meta_hash = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.proj_name


class ArchivedProject(models.Model):
    user = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    proj_name = models.CharField(max_length=255,null=True,blank=True)
    proj_desc = models.TextField(null=True,blank=True)
    total = models.CharField(max_length=6,null=True,blank=True)
    stats =  models.TextField(null=True,blank=True)
    img_hash = models.CharField(max_length=255,null=True,blank=True)
    meta_hash = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.proj_name