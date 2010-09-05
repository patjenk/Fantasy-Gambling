from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from Fantasy_Gambling.bets.models import *

class Sport(models.Model):
  """Store differents types of sports. For example, American Football."""
  name = models.CharField(max_length=200)
  def __unicode__(self):
    return self.name

class League(models.Model):
  """Store a sports league. For example, The NFL."""
  sport = models.ForeignKey(Sport)
  name = models.CharField(max_length=200)
  def __unicode__(self):
    return self.name

class Season(models.Model):
  """Store an individual season for a sports league. For example, the 
  2010-2011 NFL season."""
  league = models.ForeignKey(League)
  name = models.CharField(max_length=200)
  start_datetime = models.DateTimeField()
  def __unicode__(self):
    return self.name

class SeasonInterval(models.Model):
  """Used to breakup a season into units. For example, week 1 of the NFL 
  season."""
  season = models.ForeignKey(Season)
  name = models.CharField(max_length=200)
  start_datetime = models.DateTimeField()
  end_datetime = models.DateTimeField()
  order_number = models.IntegerField()
  def __unicode__(self):
    return self.name
  class Meta:
    ordering = ('order_number',)

class Event(models.Model):
  """An event in a season interval. For example, an individual NFL game in 
  week 1."""
  season_interval = models.ForeignKey(SeasonInterval)
  name = models.CharField(max_length=200)
  start_datetime = models.DateTimeField()
  def __unicode__(self):
    return self.name

class BettingWebsite(models.Model):  
  """ Stores info for a place online where you can store bets """
  name = models.CharField(max_length=100)
  URL = models.CharField(max_length=100)
  def __unicode__(self):
    return self.name

class BetType(models.Model):
  """ The types of bets one can place """
  description = models.TextField()
  name = models.CharField(max_length=100)
  def __unicode__(self):
    return self.name

class Bet(models.Model):
  """ Used to store actual bets on specific sites """
  event = models.ForeignKey(Event)
  bet_type = models.ForeignKey(BetType)
  betting_website = models.ForeignKey(BettingWebsite)
  active = models.BooleanField()
  def __unicode__(self):
    return self.bet_type.name + " - " + self.event.name
  def current_betline(self):
    betlines = BetLine.objects.filter(bet=self).order_by('-updated_datetime')
    if betlines.count() > 0:
      return betlines[0]
    else:
      return None

class BetLine(models.Model):
  """ stores info about specific bets"""
  bet = models.ForeignKey(Bet)
  updated_datetime = models.DateTimeField()
  line = models.DecimalField(max_digits=10, decimal_places=2)
  odds = models.IntegerField()
  def __unicode__(self):
    return str(self.bet) + " - " + str(self.line)

class FantasyLeague(models.Model):
  """Stores information about a group of users competing against each 
  other."""
  name = models.CharField(max_length=100)
  users = models.ManyToManyField(User)
  seasons = models.ManyToManyField(Season)
  public = models.BooleanField()
  def __unicode__(self):
    return self.name
  

class UserBet(models.Model):
  user = models.ForeignKey(User)
  league = models.ForeignKey(FantasyLeague)
  betline = models.ForeignKey(BetLine)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  datetime = models.DateTimeField()
  winner = models.BooleanField()
  def __unicode__(self):
    return self.user.username + " - " + self.betline.bet.event.name + " - " + self.betline.bet.bet_type.name + " - $" + str(self.amount)
  def winningPayout(self):
    result = Decimal('0')
    if self.betline.odds < 0:
      result = (self.amount / (self.betline.odds * Decimal('-1.0')) * 100) + self.amount
    else:
      result = ((self.amount / Decimal('100.0')) * self.betline.odds) + self.amount
    return "%.2f" % result

class UserFunctions:
  def getAvailableUserBets(self):
    leagues = self.getFantasyLeagues()
    season_ids = []
    for league in leagues:
      for season in league.seasons.all():
        season_ids.append(season.id)
    active_intervals = SeasonInterval.objects.filter(start_datetime__lte=datetime.now(), end_datetime__gte=datetime.now(), season__id__in=season_ids)
    result = []
    result = []
    for active_interval in active_intervals:
      bets = Bet.objects.filter(event__season_interval=active_interval)
      for bet in bets:
        result.append(bet)
    return result

  def getActiveUserBets(self):
    leagues = self.getFantasyLeagues()
    season_ids = []
    for league in leagues:
      for season in league.seasons.all():
        season_ids.append(season.id)
    active_intervals = SeasonInterval.objects.filter(start_datetime__lte=datetime.now(), end_datetime__gte=datetime.now(), season__id__in=season_ids)
    result = []
    for active_interval in active_intervals:
      active_bets = UserBet.objects.filter(betline__bet__event__season_interval=active_interval)
      for active_bet in active_bets:
        result.append(active_bet)
    return result
  
  def getExpiredUserBets(self):
    leagues = self.getFantasyLeagues()
    season_ids = []
    for league in leagues:
      for season in league.seasons.all():
        season_ids.append(season.id)
    expired_intervals = SeasonInterval.objects.filter(end_datetime__lt=datetime.now(), season__id__in=season_ids)
    result = []
    for expired_interval in expired_intervals:
      expired_bets = UserBet.objects.filter(betline__bet__event__season_interval=expired_interval)
      for expired_bet in expired_bets:
        result.append(expired_bet)
    return result
  
  def getFantasyLeagues(self):
    return FantasyLeague.objects.filter(users=self)

  def getAvailableCapital(self):
    result = Decimal('0.0')
    for fantasy_league in self.getFantasyLeagues():
      result += self.getAvailableCapitalForLeague(fantasy_league)
    return result

  def getAvailableCapitalForLeague(self, fantasy_league):
    season_ids = []
    result = Decimal('0.0')
    for season in fantasy_league.seasons.all():
      season_ids.append(season.id)
    active_intervals = SeasonInterval.objects.filter(start_datetime__lte=datetime.now(), end_datetime__gte=datetime.now(), season__id__in=season_ids)
    for active_interval in active_intervals:
      active_bets = UserBet.objects.filter(betline__bet__event__season_interval=active_interval, league=fantasy_league, user=self)
      bet_sum = Decimal('0.0')
      for active_bet in active_bets:
        bet_sum += active_bet.amount
      result += (Decimal('1000.0') - bet_sum)
    return result
  def getAvailableCapitalForInterval(self, season_interval):
    active_bets = UserBet.objects.filter(betline__bet__event__season_interval=season_interval)
    bet_sum = Decimal('0.0')
    for active_bet in active_bets:
      bet_sum += active_bet.amount
    return (Decimal('1000.0') - bet_sum)
  def getFantasyLeagueScore(self, fantasy_league):
    userbets = UserBet.objects.filter(league=fantasy_league, user=self)
    result = Decimal('0.0')
    for userbet in userbets:
      if userbet.winner:
        result += Decimal(userbet.winningPayout())
    return result
        

User.__bases__ += (UserFunctions,)

