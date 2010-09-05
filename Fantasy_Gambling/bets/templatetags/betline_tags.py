from django import template
from Fantasy_Gambling.bets.models import Bet, BetLine

register = template.Library()

@register.inclusion_tag('betlines_template_tag.html')
def display_betlines_by_bet(bet_id):
  betlines = BetLine.objects.filter(bet__id=bet_id).order_by('-updated_datetime')
  return { 'betlines': betlines, }
