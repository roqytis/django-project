# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.IntegerField()
    primary = models.IntegerField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class Godok(models.Model):
    godok_no = models.AutoField(primary_key=True)
    year = models.IntegerField()
    die = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'godok'


class SeoulCenter(models.Model):
    center_no = models.AutoField(primary_key=True)
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    welfare = models.IntegerField()
    citizen = models.IntegerField(blank=True, null=True)
    class_field = models.IntegerField(db_column='class', blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'seoul_center'


class SeoulElder(models.Model):
    elder_no = models.AutoField(primary_key=True)
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    silver = models.IntegerField()
    lower = models.IntegerField(blank=True, null=True)
    general = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seoul_elder'


class SeoulHospital(models.Model):
    h_no = models.AutoField(primary_key=True)
    h_name = models.CharField(unique=True, max_length=255)
    h_pass = models.CharField(max_length=255)
    h_open = models.CharField(max_length=255)
    h_addr = models.CharField(max_length=255)
    h_tel = models.CharField(max_length=255)
    h_kind = models.CharField(max_length=255)
    h_wi = models.FloatField(blank=True, null=True)
    h_kung = models.FloatField(blank=True, null=True)
    h_url = models.CharField(max_length=255, blank=True, null=True)
    is_confirmed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seoul_hospital'


class SeoulHospitalAd(models.Model):
    h_no = models.AutoField(primary_key=True)
    h_name = models.CharField(max_length=255)
    h_addr = models.CharField(max_length=255)
    h_tel = models.CharField(max_length=255)
    h_url = models.CharField(max_length=255)
    h_image = models.TextField()
    h_content = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'seoul_hospital_ad'


class SeoulPeople(models.Model):
    people_no = models.AutoField(primary_key=True)
    year = models.IntegerField()
    district = models.CharField(max_length=255, blank=True, null=True)
    all_people = models.IntegerField()
    elder_people = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seoul_people'
