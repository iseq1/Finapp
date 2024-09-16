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
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    # в инком user = айди CustomЮзера
    last_incomes = Income.objects.filter(user=(CustomUser.objects.get(email=request.user)).id).order_by('-date')[:10]

    data = {
        "category": categories,
        "subcategory": subcategories,
        "last_incomes": last_incomes
    }
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        selected_subcategory = request.POST.get('subcategory')
        selected_total = request.POST.get('total_sum')
        selected_date = request.POST.get('date')
        selected_comment = request.POST.get('comment')

        Income.objects.create(category=Category.objects.get(id=selected_category),
                              subcategory=Subcategory.objects.get(id=selected_subcategory),
                              total=selected_total, date=selected_date, comment=selected_comment,
                              user=CustomUser.objects.get(email=request.user))

        return render(request, 'income_page.html', context=data)

    return render(request, 'income_page.html', context=data)