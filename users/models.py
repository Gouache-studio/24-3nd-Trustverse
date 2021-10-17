from django.db import models

class User(models.Model):
    id_trv_user        = models.AutoField(primary_key=True)
    email              = models.CharField(max_length=300, unique = True)
    f_name             = models.CharField(max_length=100, null = True) 
    l_name             = models.CharField(max_length=100, null = True)
    password           = models.CharField(max_length=128, null = False)    
    password_edited_at = models.DateTimeField(null = True, auto_now = True)
    phone_no           = models.CharField(max_length=30, null = False)
    country            = models.CharField(max_length=5, null = False)
    appname            = models.CharField(max_length = 10, null = True) 
    register_datetime  = models.DateTimeField(null= True, auto_now_add = True)
    refer_code         = models.TextField(null = True)
    social_type        = models.CharField(max_length=45,null = True)
    social_uuid        = models.CharField(max_length=300, null = True) 
    inctive_user       = models.BooleanField()    
    
    class Meta:
        db_table = "users"