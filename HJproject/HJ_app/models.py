from django.db import models

# Create your models here.

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


class SeoulPeople(models.Model):
    people_no = models.AutoField(primary_key=True)
    year = models.IntegerField()
    district = models.CharField(max_length=255, blank=True, null=True)
    all_people = models.IntegerField()
    elder_people = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seoul_people'

class SeoulHospital(models.Model):
    h_no = models.AutoField(primary_key=True)
    h_name = models.CharField(max_length=255, blank=True, null=True)
    h_pass = models.CharField(max_length=255, blank=True, null=True)
    h_open = models.CharField(max_length=255, blank=True, null=True)
    h_addr = models.CharField(max_length=255, blank=True, null=True)
    h_tel = models.CharField(max_length=255, blank=True, null=True)
    h_kind = models.CharField(max_length=255, blank=True, null=True)
    h_wi = models.FloatField(blank=True, null=True)
    h_kung = models.FloatField(blank=True, null=True)
    h_url = models.CharField(max_length=255, blank=True, null=True)
    is_confirmed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'seoul_hospital'

class SeoulHospitalAd(models.Model):
    h_no = models.AutoField(primary_key=True)
    h_name = models.CharField(max_length=255)
    h_addr = models.CharField(max_length=255)
    h_tel = models.CharField(max_length=255)
    h_url = models.CharField(max_length=255)
    h_image = models.ImageField(upload_to='images/', blank=True,
                              null= True)
    h_comment = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        db_table = 'seoul_hospital_ad'

    
    