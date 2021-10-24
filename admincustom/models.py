from django.db import models
from core.models import TimeStampModel


# class Admin(TimeStampModel):
class Admincustom(models.Model):
    
    name = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 1000, null = False)  
    #누가 로그인했는지 권한을 누가 설정했는지 파악하자

    class Meta:
        db_table = "admincustom"