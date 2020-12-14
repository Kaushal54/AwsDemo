from django.db import models

# Create your models here.
class ImportData(models.Model):
    name = models.CharField(null=True,blank=True,max_length=255)
    email = models.EmailField(null=True,blank=True,max_length=255)
    phone = models.CharField(null=True,blank=True,max_length=10)
    city = models.CharField(null=True,blank=True,max_length=255)
    country = models.CharField(null=True,blank=True,max_length=255)

    def __str__(self):
        return self.name
