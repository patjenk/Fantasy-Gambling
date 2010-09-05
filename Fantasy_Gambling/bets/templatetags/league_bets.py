from datetime import datetime
from django import template
from django.contrib.auth.models import User
from Fantasy_Gambling.bets.models import Bet, BetLine, FantasyLeague, SeasonInterval, UserBet

register = template.Library()

@register.inclusion_tag('league_bets.html')
def active_bets(fantasy_league, user):
  season_ids = []
  for season in fantasy_league.seasons.all():
    season_ids.append(season.id)
  active_intervals = SeasonInterval.objects.filter(start_datetime__lte=datetime.now(), end_datetime__gte=datetime.now(), season__id__in=season_ids)
  bets = []
  for active_interval in active_intervals:
    expired_bets = UserBet.objects.filter(betline__bet__event__season_interval=active_interval, league=fantasy_league, user=user)
    for expired_bet in expired_bets:
      expired_bet.score = expired_bet.winningPayout()
      bets.append(expired_bet)
  return {
          'bets': bets,
          'fantasy_league': fantasy_league,
          'user': 'user',
         }

@register.inclusion_tag('league_bets.html')
def expired_bets(fantasy_league, user):
  season_ids = []
  for season in fantasy_league.seasons.all():
    season_ids.append(season.id)
  expired_intervals = SeasonInterval.objects.filter(end_datetime__lt=datetime.now(), season__id__in=season_ids)
  bets = []
  for expired_interval in expired_intervals:
    expired_bets = UserBet.objects.filter(betline__bet__event__season_interval=expired_interval, league=fantasy_league, user=user)
    for expired_bet in expired_bets:
      if expired_bet.winner:
        expired_bet.score = expired_bet.winningPayout()
      else:
        expired_bet.score = 0
      bets.append(expired_bet)
  return {
          'bets': bets,
          'fantasy_league': fantasy_league,
          'user': 'user',
         }

@register.inclusion_tag('league_available_capital.html')
def league_available_capital(fantasy_league,user):
  return { 'available_capital': user.getAvailableCapitalForLeague(fantasy_league), }


