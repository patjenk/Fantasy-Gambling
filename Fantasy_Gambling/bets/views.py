from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.datastructures import MultiValueDictKeyError
from Fantasy_Gambling.bets.models import *

def index(request):
  if request.user.is_authenticated():
    next = request.GET.get('next', "/user/%s/" % request.user.username)
    return HttpResponseRedirect(next)
  username = request.POST.get('username', None)
  password = request.POST.get('password', None)
  user = authenticate(username=username, password=password)
  context_dict = {
                  'login_error': False,
                 }
  if username != None and password != None:
    if user is not None:
      if user.is_active:
        login(request, user)
        next = request.GET.get('next', "/user/%s/" % user.username)
        #import pdb; pdb.set_trace()
        return HttpResponseRedirect(next)
      else:
        context_dict['login_error'] = True
    else:
      context_dict['login_error'] = True
  return render_to_response('index.html', context_dict)

@login_required
def user_profile(request, username):
  """Display rmation about a user."""
  display_user = get_object_or_404(User, username=username) 

  if 'place_bet' in request.POST:
    # find betline
    valid_bet = True

    # validate bet amount
    if 'amount' in request.POST:
      try:
        bet_amount = Decimal(request.POST['amount'])
      except:
        request.user.message_set.create(message="There was an error placing your bet. '%s' is not a valid number." % request.POST['amount'])
        valid_bet = False
    else :
      request.user.message_set.create(message="There was an error placing your bet. No bet amount was given.")
      valid_bet = False

    # Lookup betline
    if valid_bet:
      try:
        betline = BetLine.objects.get(id=request.POST['betline'])
      except BetLine.DoesNotExist:
        request.user.message_set.create(message="There was an error placing your bet for $%.2f. Please try again." % bet_amount)
        valid_bet = False

    # is this a valid betline?
    if valid_bet:
      current_betline = betline.bet.current_betline()
      if current_betline.line != betline.line or current_betline.odds != betline.odds:
        request.user.message_set.create(message="There was an error placing your bet for $%.2f on %s. The line has changed since you last loaded the page." % (bet_amount, betline.bet.event))
        valid_bet = False

    # does this user have enough cash to make this bet?
    if valid_bet:
      available_cash = request.user.getAvailableCapitalForInterval(betline.bet.event.season_interval)
      if available_cash < bet_amount:
        request.user.message_set.create(message="There was an error placing your bet for $%.2f on %s. The most you can bet on this event is $%.2f." % (bet_amount, betline.bet.event, available_cash))
        valid_bet = False

    # find league
    if valid_bet:
      try:
        league = FantasyLeague.objects.get(id=request.POST['league'])
      except (FantasyLeague.DoesNotExist, MultiValueDictKeyError,):
        request.user.message_set.create(message="There was an error placing your bet for $%.2f on %s. We were unable to determine which Fantasy League you belong to." % (bet_amount, betline.bet.event))
        valid_bet = False

    # make bet!
    if valid_bet:
      newUserBet = UserBet(user=request.user, league=league, betline=current_betline, amount=bet_amount, datetime=datetime.now())
      newUserBet.save()
      request.user.message_set.create(message="Your bet for $%.2f on %s was placed successfully." % (bet_amount, betline.bet.event))

  context_dict = {
                    'request': request,
                    'signed_in': True,
                    'display_user': display_user,
                 }
  return render_to_response('user_profile.html', context_dict, context_instance=RequestContext(request))

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/')

def custom_404(request):
  context_dict = {
                    'request': request,
                    'signed_in': None!=request.user,
                 }
  return HttpResponseNotFound(render_to_response('404.html', context_dict))

def joinleague(request):
  return HttpResponse("Email Patrick to join a league.")

