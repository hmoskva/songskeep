from django import forms

from .models import Subscription


class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = ['email',]
        widgets = {
            'email': forms.TextInput(attrs={
                'class': ''
            }),
            # 'site': forms.CheckboxSelectMultiple(attrs={
            #     'class': 'form-control'
            # }),
        }

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        super(SubscriptionForm, self).__init__(*args, **kwargs)
