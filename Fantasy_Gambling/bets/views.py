from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):


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
        return HttpResponse('Log in successful')
      else:
        context_dict['login_error'] = True
    else:
      context_dict['login_error'] = True
  return render_to_response('index.html', context_dict)

@login_required
def user_profile(request, user_name):
  """Display information about a user."""
  return HttpResponse("You are logged in.") 
