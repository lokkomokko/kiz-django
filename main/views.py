from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from . modules import table

def index(request):
    if request.user.is_authenticated:
        u_id = request.user.pk
        if request.method == 'POST':
            form = MedForm(request.POST)
            if form.is_valid():
                new_item = form.save()
                new_item.user_id = u_id
                new_item.days = (form.cleaned_data.get('date_2') - form.cleaned_data.get('date_1')).days
                new_item.save()
                return redirect('index')
                # return HttpResponse()
        else:
            form = MedForm()
            sicks = Sicks.objects.all()
            count_case = Med.objects.filter(user_id=u_id).count()
            more_case = 'Добавленные случаи: '
            if  count_case > 10:
                more_case = False

            data = Med.objects.filter(user_id=u_id)[:10].values()
            under_group = SicksUndergroup.objects.values()
            age_range = AgeRange.objects.values()

        return render(request, 'main/index.html', {
            'form': form,
            'data': data,
            'sicks': sicks,
            'under_group' : under_group,
            'age_range' : age_range,
            'more_case' : more_case,
            'table' : table
        })
    else:
        return redirect('login')


def delete(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(Med, pk=item_id)
        item.delete()
        return redirect('index')
    else:
        return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'main/signup.html', {'form': form})


def api(request):
    table = ['dsd']

    data = list(Med.objects.all())
    sicks = list(Sicks.objects.all())
    underSicks = list(SicksUndergroup.objects.all())
    singleSick = list(SicksSingle.objects.all())

    for sick in Sicks.objects.all():
        table = sick.name

    return HttpResponse(table)
    # return render(request, 'maim/api.html', {
    #     'data': data,
    #     'sicks': sicks,
    #     'underSicks': underSicks,
    #     'singleSick' : singleSick
    # })
