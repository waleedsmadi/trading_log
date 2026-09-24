from django import forms
from .models import Strategy
from django.core.exceptions import ValidationError


class CreateStrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['title', 'rules', 'balance', 'test_days']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of the strategy...',
                'id': 'create-strategy-title',
            }),

            'rules': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '13',
                'cols': '20',
                'placeholder': 'Write the rules of the strategy like:\n1 - first rule.\n2 - second rule\netc...',
                'id': 'create-strategy-rules',
            }),

            'balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Balance...',
                'id': 'create-strategy-balance',
            }),

            'test_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Test days...',
                'id': 'create-strategy-test-days',
            })
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('The `title` field should not be empty!')
        return title

    def clean_rules(self):
        rules = self.cleaned_data.get('rules')
        if not rules:
            raise ValidationError('The `rules` field should not be empty!')
        return rules

    def clean_balance(self):
        balance = self.cleaned_data.get('balance')
        if not balance:
            raise ValidationError('The `balance` field should not be empty!')

        try:
            balance = int(balance)
        except:
            raise ValidationError('The `balance` field should contains just numbers!')

        if balance < 5:
            raise ValidationError('The `balance` field should be 5 or more!')
        return balance


    def clean_test_days(self):
        test_days = self.cleaned_data.get('test_days')
        if not test_days:
            raise ValidationError('The `test days` field should not be empty!')

        try:
            test_days = int(test_days)
        except:
            raise ValidationError('The `test days` field should contains just numbers!')


        if not isinstance(test_days, int):
            raise ValidationError('The `test days` field should be an integer number!')
        
        if test_days < 1:
            raise ValidationError('The `test days` field should be 1 or more!')
        return test_days
