from Fantasy_Gambling.bets.models import Sport, League, Season, SeasonInterval, Event, BettingWebsite, BetType, Bet, BetLine, UserBet, FantasyLeague 
from django.contrib import admin

admin.site.register(Sport)
admin.site.register(League)
admin.site.register(Season)
class SeasonIntervalAdmin(admin.ModelAdmin):
  list_display = ['season', 'name', 'start_datetime', 'end_datetime', 'order_number',]
admin.site.register(SeasonInterval, SeasonIntervalAdmin)
class EventAdmin(admin.ModelAdmin):
  list_display = ['id', 'season_interval', 'name', 'start_datetime',] 
admin.site.register(Event, EventAdmin)
admin.site.register(BettingWebsite)
class BetTypeAdmin(admin.ModelAdmin):
  list_display = ['name', 'description',]
admin.site.register(BetType, BetTypeAdmin)
class BetAdmin(admin.ModelAdmin):
  list_display = ['id', 'event', 'bet_type', 'betting_website', 'active',]
admin.site.register(Bet, BetAdmin)
class BetLineAdmin(admin.ModelAdmin):
  list_display = ['id', 'bet', 'updated_datetime', 'line', 'odds',]
admin.site.register(BetLine, BetLineAdmin)
class UserBetAdmin(admin.ModelAdmin):
  list_display = ['id', 'betline', 'amount', 'datetime',]
admin.site.register(UserBet, UserBetAdmin)
class FantasyLeagueAdmin(admin.ModelAdmin):
  def members(self, object):
    return object.users.count()
  list_display = ['name', 'public', 'members',]
admin.site.register(FantasyLeague, FantasyLeagueAdmin)
