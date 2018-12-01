from django.db import models

class Shop(models.Model):
    '''[Enter description for the model here]'''
    name = models.CharField(max_length=255)
