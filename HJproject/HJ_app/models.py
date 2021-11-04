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