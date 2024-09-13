from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import CustomUser, UserProfile, Category, Subcategory, Income


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
    subcategory = Subcategory.objects.all()
    # в инком user = айди CustomЮзера
    last_incomes = Income.objects.filter(user=(CustomUser.objects.get(email=request.user)).id).order_by('-date')[:10]


    data = {
        "category": category,
        "subcategory": subcategory,
        "last_incomes": last_incomes
    }

    return render(request, 'income_page.html', context=data)