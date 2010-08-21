from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
  username = request.POST.get('username', None)
  password = request.POST.get('password', None)
  user = authenticate(username=username, password=password)
  if username != None and password != None:
    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponse('Log in successful')
      else:
        return HttpResponse('Error, disabled')
    else:
      return HttpResponse('No Username exists for that password')
  else:
    return render_to_response('index.html')
