from datetime import datetime
from django.db import models

class Sport(models.Model):
  """Store differents types of sports. For example, American Football."""
  name = models.CharField(max_length=200)

class League(models.Model):
  """Store a sports league. For example, The NFL."""
  sport = models.ForeignKey(Sport)
  name = models.CharField(max_length=200)

class Season(models.Model):
  """Store an individual season for a sports league. For example, the 
  2010-2011 NFL season."""
  league = models.ForeignKey(League)
  name = models.CharField(max_length=200)
  start_datetime = models.DateTimeField()

class SeasonInterval(models.Model):
  """Used to breakup a season into units. For example, week 1 of the NFL 
  season."""
  season = models.ForeignKey(season)
  name = models.CharField(max_length=200)
  start_datetime = models.DateTimeField()
  end_datetime = models.DateTimeField()
  order_number = models.IntegerField()

class Event(models.Model)
  """An event in a season interval. For example, an individual NFL game in 
  week 1."""
  season_interval = models.ForeignKey(SeasonInterval)
  name = models.CharField(max_length=200)
  start_datetime = models.DateTimeField()
  
