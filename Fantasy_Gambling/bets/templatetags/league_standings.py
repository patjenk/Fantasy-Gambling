from django import template
from django.contrib.auth.models import User
from Fantasy_Gambling.bets.models import Bet, BetLine, FantasyLeague, UserBet

register = template.Library()

@register.inclusion_tag('league_standings.html')
def league_standings(fantasy_league, current_user):
  users = []
  for league_user in fantasy_league.users.all():
    league_user.score = league_user.getFantasyLeagueScore(fantasy_league)
    users.append(league_user)
  ranked_users = sorted(users, key=lambda user: user.score, reverse=True)
  return {
          'current_user': 'current_user',
          'fantasy_league': fantasy_league,
          'users': ranked_users, 
         }
