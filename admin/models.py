from django.db import models

class Admin(models.Model):
    name     = models.CharField(max_length=16, unique = True)
    password = models.CharField(max_length=128, null = False)  
    
    class Meta:
        db_table = "admin"