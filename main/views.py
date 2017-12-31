from django.db import connection
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
                new_item.code_id_id = request.POST['code']
                new_item.days = (form.cleaned_data.get('date_2') - form.cleaned_data.get('date_1')).days

                new_item.save()

                table.findTable(list(Med.objects.filter(user_id=u_id)), u_id)
                return redirect('index')
                # return HttpResponse()
        else:
            form = MedForm()
            sicks = Sicks.objects.all().values()
            single = SicksSingle.objects.all().values()
            under_group = SicksUndergroup.objects.values()
            try: Table.objects.get(user_id=u_id)
            except Table.DoesNotExist:
                table_json = False
            else:
                table_json = Table.objects.get(user_id=u_id)
                import json
                table_json.data = json.loads(table_json.data)
                table_json.data_all_count = json.loads(table_json.data_all_count)

            count_case = Med.objects.filter(user_id=u_id).count()
            more_case = 'Добавленные случаи: '
            if  count_case > 10:
                more_case = False

            data = Med.objects.filter(user_id=u_id)[:10].values()

            age_range = AgeRange.objects.values()

        return render(request, 'main/index.html', {
            'form': form,
            'data': data,
            'sicks': sicks,
            'under_group' : under_group,
            'table_json' : table_json,
            'single' : single,
            'more_case' : more_case,
            # 'table' : table.findTable(list(Med.objects.filter(user_id=u_id)), u_id),
            'nums': [2,6,9,13,17, 22,30, 34, 36, 38, 44]
        })
    else:
        return redirect('login')


def delete(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(Med, pk=item_id)
        if str(item.user) != request.user.username:
            return HttpResponse('Вы пытаетесь удалить не свою запись. Не надо')
        item.delete()
        table.findTable(list(Med.objects.filter(user_id=request.user.pk)), request.user.pk)
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
    # ТЕСТОВЫЕ ДАННЫЕ
    # cursor = connection.cursor()
    # from random import randint
    # d = randint(1, 52)
    # import random
    # foo = ['муж', 'жен']
    #
    # c = random.choice(foo)
    # i = 0
    # while i <= 500:
    #     cursor.execute(
    #         "INSERT INTO main_med (code_id_id, code_name, sex, adult, adult_age, adult_range_id, days, user_id, pub_date, date_1, date_2) VALUES (%s, 'test', %s, '1945-01-01'::date, 40, 10, 1, 1, '2017-12-31T13:10:49.570332+00:00'::timestamptz, '1970-01-01'::date, '1970-01-01'::date) ",
    #         [d, c])
    #     i = i + 1

    return render(request, 'main/api.html', {'data': Med.objects.all()})

    # return HttpResponse(Med.objects.all())
    # return render(request, 'maim/api.html', {
    #     'data': data,
    #     'sicks': sicks,
    #     'underSicks': underSicks,
    #     'singleSick' : singleSick
    # })
