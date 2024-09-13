from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import CustomUser, UserProfile, Category, Subcategory


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
    category = Category.objects.all()
    for item in category:
        print(f'{item.id}.{item.name} - {item.type}')
    subcategory = Subcategory.objects.all()
    for item in subcategory:
        print(f'{item.id}.{item.name}')

    data = {
        "category": category,
        "subcategory": subcategory
    }

    return render(request, 'income_page.html', context=data)