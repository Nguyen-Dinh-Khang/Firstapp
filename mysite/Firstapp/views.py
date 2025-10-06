from django.shortcuts import render
from .forms import RegistrationForm
from django.http import HttpResponse, HttpResponseRedirect



def Introduce (request):
    context = {
        'name': 'Khang',
        'age': 20
    }
    return render(request, 'page/introduce.html', context)


def Troll (request):
    if request.user.is_authenticated:
        context = {'image_url': 'images/5.jpg'}
    else:
        context = {'image_url': 'images/3.jpg'}
    return render(request, 'page/troll.html', context)


def Register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'page/register.html', {'Form': form})




