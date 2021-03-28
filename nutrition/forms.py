from django import forms
from .models import *


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['list_Img']


class FoodForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = ListFood
        fields = ("__all__")