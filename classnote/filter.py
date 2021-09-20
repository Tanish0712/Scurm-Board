import django_filters
from django_filters import CharFilter
from django import forms
from .models import ScurmBoard


class DateInput(forms.DateInput):
    input_type = 'date'


class Taskfilter(django_filters.FilterSet):
    Dead_line = django_filters.DateFilter(
        widget=DateInput(
            attrs={
                'class': 'datepicker'
            }
        ),label='Date'

    )
    Task_name = CharFilter(field_name = 'Task_name', lookup_expr = 'icontains', label='Task name')

    class Meta:
        model = ScurmBoard
        fields = ['Task_name', 'Dead_line', 'status']

