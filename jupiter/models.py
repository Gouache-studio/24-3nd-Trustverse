from django.db import models

class Report(models.Model):
    report_id     = models.AutoField(primary_key=True, null = False)
    title         = models.CharField(max_length=255)
    brief         = models.CharField(max_length=255)
    title_picture = models.CharField(max_length=255)
    pdfurl        = models.CharField(max_length=255)

    class Meta:
        db_table = "reports"

