from django.db import models

class Radcheck(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64, default='Cleartext-Password')
    op = models.CharField(max_length=2, default=':=')
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radcheck'
        managed = False

    def __str__(self):
        return self.username


class Radreply(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2, default='=')
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radreply'
        managed = False

    def __str__(self):
        return f"{self.username} → {self.attribute}"


class Radgroupcheck(models.Model):
    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2, default=':=')
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radgroupcheck'
        managed = False

    def __str__(self):
        return self.groupname


class Radgroupreply(models.Model):
    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2, default='=')
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radgroupreply'
        managed = False

    def __str__(self):
        return self.groupname


class Radusergroup(models.Model):
    username = models.CharField(max_length=64)
    groupname = models.CharField(max_length=64)
    priority = models.IntegerField(default=1)

    class Meta:
        db_table = 'radusergroup'
        managed = False

    def __str__(self):
        return f"{self.username} → {self.groupname}"


class Radacct(models.Model):
    radacctid = models.BigAutoField(primary_key=True)
    acctsessionid = models.CharField(max_length=64)
    acctuniqueid = models.CharField(max_length=32, unique=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    nasipaddress = models.GenericIPAddressField()
    acctstarttime = models.DateTimeField(null=True, blank=True)
    acctstoptime = models.DateTimeField(null=True, blank=True)
    acctsessiontime = models.IntegerField(null=True, blank=True)
    acctinputoctets = models.BigIntegerField(null=True, blank=True)
    acctoutputoctets = models.BigIntegerField(null=True, blank=True)
    acctterminatecause = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'radacct'
        managed = False

    def __str__(self):
        return f"{self.username} ({self.acctsessionid})"


class Radpostauth(models.Model):
    username = models.CharField(max_length=64)
    pass_field = models.CharField(max_length=64, db_column='pass')
    reply = models.CharField(max_length=32)
    authdate = models.DateTimeField()

    class Meta:
        db_table = 'radpostauth'
        managed = False

    def __str__(self):
        return f"{self.username} - {self.reply}"


class Nas(models.Model):
    nasname = models.CharField(max_length=128, unique=True)
    shortname = models.CharField(max_length=32, blank=True)
    type = models.CharField(max_length=30, blank=True)
    ports = models.IntegerField(null=True, blank=True)
    secret = models.CharField(max_length=60)
    server = models.CharField(max_length=64, blank=True)
    community = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'nas'
        managed = False

    def __str__(self):
        return self.shortname or self.nasname
