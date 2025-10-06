from django.db import models

class Radcheck(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64, default='Cleartext-Password')
    op = models.CharField(max_length=2, default=':=')
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radcheck'

    def __str__(self):
        return self.username
