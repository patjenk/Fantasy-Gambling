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
  season = models.ForeignKey(Season)
  name = models.CharField(max_length=200)
  start_datetime = models.DateTimeField()
  end_datetime = models.DateTimeField()
  order_number = models.IntegerField()

class Event(models.Model):
  """An event in a season interval. For example, an individual NFL game in 
  week 1."""
  season_interval = models.ForeignKey(SeasonInterval)
  name = models.CharField(max_length=200)
  start_datetime = models.DateTimeField()

class BettingWebsite(models.Model):  
  """ Stores info for a place online where you can store bets """
  name = models.CharField(max_length=100)
  URL = models.CharField(max_length=100)

class BetType(models.Model):
  """ The types of bets one can place """
  description = models.TextField()
  name = models.CharField(max_length=100)

class Bet(models.Model):
  """ Used to store actual bets on specific sites """
  event = models.ForeignKey(Event)
  bet_type = models.ForeignKey(BetType)
  betting_website = models.ForeignKey(BettingWebsite)
  active = models.BooleanField()

class BetLine(models.Model):
  """ stores info about specific bets"""
  bet = models.ForeignKey(Bet)
  updated_datetime = models.DateTimeField()
  line = models.DecimalField(max_digits=10, decimal_places=2)
  odds = models.IntegerField()


