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
        user_data = {
            "name": person.first_name,
            "surname": person.last_name,
            "address": person.address,
            "tel": person.phone_number,
            "db": person.date_of_birth,
        }
        return render(request, 'index.html', context=user_data)
    else:
        return render(request, 'index.html', context={})


def income_page(request):
    return render(request, 'income_page.html')