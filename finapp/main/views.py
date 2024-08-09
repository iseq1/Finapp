from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import CustomUser, UserProfile

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_id = request.user.email
        user = CustomUser.objects.get(email=user_id)
        person = UserProfile.objects.get(user=user)
        return HttpResponse(f"Hello {person.first_name} {person.last_name} from {person.address}, you in FinAPP.com")
    else:
        return render(request, 'index.html')