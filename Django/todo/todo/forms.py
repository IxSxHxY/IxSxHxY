from django.forms import ModelForm
from .models import *

class TodoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = '__all__'