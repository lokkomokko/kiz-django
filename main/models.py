from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.forms import ModelForm, SelectDateWidget
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import UpdateView, ListView


class Sicks(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование группы')

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
        self.code_name = str(self.code_id)
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
    date_1 = forms.DateField(widget=SelectDateWidget(empty_label="Nothing", years=range(1970, 2020)), label='С ',
                             help_text='Период болезни')
    date_2 = forms.DateField(widget=SelectDateWidget(empty_label="Nothing", years=range(1970, 2020)), label='По')

    class Meta:
        model = Med
        fields = ['code_id', 'sex', 'adult']
        widgets = {
            'adult': SelectDateWidget(empty_label="Nothing", years=range(1945, 2020)),
        }


class MedUpdate(UpdateView):
    model = Med
    template_name = 'main/update.html'
    form_class = MedForm
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.days = (form.cleaned_data.get('date_2') - form.cleaned_data.get('date_1')).days
        instance.save()

        return redirect('/')


class MedList(ListView):
    model = Med
    template_name = 'main/list.html'
    paginate_by = 25

    def get_queryset(self):
        return Med.objects.filter(user_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
