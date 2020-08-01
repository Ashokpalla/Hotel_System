from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from hotel.models import (Customer,RoomNumber, User)


class EmployerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        if commit:
            user.save()
        return user


class CustomerSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=RoomNumber.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.interests.add(*self.cleaned_data.get('interests'))
        return user


class CustomerInterestsForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


