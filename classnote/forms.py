from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, ScurmBoard


"""
    User-registration form which extends user model with extra fields
"""

class Join(forms.Form):
    join = forms.CharField(
        strip=True, max_length=6,
        required=True, help_text="Enter the unique code here"
    )

    class Meta:
        model = Project
        fields = [
            'join'
        ]
class DateInput(forms.DateInput):
    input_type = 'date'


class AddTask(ModelForm):
    class Meta:
        model = ScurmBoard
        fields = ['Task_name', 'Task_Description', 'Dead_line', 'status']
        widgets = {
            'Dead_line': DateInput(),
        }
        labels = {'Task_name': 'name', 'Task_Description' : 'Task Description', 'Dead_line' : 'Dead line', 'status': 'Status' }

