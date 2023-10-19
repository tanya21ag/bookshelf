from django.db import models

# Create your models here.
from django.db import models

class Pileofbooks(models.Model):
  title = models.CharField(max_length=255)
  author = models.CharField(max_length=255)