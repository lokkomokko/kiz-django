from datetime import datetime

from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django import forms
from django.forms import ModelForm, SelectDateWidget
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import UpdateView, ListView


class Sicks(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование группы')
    main_group_codes = models.CharField(max_length=150, verbose_name='Коды главной группы', blank=True, null=True)
    only_sick = models.BooleanField(verbose_name='Болезнь', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Название группы'
        verbose_name_plural = 'Названия группы'

    # pass


class SicksUndergroup(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование группы')
    group_name = models.ForeignKey(Sicks, on_delete=models.CASCADE, null=True, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подгруппы болезни'
        verbose_name_plural = 'Название подгруппы'


class SicksSingle(models.Model):
    name = models.CharField(max_length=150, verbose_name='Код болезни')
    group_name = models.ForeignKey(Sicks, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Группа')
    under_group_name = models.ForeignKey(SicksUndergroup, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name='Подгруппа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Код болезни'
        verbose_name_plural = 'Коды болезней'


class MedManager(models.Manager):

    def days(self, id):
        items = self.objects.filter(user_id=id)
        self.days = 0

        for i in items:
            self.days += i.days

        return self.days


class AgeRange(models.Model):
    name = models.CharField(max_length=50, verbose_name='Диапазон возрастов')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Диапазоны возрастов'
        verbose_name = 'Диапазон возрастов'

class Table(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    data = JSONField(null=True)
    data_all_count = JSONField(null=True)

    def __str__(self):
        return 'Таблица для ' + self.user


class Med(models.Model):
    code_id = models.ForeignKey(SicksSingle, on_delete=models.CASCADE, null=True, verbose_name='Код болезни')
    code_name = models.CharField(max_length=120, verbose_name='Код болезни', null=True)
    sex = models.CharField(max_length=5, choices=(('муж', 'муж'), ('жен', 'жен')), default='муж', verbose_name='Пол')
    adult = models.DateField(verbose_name='Возраст', null=True)
    adult_age = models.IntegerField(verbose_name='Возраст(год)', null=True)
    adult_range = models.ForeignKey(AgeRange, on_delete=models.CASCADE, null=True, )
    days = models.IntegerField(verbose_name='Число дней', default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, )
    pub_date = models.DateTimeField(auto_now_add=True)
    date_1 = models.DateField(verbose_name='С ', help_text='Период болезни:', null=False, default=now())
    date_2 = models.DateField( verbose_name='По', null=False, default=now())

    methods = MedManager

    def _data(self, id, type='all'):
        if type == '10':
            return Med.objects.filter(user_id=id)[:10].values()
        elif type == 'all':
            return Med.objects.filter(user_id=id).values()
        elif type == 'count':
            return Med.objects.filter(user_id=id).count()

    class Meta:
        verbose_name_plural = 'Случаи'
        verbose_name = 'Случай'
        ordering = ['-pub_date']

    def __str__(self):
        return str(self.code_name)

    def save(self, *args, **kwargs):
        from datetime import date

        id = self.code_id_id
        ss = SicksSingle.objects.all().values()
        name = 'error'
        for s in ss:
            if id == str(s['id']):
                name = s['name']
        self.code_name = name
        # self.code_name = self.date_1
        self.adult_age = date.today().year - self.adult.year
        # self.days =
        age = int(self.adult_age)
        for i in range(1, 11):
            if age <= 19 and age < 20:
                self.adult_range_id = 1
                break
            elif age <= 24 and age < 25:
                self.adult_range_id = 2
                break
            elif age <= 29 and age < 30:
                self.adult_range_id = 3
                break
            elif age <= 34 and age < 35:
                self.adult_range_id = 4
                break
            elif age <= 39 and age < 40:
                self.adult_range_id = 5
                break
            elif age <= 44 and age < 45:
                self.adult_range_id = 6
                break
            elif age <= 49 and age < 50:
                self.adult_range_id = 7
                break
            elif age <= 54 and age < 55:
                self.adult_range_id = 8
                break
            elif age <= 59 and age < 60:
                self.adult_range_id = 9
                break
            elif age >= 60:
                self.adult_range_id = 10
                break

        super(Med, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('med-detail', kwargs={'pk': self.pk})


class MedForm(ModelForm):
    # date_1 = forms.DateField(widget=SelectDateWidget(empty_label="Nothing", years=range(1970, 2020)), label='С ',
    #                          help_text='Период болезни')
    # date_2 = forms.DateField(widget=SelectDateWidget(empty_label="Nothing", years=range(1970, 2020)), label='По')

    class Meta:
        model = Med
        fields = ['sex', 'adult', 'date_1', 'date_2']
        widgets = {
            'adult': SelectDateWidget(empty_label="Nothing", years=range(1945, 2020)),
            'date_1': AdminDateWidget(),
            'date_2': AdminDateWidget(),
        }


class MedUpdate(UpdateView):
    model = Med
    template_name = 'main/update.html'
    form_class = MedForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MedUpdate, self).get_context_data(**kwargs)
        context['sicks'] = Sicks.objects.all().values()
        context['single'] = SicksSingle.objects.all().values()
        context['under_group'] = SicksUndergroup.objects.values()

        return context

    def form_valid(self, form):
        from .modules import table
        instance = form.save(commit=False)
        instance.days = (form.cleaned_data.get('date_2') - form.cleaned_data.get('date_1')).days
        instance.code_id_id = self.request.POST['code']
        instance.save()
        table.findTable(list(Med.objects.filter(user_id=self.request.user.pk)), self.request.user.pk)
        return redirect('/')

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if  request.user.username != str(self.get_object().user):
            return HttpResponse('Вы пытаетесь обновить не свою запись. Это невозможно.')
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler(request, *args, **kwargs)

class MedList(ListView):
    model = Med
    template_name = 'main/list.html'
    paginate_by = 25

    def get_queryset(self):
        return Med.objects.filter(user_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
